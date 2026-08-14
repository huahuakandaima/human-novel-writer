# 网文技法知识库索引

> 本目录是 oh-story-claudecode（13 个 skill）+ writing-dna-skill 的可迁移能力，整合进 human-novel-writer 的知识层。
> 整合日期：2026-08-14。来源仓库：`worldwonderer/oh-story-claudecode`、`larashero3-dotcom/writing-dna-skill`。
> 使用原则：**按需加载，不预占上下文**——写对应环节前再读对应文件。

## 目录

| 模块 | 文件 | 何时读 |
|---|---|---|
| 拆文对标 | `拆文对标/短篇拆文.md`、`长篇拆文.md` | 用户要拆爆款书/对标书时（番茄题材可先查 NOVELCATCH https://novelcatch.com/dissect 做预对标参考） |
| 拆文标尺 | `拆文对标/标尺/`（material-decomposition / output-templates / deconstruction-notes / style-profile-generator / style-profile-protocol / deconstruction-examples / zhihu-style / genre-writing-techniques / real-market-data / output-contract / cross-book-recall） | 拆文过程中按 Stage 需求读取 |
| 题材库 | `题材库/题材索引.md`（题材总览）、`题材公式.md`（21 大题材写作公式）、`核心梗与读者.md`（核心梗+读者心理）、`short-craft.md`（短篇通用底座）、`short-format.md`（短篇格式）、`short-deslop.md`（短篇去AI味）、原文件名版：genre-catalog / genre-core-mechanics / genre-readers / genre-writing-formulas | 开书选材/写指定题材/写短篇时 |
| 选题（静态+数据） | `题材库/选题/选题四步.md`（推荐写什么/为什么能爆/行不行/怎么验证）、`读者画像.md`（9 维）、`题材趋势.md`（静态候选假设）、`平台指南.md`（运营+书名简介） | 用户说"帮我选题/写什么能爆"时；**数据源：NOVELCATCH**（https://novelcatch.com，番茄每日榜单/黑马/情报/赛道对比，agent 可 WebFetch 读取，样本≥15 可给"高"）；无数据时可行性最高给"中" |
| 长篇题材卡 | `题材库/长篇题材卡/{题材}.md`（32 张） | 写对应题材的长篇正文时 |
| 短篇风格包 | `题材库/短篇风格包/{题材}.md`（10 个） | 写对应题材的短篇时 |
| 钩子库 | `钩子库/hooks-chapter.md`（章首7式/章尾13式）、`hooks-paragraph.md`、`hooks-suspense.md` | 设计章首/章尾钩子、悬念时 |
| 爽点情绪 | `爽点情绪/plot-emotion-system.md`（爽点六类型/倒推法）、`plot-core-methods.md`（高潮公式）、`emotional-methods.md`、`emotional-arc-design.md`（六种情绪弧线）、`style-combat-face.md`（打斗/装逼） | 设计爽点/高潮/情绪节奏时 |
| 读者契约 | `读者契约/reader-contract-and-progression.md`（终局储备/升级台阶/主角代理权/契约三分级） | 全书规划、防「写无可写」时 |
| 大纲结构 | `大纲结构/outline-methods.md`（八节点）、`outline-structure-theory.md`（章节定位与张弛）、`opening-design.md`（黄金三章） | 搭全书大纲/细化纲时 |
| 反转对话 | `反转对话/reversal-toolkit.md`、`villain-and-reveal.md`（短篇反派/揭露）、`dialogue-mastery.md` | 设计反转/反派/对话时 |
| 正文技法 | `正文技法/writing-craft.md`（正文写作技法）、`format-and-structure.md`（正文格式规范）、`writing-workflow.md`（短篇设计+精修工作流） | 写正文技法细节、格式规范时 |
| 去AI味（补充） | `去AI味/anti-ai-writing.md`（AI 指纹识别+三遍法+改写范例库）、`banned-words.md`（禁用词与句式表） | 与主文件 anti-ai-rules.md 三轨互补；拆文报告/审稿/正文自查时按需读 |
| 审稿 | `审稿/四视角审稿.md`（主流程）、`quality-rubric.md`、`quality-checklist.md`、`rubrics/{fanqie,qidian,zhihu}.md` | 用户说「审一下/审查」时 |
| 封面 | `封面/封面生成.md`（foxtrai 版流程）、`cover-styles.md`（题材→视觉风格映射） | 用户要封面图时 |
| 文风蒸馏 | `文风蒸馏/蒸馏方法论.md`、`模板/`（六层产物模板） | 用户要蒸馏某作者/某书文风时 |

## 来源文件对应表（升级 oh-story 时同步用）

| 本目录文件 | 上游源文件 |
|---|---|
| 拆文对标/短篇拆文.md、长篇拆文.md | story-short-analyze / story-long-analyze SKILL.md（去工程化改写） |
| 拆文对标/标尺/* | story-short-analyze + story-long-analyze references/（原文件名保留） |
| 题材库/长篇题材卡/* | story-long-write/references/genre-prose-cards/ |
| 题材库/短篇风格包/* | story-short-write/references/genre-styles/ |
| 题材库/题材公式.md | story-long-write/references/genre-writing-formulas.md |
| 题材库/题材索引.md | story-long-write/references/genre-catalog.md（摘要版） |
| 题材库/核心梗与读者.md | genre-core-mechanics.md + genre-readers.md（合并） |
| 题材库/short-craft.md、short-format.md、short-deslop.md | story-short-write/references/ 同名文件 |
| 题材库/genre-*.md（原文件名） | story-long-write/references/ 同名文件（供内部引用解析） |
| 钩子库/* | story-long-write/references/hooks-*.md |
| 爽点情绪/* | story-long-write/references/{plot-emotion-system,plot-core-methods,emotional-methods,emotional-arc-design,style-combat-face}.md |
| 读者契约/* | story-long-write/references/reader-contract-and-progression.md |
| 大纲结构/* | story-long-write/references/{outline-methods,outline-structure-theory,opening-design}.md |
| 反转对话/* | story-long-write/references/{reversal-toolkit,dialogue-mastery}.md + story-short-write/references/villain-and-reveal.md |
| 正文技法/* | story-long-write/references/{writing-craft,format-and-structure}.md + story-short-write/references/writing-workflow.md |
| 去AI味/* | story-long-write/references/{anti-ai-writing,banned-words}.md（与主文件 anti-ai-rules.md 互补） |
| 审稿/* | story-review/references/{quality-rubric,quality-checklist,rubrics/*}.md + SKILL.md（solo 改写） |
| 封面/* | story-cover/SKILL.md（foxtrai 改写）+ references/cover-styles.md |
| 文风蒸馏/* | writing-dna-skill/SKILL.md + templates/author-corpus/zh/ |

## 同步升级说明

oh-story 或 writing-dna-skill 上游更新时：
1. 题材卡/风格包/技法库文件：直接覆盖同名文件（上游原样，无改写）
2. 拆文/审稿/封面/蒸馏主文件：按「来源文件对应表」重读上游 SKILL.md，人工同步改写版
3. 标尺文件保留上游原文件名，勿改回中文名（上游内部互相引用依赖原文件名）
4. 更新本文件的整合日期与来源版本
