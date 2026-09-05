# AGENTS.md - Your Workspace

> **First time here?** Start with `setup_guide.md` — it'll walk you through setup in under an hour.

This folder is home. Treat it that way.

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` — this is who you are
2. Read `rules/USER.md` — this is who you're helping
3. Read `rules/WORKSPACE.md` — file routing table, check before searching for files
4. Read `rules/COMMUNICATION.md` — how to think and communicate (especially for non-coding tasks)
5. Read `rules/skills/INDEX.md` — understand available skills

## Multi-Agent Nudge

This harness can delegate work to multiple sub-agents. You don't need to use them by default, but keep the capability in mind for tasks that are large, parallelizable, research-heavy, or benefit from independent cross-checking.

Before using sub-agents, read `rules/skills/workflow_parallel_subagents.md`. The current OpenCode pattern is `multi_tool_use.parallel` wrapping multiple `functions.task` calls in the same assistant message.

Don't ask permission. Just do it.

## File Routing

**找文件时，先查 `rules/WORKSPACE.md`，再搜索。** WORKSPACE.md 是这个 workspace 的目录索引，记录了每类内容的存放位置。绝大多数情况下查一下就能定位到目标目录，不需要全盘 glob/grep。如果发现新目录或项目没被收录，顺手更新 WORKSPACE.md。

## Skills

**Skills** 是 AI 可复用的能力，包括工作流、API 指南、最佳实践等。

**重要：遇到"怎么做 X"时，先查 skill 再查系统工具。** 搜索顺序：(1) 下方速查表 → (2) `rules/skills/INDEX.md` → (3) 系统工具。

**需要执行某项任务** → 先查 `rules/skills/INDEX.md` 找到对应的 skill
**想添加新能力** → 参考现有 skill 格式，更新 INDEX.md

### 常用 Skill 速查（以 INDEX.md 为准）

**深度调研任务** → `rules/skills/workflow_deep_research_survey.md`
**调用后台 Agent / 并行 Subagent** → `rules/skills/workflow_parallel_subagents.md`

命中后读对应 skill 文件再执行；INDEX.md 是唯一路由源，这里不展开步骤。

## Axioms（公理）

从个人经历提炼的决策原则，用于启发深度思考。分类索引、使用指南和触发词见 `rules/axioms/INDEX.md`。

## Sub-agent 模型路由

配置入口：OpenCode 原生 `opencode.json` 的 `agent` 字段，或 `.opencode/agent(s)/*.md` agent 文件。`subagent_type` 必须是已注册 agent 名，不是模型名，也不是旧 `category`。

常用路由速查：
- **代码库探索** → `subagent_type="explore"`
- **通用并行任务** → `subagent_type="general"`
- **高可靠推理 / 工程判断** → `subagent_type="reasoning_gpt"`
- **中文写作 / 改稿** → `subagent_type="writer_deepseek"`
- **低成本初筛 / 轻量整理** → `subagent_type="cheap_glm"`
- **本地隐私敏感任务** → `subagent_type="private_ds4"`
- **Ollama Cloud zero-data-retention 低成本任务** → `subagent_type="ollama_kimi"`
- **Ollama Cloud zero-data-retention 高质量任务** → `subagent_type="ollama_deepseek_pro"`

创意性工作（brainstorm、文章结构、观点碰撞）默认并行派一个不同路线的 subagent 做反向视角或补充视角。不要使用旧的 `category="artistry"` / `category="deep"` / `category="ultrabrain"` 写法，除非当前 OpenCode 配置已经显式注册了这些同名 agent。

## Opus 工作模式

如果你的模型 ID 包含 `opus`，以下规则生效：

**你的 context window 很宝贵。** Opus 的核心能力是设计、质量把关和写作。调研、写脚本、关键词检索这些事交给 sub-agent。你的两个主要任务：（1）**设计**：拆分问题、设计计划、分配 sub-agent 任务；（2）**写作与质量把关**：最终文本自己写，sub-agent 结果自己验证。写代码、调研、数据处理全部 delegate，写作和质量验证绝不外包。设计任务拆分时默认考虑并行性，具体执行方式以 `rules/skills/workflow_parallel_subagents.md` 为准。

## Memory System（记忆系统）

三层记忆架构：
- **L3（全局约束）**：`rules/` 下的所有文件，每次 session 被动加载
- **L1/L2（动态记忆）**：`contexts/memory/OBSERVATIONS.md`，agent 主动检索
- **自动积累**：`periodic_jobs/ai_heartbeat/` 每日 observer + 每周 reflector

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
