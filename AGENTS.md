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

调用 sub-agent 或独立审阅载体前，先读 `rules/skills/workflow_parallel_subagents.md`。

- **工程与代码实现**：默认主线程亲自完成，仅用户明确要求委派实现时才分派。
- **Code / privacy / design review**：通常交独立 sub-agent 或 Antigravity CLI 获取 fresh context，主线程最终验收；轻微低风险局部变更可按比例例外。单次 review 不受多路并行门槛限制。

- **广泛调研与代码库探索**：满足并行门槛时可多 sub-agent 并行；同批就绪任务用 `multi_tool_use.parallel` 同消息启动，运行时支持时默认 `background: true`，等自动完成通知，不轮询。

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

只有按 workflow 已决定委派后，才从运行时 schema 选择能力：代码库探索用 `explore`，通用调研用 `general`，专项审阅、编码、初筛与隐私能力使用当前已注册 agent。不维护固定模型或历史别名清单；路由不授予实现委派权限。

Antigravity CLI 是独立外部载体，不等同于 Gemini subagent。用于独立审阅或已选写作 workflow 时，先读已安装的 `ai-agent-cli` 根 skill 与 Antigravity focused skill，按当前可用模型调用。

## Opus 工作模式

如果你的模型 ID 包含 `opus`，以下规则生效：

**实现与最终验收默认留在主线程。** Opus 同样默认亲自实现，仅用户明确要求时才委派实现；广泛调研探索可按需委派，code / privacy / design review 通常交独立载体。已选写作 workflow 可指定 writer，主线程仍须读回核验并承担最终交付责任。调度边界见 `rules/skills/workflow_parallel_subagents.md`。

## Memory System（记忆系统）

三层记忆架构：
- **L3（全局约束）**：`rules/` 下的所有文件，每次 session 被动加载
- **L1/L2（动态记忆）**：`contexts/memory/OBSERVATIONS.md`，agent 主动检索
- **自动积累**：`periodic_jobs/ai_heartbeat/` 每日 observer + 每周 reflector

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- When in doubt, ask.
