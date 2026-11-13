# Crontab 配置指南

本文档描述 context infrastructure 系统所需的定时任务。

---

## 时间线总览

```
3:05 AM   → Situation Awareness: 每日摘要 + 摄像头缓存刷新
4:00 AM   → Session Sync: 导出 AI session 归档
6:30 AM   → WeChat DB Parser: 导出每日消息为 CSV（如适用）
7:00 AM   → Daily Briefing: 生成个人晨报 → Email
8:00 AM   → AI Heartbeat Observer: 扫描文件变动，提取观察写入 OBSERVATIONS.md
Every 2m  → Situation Awareness: 快照采集（交通/摄像头/警报）
Every 12h → Situation Awareness: 风力预警检查
Weekly    → AI Heartbeat Reflector: 合并/提升/清理记忆
Daily     → Crontab Monitor: 健康审计，发现异常则发告警邮件
```

---

## 核心任务说明

### Session Sync（每日）

使用独立的 [ai_session_export](https://github.com/grapeot/ai_session_export)
把 OpenCode、Claude Code、Codex、Antigravity 和 Second Mind 的本地会话增量导出为
统一 Markdown。真实归档应放在私有数据目录并加入 `.gitignore`，不要写进 public repo。

- **建议时间**：每日 4:00 AM
- **输出**：`contexts/ai_sessions/<source>/`
- **可选后处理**：用 semantic-search-skill 刷新私有向量索引
- **搜索入口**：`rules/skills/ai_session_search_archive.md`

### AI Heartbeat Observer（每日）

扫描 workspace 文件变动，提取有价值的观察写入 `contexts/memory/OBSERVATIONS.md`。这是三层记忆系统的"输入端"。

- **脚本**：`periodic_jobs/ai_heartbeat/src/v0/observer.py`
- **依赖**：OpenCode Server API（`OPENCODE_API_URL`）
- **建议时间**：每日 8:00 AM（在 daily briefing 之后）

### AI Heartbeat Reflector（每周）

从 OBSERVATIONS.md 中积累的观察里提炼规则候选，写进 `contexts/memory/RULE_CANDIDATES.md` 等人批阅；cron 里只跑提议阶段，不会改 `rules/`。人在候选文件里勾选 `- [x] 批准` 后，手动运行 `reflector.py --apply` 合入并清理 OBSERVATIONS.md。

- **脚本**：`periodic_jobs/ai_heartbeat/src/v0/reflector.py`（提议）；`reflector.py --apply`（人批阅后合入）
- **依赖**：OpenCode Server API（`OPENCODE_API_URL`）
- **建议时间**：每周日 9:00 AM

### Crontab Monitor（每日）

自主审计所有 crontab 任务的健康状态，发现异常时发送告警邮件。

- **脚本**：`periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py`
- **依赖**：OpenCode Server API、Gmail（`GMAIL_USERNAME` / `GMAIL_APP_PASSWORD`）
- **建议时间**：每日 9:00 AM

### AI News Survey（每日/每周）

调用 AI Agent 生成 AI 行业日报或周报，可发布到 Kit 订阅者或发送个人邮件。

- **脚本**：`periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py`
- **依赖**：OpenCode Server API、Gmail 或 Kit API
- **建议时间**：每日 8:00 AM（日报）或每周一 8:00 AM（周报）

---

## 示例 crontab 配置

将以下内容添加到 `crontab -e`。**使用前请将 `/path/to/your/workspace` 替换为实际路径。**

```cron
# ── 时区说明 ──────────────────────────────────────────────
# 以下时间均为本地时间。如需指定时区，在 crontab 顶部添加：
# TZ=America/Los_Angeles

# AI Heartbeat Observer — 每日 8:00 AM
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# Session Sync — 每日 4:00 AM；先按 ai_session_export README 配置私有输出路径
0 4 * * * cd /path/to/ai_session_export && /path/to/ai_session_export/.venv/bin/python export_sessions.py --base-dir /path/to/your/workspace/contexts/ai_sessions --state-file /path/to/your/workspace/contexts/ai_sessions/.export_state.json >> /tmp/ai_session_sync.log 2>&1

# AI Heartbeat Reflector — 每周日 9:00 AM
0 9 * * 0 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1

# Crontab Monitor — 每日 9:00 AM
0 9 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py >> /tmp/crontab_monitor.log 2>&1

# AI News Survey 日报 — 每日 8:00 AM（发个人邮件）
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode daily >> /tmp/ai_news_survey.log 2>&1

# AI News Survey 周报 — 每周一 8:00 AM（发布到 Kit 订阅者）
0 8 * * 1 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode weekly --publish-to-kit >> /tmp/ai_news_weekly.log 2>&1
```

---

## 注意事项

1. **路径替换**：所有 `/path/to/your/workspace` 必须替换为你的实际绝对路径。
2. **虚拟环境**：脚本依赖 `.venv` 中的 Python 包，确保先运行 `uv pip install -r requirements.txt`（如有）。
3. **环境变量**：cron 环境不会自动加载 `.env`，建议在脚本中显式加载，或在 crontab 中用 `env $(cat .env | xargs)` 注入。
4. **时区**：macOS cron 默认使用系统时区；Linux 服务器建议在 crontab 顶部显式设置 `TZ=`。
5. **日志**：示例中日志写入 `/tmp/`，生产环境建议改为持久化路径（如 `logs/` 目录）。
6. **依赖顺序**：Observer 依赖当天的文件变动，建议在 daily briefing 和 news survey 之后运行（8:30 AM 以后）。
