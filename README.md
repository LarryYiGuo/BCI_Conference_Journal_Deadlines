# 🧠 BCI Conference Deadlines

**Live site:** https://larryyiguo.github.io/BCI_Conference_Deadlines/

A deadline tracker for **BCI / EEG / brain-signal** researchers — 40 conferences across
machine learning, data mining, vision & multimedia, affective computing, signal
processing, biomedical engineering and neural engineering.

## Features

- **Live countdowns** to every upcoming submission deadline, grouped into
  *Upcoming / To-be-announced / Passed*
- **Abstract vs. submission** deadlines in two colors (blue / red), drawn on a
  per-conference **timeline** with a today marker; multi-round venues are labeled
  (*Round 1*, *Cycle 1*, …)
- **Add to calendar** — Google Calendar link and `.ics` download for every deadline
- **Auto-updated** — dates sync weekly from the
  [ccfddl dataset](https://github.com/ccfddl/ccf-deadlines); conferences outside that
  dataset are watched on their official sites and flagged for review when a CFP changes.
  Closed deadlines move to *TBA* until the next cycle is announced
- **Venue metrics** — CCF rank, CORE rank and Google Scholar h5-index on every card
  (conferences have no JCR impact factor; h5 is the standard citation metric)
- **Four color themes, shaded by rank** — the darker the color, the higher the venue rank
- **EN / 中文** with shareable filter URLs (`?sub=ML,CV&lang=en`)

## Categories

| Theme | Color | Subs | Conferences |
|-------|-------|------|-------------|
| Algorithms | 🔵 blue | `ML` `DM` `NC` | NeurIPS · ICLR · ICML · AAAI · IJCAI · UAI · AISTATS · ACML · KDD · WWW · SIGIR · ECML PKDD · CIKM · ICDM · SDM · PAKDD · IJCNN · ICONIP |
| Vision & Interaction | 🟣 purple | `CV` `AC` | CVPR · ICCV · ECCV · ACM MM · MM Asia · WACV · BMVC · ICME · ICIP · ACII · ICMI |
| Medical & Signal | 🟡 amber | `BME` `SP` | EMBC · BIBM · MICCAI · ISBI · IEEE SMC · ICASSP · EUSIPCO |
| Neuro | 🔴 red | `BCI` | IEEE NER · International BCI Meeting · SfN · OHBM |

## Data

Pure static site, no build step. All data lives in
[`data/conferences.yml`](data/conferences.yml) — edit the YAML and the site updates.
Dates marked *Est.* are projected from past cycles; always confirm with the official
CFP. Journals (TPAMI, TNNLS, JNE, TNSRE, …) have rolling submissions and are not
tracked. PRs fixing dates are welcome.

```bash
# local preview
python3 -m http.server 8000   # open http://localhost:8000
```

## License

MIT

---

# 🧠 BCI 会议截稿日历

**在线访问:** https://larryyiguo.github.io/BCI_Conference_Deadlines/

面向 **BCI / EEG / 脑信号** 研究者的会议截稿追踪——覆盖机器学习、数据挖掘、视觉多媒体、
情感计算、信号处理、医工影像与神经工程共 40 个会议。

## 功能

- 所有会议下一届投稿截止的**实时倒计时**,按「即将截稿 / 待公布 / 已截稿」分组
- **摘要与全文双截稿**蓝红两色区分,配每个会议的**时间轴**与"今天"标记;
  多轮会议带轮次标签(*Round 1*、*Cycle 1* 等)
- **一键加日历**——每条截稿支持 Google Calendar 链接和 `.ics` 下载
- **自动更新**——日期每周从 [ccfddl 数据集](https://github.com/ccfddl/ccf-deadlines)
  同步;不在该数据集的会议监视官网,CFP 一变化即标记复核。截稿过后条目进入「待公布」,
  等待下一届公布
- 每张卡片附**会议指标**——CCF 等级、CORE 等级、Google Scholar h5-index
  (会议没有 JCR 影响因子,h5 为通行引用指标)
- **四大主题色 + 分级深浅**——颜色越深代表会议分级越高
- **中英文切换**,过滤条件可分享(`?sub=ML,CV&lang=en`)

## 分类

| 主题 | 颜色 | 方向 | 会议 |
|------|------|------|------|
| 算法 | 🔵 蓝 | `ML` `DM` `NC` | NeurIPS · ICLR · ICML · AAAI · IJCAI · UAI · AISTATS · ACML · KDD · WWW · SIGIR · ECML PKDD · CIKM · ICDM · SDM · PAKDD · IJCNN · ICONIP |
| 视觉·交互 | 🟣 紫 | `CV` `AC` | CVPR · ICCV · ECCV · ACM MM · MM Asia · WACV · BMVC · ICME · ICIP · ACII · ICMI |
| 医疗·信号 | 🟡 黄 | `BME` `SP` | EMBC · BIBM · MICCAI · ISBI · IEEE SMC · ICASSP · EUSIPCO |
| 神经 | 🔴 红 | `BCI` | IEEE NER · International BCI Meeting · SfN · OHBM |

## 数据

纯静态站点,无构建步骤。所有数据在 [`data/conferences.yml`](data/conferences.yml),
改完 YAML 即生效。标注「预估」的日期为按往年规律推测,以官网 CFP 为准。
期刊(TPAMI / TNNLS / JNE / TNSRE 等)为滚动投稿,不收录。欢迎 PR 修正日期。

```bash
# 本地预览
python3 -m http.server 8000   # 打开 http://localhost:8000
```

## License

MIT
