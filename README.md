# human-novel-writer

AI 长篇小说（网文/番茄风）全流程写作工作流 Skill，**v2.0（2026-08-14）**。适用于 ZCode、Claude Code 等支持 open SKILL.md 格式的 agent。

## v2.0 更新说明（2026-08-14）

v2.0 将 **oh-story-claudecode**（13 个网文 skill）与 **writing-dna-skill**（文风蒸馏）的可迁移能力全部并入本 skill，成为单一自包含写作引擎：

**新增能力**
- **拆文对标**：短篇/长篇拆解管道（`拆文库/{书名}/`），把爆款书拆成 剧情/节奏.md、情绪模块.md、文风.md 等对标资产；番茄题材可先用 NOVELCATCH 黄金三章拆解报告做预对标参考
- **题材库**：32 张长篇题材卡 + 10 个短篇风格包 + 题材公式（21 大公式）+ 核心梗与读者心理
- **选题（静态+NOVELCATCH 数据）**：选题四步（推荐写什么/为什么能爆/行不行/怎么验证）+ 9 维读者画像 + 平台指南；数据源 NOVELCATCH（https://novelcatch.com，番茄每日榜单/黑马/情报/赛道对比，agent 可 WebFetch 读取，样本≥15 可给"高"）；无数据时可行性最高给"中"
- **写作技法层**（`references/网文技法/`）：钩子库（章首 7 式/章尾 13 式）、爽点情绪工程（爽点六类型/高潮蓄能公式/六种情绪弧线）、读者契约（终局储备/主角代理权）、大纲结构理论（八节点/章节张弛/黄金三章）、反转工具箱、对话技法、正文技法
- **四视角审稿**：架构师/人物/叙事/一致性四视角 + 番茄/起点/知乎平台 rubric（S1/S2/S3 分级）
- **封面生成**（foxtrai 版）：题材→视觉风格映射 + 三层提示词，执行走 foxtrai 生图 API（依赖 foxtrai-生图 skill）
- **文风蒸馏**：writing-dna 六层蒸馏（语言 DNA/结构模板/认知框架/视觉风格 → Writing-DNA.md），产物落 `文风库/{作者}/`

**规则调整**
- **技法优先（试验期）**：网文技法层优先于风格/文戏类写作红线（文戏功能重复、展示而非告知、短句节制、视角受限）；内容边界类红线保留（无阴谋论、无死亡威胁、角色人设查证、新设定查重、战力自洽）
- **去 AI 味双门禁调整**：朱雀密度红线降为提示级（技法优先期），翻案腔/黑话/模型路标硬项仍必修；删除重写制触发加人工确认
- **章节合同升级**：11 问 + 3 行生产要素（情节点字数预算 / 章尾钩子类型 / 复沓锚句）
- 外挂 skill（qu-ai-wei、remove-ai-flavor）已删除——其 51 类矩阵与模板壳内容已蒸馏进 `references/anti-ai-rules.md`

## 能力覆盖

- **项目目录搭建**：一键复制 `assets/项目骨架/`（16 文件模板，含 4 个总控文件）即成新书骨架
- **三总控文件**：项目状态（单点事实源）/ 开书定位 / 核心设定
- **人物卡 9 要素**：公开目标 / 私下欲望 / 当前利益 / 害怕失去 / 底线与缺陷 / 资源与权限 / 利益冲突 / 语言指纹 / 重大刺激反应
- **大纲三件套**：全书大纲 / 分卷大纲 / 滚动细纲（只细化接下来 5-12 章；每章含 11 问 + 3 行生产要素）
- **追踪四件套**：时间线 / 角色状态 / 伏笔 / 资源与权限
- **每章 8 步循环**：LOAD → CHECK → CONTRACT → DRAFT → REVIEW → REVISE → UPDATE → DECIDE（用户裁决才算完成）
- **去 AI 味三轨**：`anti-ai-rules.md`（朱雀画像/句式指纹/删除重写制）+ `human-writing-*.md`（活人感规则）+ `网文技法/去AI味/`（oh-story 三遍法补充）；双门禁量化（density_check 提示级 / check_prose 硬项必修）
- **网文技法知识层**：见上"v2.0 更新说明"，入口 `references/网文技法/INDEX.md`（按需加载，不预占上下文）

## 目录结构

```
human-novel-writer/
├── SKILL.md                    ← 工作流总入口（决策树/8步循环/硬规则/技法优先声明）
├── assets/项目骨架/            ← 新书项目模板（16 文件：4 总控 + 人物/大纲/追踪/正文/待确认）
├── references/
│   ├── anti-ai-rules.md        ← 去 AI 味完整规则（密度量化红线/删除重写制/51类矩阵蒸馏）
│   ├── human-writing-*.md      ← 活人感写作（叙述位置/第一稿/成稿硬禁/七遍改稿）
│   └── 网文技法/               ← v2.0 知识层（INDEX.md 索引）
│       ├── 拆文对标/           ← 短篇/长篇拆解 + 11 份标尺
│       ├── 题材库/             ← 32 长篇题材卡 + 10 短篇风格包 + 选题/（静态选题）
│       ├── 钩子库/ 爽点情绪/ 读者契约/ 大纲结构/ 反转对话/ 正文技法/
│       ├── 审稿/               ← 四视角审稿 + 平台 rubric
│       ├── 封面/               ← foxtrai 版封面生成
│       ├── 文风蒸馏/           ← writing-dna 六层 + 产物模板
│       └── 去AI味/             ← oh-story anti-ai-writing/banned-words（补充）
└── scripts/
    ├── density_check.py        ← 朱雀密度红线检查器（技法优先期=提示级）
    └── check_prose.py          ← 翻案/黑话/路标硬项 + 说话人归属提示
```

## 使用方式

把本目录放入 agent 的 skills 目录（如 `~/.zcode/skills/`），然后：

- 写新书：`搭小说项目` → 自动复制项目骨架
- 写章节：agent 按"每章 8 步循环"执行，章末跑双门禁脚本
- 拆文对标：`拆这本书` → 拆文库/{书名}/ → 日更时自动对标（番茄题材可先看 NOVELCATCH 预对标）
- 选题数据：`帮我选题` → 自动读 NOVELCATCH 榜单（或你粘贴数据）→ 选题四步跑数据模式
- 选题：`帮我选题` → 选题四步（静态，无榜单时给"中"）
- 审稿：`审一下` → 四视角审稿
- 封面：`做个封面` → foxtrai 生成
- 蒸馏文风：`蒸馏XX作者的文风` → 文风库/{作者}/
- 去 AI 味：按 `references/anti-ai-rules.md` 全量自查 + 双门禁

## 致谢与协议

- 活人感写作规则整合自 [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing)（v1.1.0，MIT），已在本地做小说例外适配与扩展
- 网文技法层整合自 [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)（v0.7.6，MIT）——拆文/题材库/钩子/爽点/契约/审稿/封面方法论，已做去工程化改写（无 agents/hooks/scripts 依赖）
- 文风蒸馏整合自 [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill)（MIT）——六层蒸馏方法论与产物模板
- 本仓库 MIT License。
