# human-novel-writer

AI 长篇小说（网文/番茄风）全流程写作工作流 Skill。适用于 ZCode、Claude Code 等支持 open SKILL.md 格式的 agent。

## 能力覆盖

- **项目目录搭建**：一键复制 `assets/项目骨架/`（16 文件模板）即成新书骨架
- **三总控文件**：项目状态（单点事实源）/ 开书定位 / 核心设定
- **人物卡 9 要素**：公开目标 / 私下欲望 / 当前利益 / 害怕失去 / 底线与缺陷 / 资源与权限 / 利益冲突 / 语言指纹 / 重大刺激反应
- **大纲三件套**：全书大纲 / 分卷大纲 / 滚动细纲（只细化接下来 5-12 章）
- **追踪四件套**：时间线 / 角色状态 / 伏笔 / 资源与权限
- **章节合同 11 问**：写正文前回答 11 个问题（答不出"推进剧情"就退回细纲）
- **每章 8 步循环**：LOAD → CHECK → CONTRACT → DRAFT → REVIEW → REVISE → UPDATE → DECIDE（用户裁决才算完成）
- **去 AI 味三轨**：
  - `references/anti-ai-rules.md`：朱雀检测器实战画像、句式指纹、密度量化红线、代词三法、时代认知边界、删除重写制、普通人视角铁则、解释层禁令
  - `references/human-writing-*.md`：整合自 [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing)（1.1.0）的活人感规则（说话位置 / 第一稿 / 成稿硬禁 / 七遍改稿），含小说例外适配
  - 外挂 skill：`qu-ai-wei`（51 类减法矩阵）、`remove-ai-flavor`（模板壳专项）
- **双门禁量化**：`scripts/density_check.py`（朱雀密度红线一键量化）+ `scripts/check_prose.py`（翻案腔/黑话/路标 + 对话归属提示），FAIL 必修

## 目录结构

```
human-novel-writer/
├── SKILL.md                    ← 工作流总入口（决策树/8步循环/硬规则）
├── assets/项目骨架/            ← 新书项目模板（16 文件，复制改名即用）
├── references/
│   ├── anti-ai-rules.md        ← 去 AI 味完整规则（密度量化红线/删除重写制等）
│   ├── human-writing-style.md  ← 活人感整合说明（叙述位置/第一稿/成稿硬禁）
│   ├── human-writing-fiction.md    ← 虚构写作专文（人物/场景/对白/设定/视角/结尾）
│   ├── human-writing-revision.md   ← 七遍改稿（初稿后读）
│   ├── human-writing-formats.md    ← 不同文体形式差异
│   ├── human-writing-forum-prose.md← 论坛长帖体
│   ├── human-writing-reality.md    ← 非虚构核验
│   └── human-writing-lite.md       ← 活人感规则速览
└── scripts/
    ├── density_check.py        ← 朱雀密度红线检查器（退出码 0=通过）
    └── check_prose.py          ← 翻案/黑话/路标 + 说话人归属提示
```

## 使用方式

把本目录放入 agent 的 skills 目录（如 `~/.zcode/skills/`），然后：

- 写新书：`搭小说项目` → 自动复制项目骨架
- 写章节：agent 按"每章 8 步循环"执行，章末跑双门禁脚本
- 去 AI 味：按 `references/anti-ai-rules.md` 全量自查 + 双门禁量化

## 致谢与协议

- 活人感写作规则整合自 [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing)（v1.1.0，MIT），已在本地做小说例外适配与扩展（说话人归属 S1 规则、对话归属提示等）。
- 本仓库 MIT License。
