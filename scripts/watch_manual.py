#!/usr/bin/env python3
"""CFP watcher for manually maintained conferences.

For every entry in data/conferences.yml that carries a ``watch`` key (the
conferences with no ccfddl coverage: SfN, OHBM, EMBC, NER, BCI Meeting,
ACII, ISBI), fetch the watched page, keep only the deadline-related lines,
and fingerprint them. When the fingerprint changes between weekly runs, the
script opens a GitHub Issue listing the extracted candidate dates — so
maintenance shifts from "remember to check 7 sites" to "react to an issue".

State lives in data/watch_state.json (committed by the workflow).
Requires: requests, ruamel.yaml. GITHUB_TOKEN + GITHUB_REPOSITORY env vars
enable issue creation; without them the script just prints findings.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from html import unescape
from pathlib import Path

import requests
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "conferences.yml"
STATE = ROOT / "data" / "watch_state.json"

UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")}

KEYWORDS = re.compile(
    r"deadline|submission|submit|abstract|call for|cfp|due|important date|"
    r"registration|meeting|conference|congress|workshop", re.I)
MONTH = (r"(?:january|february|march|april|may|june|july|august|september|"
         r"october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)")
DATE_PAT = re.compile(
    rf"{MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?\s*(?:[–\-—]\s*\d{{1,2}})?,?\s+20\d{{2}}|"
    rf"\d{{4}}-\d{{2}}-\d{{2}}|"
    rf"\d{{1,2}}\s*(?:[–\-—]\s*\d{{1,2}})?\s+{MONTH}\s+20\d{{2}}|"
    rf"{MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?\b", re.I)


def page_text(url: str) -> str | None:
    try:
        r = requests.get(url, headers=UA, timeout=45)
        if r.status_code != 200:
            return None
        t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", r.text, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", "\n", t)
        return unescape(t)
    except requests.RequestException:
        return None


def deadline_lines(text: str) -> list[str]:
    """Date-bearing lines whose ±2-line context mentions a CFP keyword.

    HTML tables usually split the label ('Abstract deadline') and the date
    ('January 15, 2027') into separate lines, so match on a context window.
    """
    lines = [" ".join(l.split()) for l in text.splitlines() if l.strip()]
    out, seen = [], set()
    for i, ln in enumerate(lines):
        if len(ln) > 300 or not DATE_PAT.search(ln):
            continue
        ctx = " | ".join(lines[max(0, i - 2):i + 2])[:300]
        if KEYWORDS.search(ctx) and ctx not in seen:
            seen.add(ctx)
            out.append(ctx)
    return out[:30]


def open_issue(title: str, body: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not (token and repo):
        print("  (no GITHUB_TOKEN/REPOSITORY — printing instead of opening issue)")
        print(body)
        return
    api = f"https://api.github.com/repos/{repo}"
    hdrs = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    # skip if an open issue with the same title already exists
    q = requests.get(f"{api}/issues", headers=hdrs,
                     params={"state": "open", "labels": "cfp-watch"}, timeout=30)
    if q.ok and any(i["title"] == title for i in q.json()):
        print(f"  issue already open: {title}")
        return
    r = requests.post(f"{api}/issues", headers=hdrs, timeout=30,
                      json={"title": title, "body": body, "labels": ["cfp-watch"]})
    print(f"  issue {'created' if r.ok else 'FAILED ' + str(r.status_code)}: {title}")


def main() -> int:
    yaml = YAML()
    docs = yaml.load(DATA.read_text())
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    changed_state = False

    for c in docs:
        url = c.get("watch")
        if not url:
            continue
        cid = c["id"]
        text = page_text(str(url))
        if text is None:
            print(f"[{cid}] fetch failed: {url}")
            continue
        lines = deadline_lines(text)
        digest = hashlib.sha256("\n".join(lines).encode()).hexdigest()
        prev = state.get(cid, {}).get("hash")

        if prev is None:
            print(f"[{cid}] baseline recorded ({len(lines)} deadline lines)")
        elif digest != prev:
            print(f"[{cid}] CHANGE detected on {url}")
            body = (
                f"The watched page for **{c['title']} {c['year']}** changed its "
                f"deadline-related content.\n\n"
                f"- Page: {url}\n- Entry: `{cid}` in `data/conferences.yml` "
                f"(current deadline: `{c.get('deadline')}`)\n\n"
                "Extracted candidate lines:\n\n"
                + "\n".join(f"> {ln}" for ln in lines[:15] or ["(none matched)"])
                + "\n\nReview the page and update `data/conferences.yml` if needed."
            )
            open_issue(f"CFP update detected: {c['title']} {c['year']}", body)
        else:
            print(f"[{cid}] no change")

        state[cid] = {"hash": digest, "lines": lines}
        changed_state = True

    if changed_state:
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
