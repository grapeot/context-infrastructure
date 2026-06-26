# Memory Observations

这是三层记忆系统的 L1/L2 层。每日观察由 `periodic_jobs/ai_heartbeat/src/v0/observer.py` 自动写入，每周由 `reflector.py` 整理和蒸馏。

## 格式说明

每个日期条目格式如下：

```
Date: YYYY-MM-DD

🔴 High: [方法论/约束] 描述
🟡 Medium: [项目状态/决策] 描述
🟢 Low: [任务流水] 描述
```

### 优先级定义

- **🔴 High**：跨项目通用的经验教训、硬性约束、影响系统架构的重大决策。永久保留，候选晋升为 axiom 或 skill。
- **🟡 Medium**：活跃项目的关键进展、技术决策背景、未来几周仍需参考的信息。
- **🟢 Low**：日常任务流水、瞬时 debug 记录、临时上下文。定期垃圾回收。

## 如何加载记忆

不要全文加载这个文件（可能很大）。按需检索：

```bash
# 搜索特定主题
grep -n "关键词" contexts/memory/OBSERVATIONS.md

# 搜索最近 N 天
grep -A 20 "Date: $(date -v-7d +%Y-%m-%d)" contexts/memory/OBSERVATIONS.md
```

或使用语义搜索（`rules/skills/semantic_search.md`）做跨日期语义检索。

---

<!-- 以下是记录区域，由 observer.py 自动追加 -->
<!-- L2 Reflector GC: 2026-06-27 — 芯片双层路由、Heartbeat 双引擎、survey 批次路由、Cursor skills 索引已晋升至 rules/ -->

Date: 2026-06-27

🔴 High: [Heartbeat 双引擎] `periodic_jobs/ai_heartbeat/src/v0/agent_client.py` 统一 Cursor/OpenCode 抽象；`HEARTBEAT_ENGINE=cursor|opencode`（默认 cursor），Cursor 路径经 `cursor_client.py` 用 `agent -p` 驱动，prompt 落盘 `.cursor_tmp/heartbeat/`。
🔴 High: [芯片调研路由] internals 层先读 `rules/skills/reference_crucible_notes.md`；产品/代际层走 `rules/skills/workflow_deep_research_survey.md` 输出至 `contexts/survey_sessions/`（已晋升 `rules/WORKSPACE.md` 与 `AGENTS.md`）。
🔴 High: [Observer 扫描] 根目录含嵌套独立 git 仓库，不可依赖全局 git diff；优先 `find`/`ls` 按 mtime 扫描，`contexts/blog/` 须读 Markdown `Date` 头校验，`contexts/daily_records/` 黑名单忽略。
🟡 Medium: [芯片 survey 批次] 2026-06-26 完成 16 份 `contexts/survey_sessions/*_survey_20260626.md`（NVIDIA/AMD/AWS Neuron/Google TPU/Meta MTIA/昇腾/壁仞/燧原/昆仑芯/摩尔线程/天数智芯/沐曦/Graphcore/Cerebras/Groq/SambaNova）及 `contexts/survey_sessions/assets/` 架构图。
🟡 Medium: [AI 简报] `contexts/survey_sessions/ai_briefing_20260626.md` Vol.1 发布，覆盖美国政府介入模型发布、OpenAI Jalapeño 推理芯片、DeepSeek 74 亿美元 A 轮等。
🟡 Medium: [Cursor skills 导入] `adhoc_jobs/import_awesome_cursor_skills/import_skills.py` 从 awesome-cursor-skills 批量导入约 98 个 skill 至 `rules/skills/`，索引见 `rules/skills/INDEX.md` Cursor Skills 节。
🟡 Medium: [Heartbeat 脚本重构] `periodic_jobs/ai_heartbeat/src/v0/observer.py`、`reflector.py`、`jobs/crontab_monitor.py` 均改用 `agent_client.add_engine_args()` / `get_client()`，硬编码 workspace 路径已替换为 `WORKSPACE_ROOT`。
🟢 Low: [L2 Reflector GC] 今日执行垃圾回收，`contexts/memory/OBSERVATIONS.md` 历史条目已清空；芯片双层路由、Heartbeat 双引擎、survey 批次路由、Cursor skills 索引已固化进 `rules/`。
🟢 Low: [配置] `.env.example` 增补 `HEARTBEAT_ENGINE`、`CURSOR_AGENT_MODEL`、`CURSOR_AGENT_TIMEOUT`、`OPENCODE_BASE_URL` 等 Heartbeat 相关变量。
🟢 Low: [文档] `rules/skills/ai_agent_cli_guide.md` 新增 Cursor Agent CLI 章节并与 OpenCode 选型对照表（2026-06-27 更新）。

