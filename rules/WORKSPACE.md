# WORKSPACE.md - 目录路由速查

目标：让 AI 每轮 session 都能快速知道"去哪里找/放什么"。**找任何文件前先查这里。**

## 路由规则

### 项目与代码
- 写代码 / 跑脚本 / 一次性项目：`adhoc_jobs/<project>/`
- 工具脚本（邮件、语义搜索、分享报告等）：`tools/`
- 定时任务：`periodic_jobs/`

### 知识与记录
- 通用调研报告：`contexts/survey_sessions/`
- **芯片 / 加速器 internals**（编译器 IR、NEFF、runtime、PTX/SASS 等）：先读 `rules/skills/reference_crucible_notes.md`，再查 survey 报告或启动调研
- 已有芯片产品层调研：`contexts/survey_sessions/*_survey_*.md`（2026-06 批次含 NVIDIA/AMD/AWS Neuron/Google TPU/Meta MTIA/昇腾/寒武纪/壁仞/燧原/昆仑芯/摩尔线程/天数智芯/沐曦/Graphcore/Cerebras/Groq/SambaNova 等 17 家；架构图 `contexts/survey_sessions/assets/`）
- AI 行业周报：`contexts/survey_sessions/ai_briefing_*.md`
- 思考 / 复盘 / 方法论：`contexts/thought_review/`
- 每日日志：`contexts/daily_records/`

### 系统与规则
- 可复用技术方案 / Skill：`rules/skills/`
- 核心公理（Axioms）：`rules/axioms/`
- 记忆系统：`contexts/memory/` + `periodic_jobs/ai_heartbeat/`
  - Observer（每日）/ Reflector（每周）：`src/v0/observer.py`、`reflector.py`；SOP 见 `docs/KNOWLEDGE_BASE.md`
  - 双引擎：`src/v0/agent_client.py`，`HEARTBEAT_ENGINE=cursor|opencode`（默认 cursor）；配置见根目录 `.env.example`
  - Cursor 引擎：`cursor_client.py`（`agent create-chat` + `-p --resume`）；prompt 落盘 `.cursor_tmp/heartbeat/`
  - OpenCode 引擎：`opencode_client.py`（需 `OPENCODE_BASE_URL` server）

## 命名规则
- 目录和文件名：小写 + 下划线 (snake_case)
- 临时一次性项目：`tmp_<name>/`

## Python 环境
- 根目录 `.venv/` 为工作区级环境，用 `uv pip install` 管理依赖
- 需要隔离时在 `adhoc_jobs/<project>/.venv/` 建独立环境

## 快速查询

<!-- 随着你的项目增长，在这里添加活跃项目的快捷路由 -->
<!-- 格式：- `project-name` → `adhoc_jobs/project_name/` (说明) -->
