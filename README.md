# 申论提分教练 · Shenlun Score Coach

> 手写申论拍照即批。不只告诉你扣了几分，而是讲清这道题该怎么想、为什么这么答、下次怎么提高。

![license](https://img.shields.io/badge/license-MIT-blue)
![platform](https://img.shields.io/badge/WorkBuddy-Skill-orange)
![python](https://img.shields.io/badge/python-3.9%2B-3776AB)

一个 [WorkBuddy](https://www.workbuddy.cn) 技能：把手写的申论答卷照片变成一份**教学复盘报告**——按稿纸格数转写、推算字数、匹配真题采分点，输出「题干解剖 → 材料映射 → 偏差定位 → 关键决策 → 可迁移技巧 → 考场自检 → 参考作答」七段教学。

## 它解决什么问题

市面上的申论批改大多停在"诊断"：丢了几个采分点、扣了几分。
但**知道错了 ≠ 下次会对**——换个材料，同样的坑还会踩。

这个技能把重心从"诊断"移到"教学"，报告主体是三条链：

1. **材料 → 答案的映射链**：材料哪句话 → 什么信号词 → 归到哪个上位概念 → 是否必踩
2. **认知偏差定位**：漏点（没看见）／偏差（看见了想错）／冗余（想多了）——三者练法完全不同
3. **可迁移技巧**：写成「看到 X → 就做 Y」，能带到下一题，不是"要注意表述规范"

## 效果示例

[`examples/sample-report.md`](examples/sample-report.md) 是一份真实使用中生成的完整报告：可以直观看到七段结构、材料映射表、偏差定位和两版参考作答长什么样。

## 快速开始

### 方式一：WorkBuddy 技能市场

在 WorkBuddy 左侧「专家 · 技能 · 连接器」→「技能市场」搜索 **申论提分教练**，点击加号安装。

### 方式二：手动安装

```bash
git clone https://github.com/Double808/shenlun-auto.git
cp -r shenlun-auto ~/.workbuddy/skills/
```

Windows 下把整个 `shenlun-auto` 文件夹复制到 `C:\Users\<你的用户名>\.workbuddy\skills\`，重启 WorkBuddy 生效。

### 使用

1. 拍三样：**题干页、材料页、手写作答页**（多页可一次发，不用按顺序）
2. 发进对话，说「批改」或直接发图
3. 得到：七段教学复盘 + 手写答案转写稿（供核对）+ 两版参考作答 + 错题库更新

> 想让"为什么"讲得准，**材料页一定要拍全**——教学的核心是"材料哪句→怎么概括"，看不到材料就只剩答案点评。

## 报告结构

```
识别与假设       每题开头，自动补全项全部显式标注（分值/字数/真题来源）
手写答案转写     忠实转写，不润色；存疑字原位标〔候选?〕，供你核对
① 题干解剖      审题 60 秒：题型/要素/范围/字数/命题意图，每项带依据
② 材料→答案映射  核心表格：材料原文 | 识别信号 | 上位概括 | 必踩与否
③ 偏差定位      漏点型/偏差型/冗余型，各给"你当时的思路 vs 正确思路"
④ 三处关键决策   为什么这里分条、为什么用这个词、为什么合并——每处给判据
⑤ 可迁移技巧     「看到 X → 就做 Y」格式
⑥ 考场自检清单   答完 60 秒能过一遍的 5 条
⑦ 参考作答+分数  分数放最后，作参照而非结论
```

整卷批改时，每题给精简版，另挑 1–2 道最值得深挖的给完整七段。

## 核心能力

| 能力 | 说明 |
|---|---|
| 手写格纸转写 | 按 25 格/行逐格对应，而非按行粗读；转写结果忠实写入报告供核对 |
| 字数按格推算 | 手写连笔会导致字符数系统性偏低，用格数推算才不会冤判"字数不足" |
| 涂改分级处理 | 划线删除／涂黑覆盖／旁注补充，三类处理规则不同 |
| 真题匹配 | 联网检索 + 本地真题库双通道，命中即以真题采分点为基准，并区分"精确命中/同源材料" |
| 双视角参考作答 | 小马哥版（结构固定、要素融合）／白鹭版（结构随题干、要素分栏），两版必须结构不同 |
| 大作文定档 | 袁东累进四类文，强制先判单/双/多主题 → AB/ABC 型 |
| 错题库累积 | 按**认知偏差**而非失分点记录，跨题累积成能力曲线，≥2 次自动复发提醒 |

## 字数推算脚本

`scripts/count_grid.py` 是纯标准库实现的稿纸字数 CLI（Python 3.9+），也可以单独用：

```bash
# 逐行占格（25 格稿纸，9 整行 + 末行 19 格），限制 250 字，附转写字符数做双通道校验
python scripts/count_grid.py --cols 25 --lines 25,25,25,25,25,25,25,25,25,19 --limit 250 --chars 240

# 按行数简写
python scripts/count_grid.py --cols 25 --rows 9.8 --limit 250 --json
```

输出包含：稿纸占格数、满行/未满行统计、双通道偏差判读、超限判定。

## 仓库结构

```
shenlun-auto/
├── SKILL.md                          技能主控流程（7 步流水线）
├── README.md                         本文件
├── CHANGELOG.md                      更新日志
├── NOTICE.md                         第三方内容与授权说明
├── LICENSE                           MIT
├── examples/
│   └── sample-report.md              完整报告示例
├── references/                       参考库（平台要求 ≤ 两级目录，已扁平化）
│   ├── teaching-report-spec.md       教学报告七段结构（默认）
│   ├── auto-report-spec.md           诊断报告八段结构（降级）
│   ├── handwriting-grid-reading.md   手写格纸识读细则
│   ├── scoring-rules.md              评分方法与格式模板
│   ├── writing-rules.md              作答铁律
│   ├── error-bank-rules.md           错题库分类与记录规则
│   ├── expression-upgrade-rules.md   表述升级替换表
│   ├── image-reading-rules.md        图片识读规范
│   ├── router.md                     总调度：真题识别、错题库、命题预判
│   ├── xiaoti.md                     小题批改流程
│   ├── dawenti.md                    大作文批改流程
│   ├── bai-lu-methodology.md         白鹭方法论（小题）
│   ├── xiaoma-methodology.md         小马哥方法论（小题）
│   ├── yuan-dong-methodology.md      袁东方法论（大作文）
│   ├── prediction-methodology.md     命题预判方法
│   ├── fallback-eval-rules.md        无题干兜底评改
│   ├── exam-index.md                 真题库索引
│   ├── exam-template.md              真题入库模板
│   └── exam-*.md                     真题样本（4 套）
└── scripts/
    └── count_grid.py                 稿纸字数推算 CLI
```

> 平台限制技能包最多两级目录（`根/二级/文件`），因此上游模块的嵌套 `references/` 已全部拍平到一层，真题库文件统一加 `exam-` 前缀。

## 数据存放与隐私

- 批改报告写入工作区 `申论批改/`，错题库写入 `错题库/`，**均不在技能包内**，升级或重装不会覆盖历史记录
- 本仓库 `.gitignore` 已排除这两个目录，避免个人作答被误提交
- 批改过程只做真题检索的联网查询；你的作答与报告只保存在本地

## 已知限制

- 手写识读依赖多模态模型的视觉能力，字迹潦草时会有个别字误识；误识处列入「待复核」区，**不计入评分**
- 分值、字数限制若未拍进画面，会按题型默认值补齐，并在报告中标注为假设
- 未匹配到真题时，采分点为现场拆解，报告会明确标注
- 输出为学习辅助建议，**不构成任何考试承诺或评分权威**；实际成绩以官方阅卷为准

## 授权与致谢

- 本仓库原创部分（SKILL.md、报告模板、识读细则、脚本等）采用 **MIT** 授权，见 [LICENSE](LICENSE)
- `references/` 下的方法论库来自开源项目 [coffe-d/Shenlun.skill](https://github.com/coffe-d/Shenlun.skill)（MIT）；白鹭、小马哥、袁东的方法论思想权利归原讲授者所有
- 完整来源、改动说明与授权边界见 [NOTICE.md](NOTICE.md)

## 贡献

欢迎 Issue 与 PR。两条硬约束：

1. 方法论库中标注 ❌ 已证伪的条目**不得**用于批改逻辑
2. 修改 `SKILL.md` 的 frontmatter 后，`version` 必须递增（WorkBuddy 平台按版本号校验更新）

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)。
