# Skills Index

本索引指向可复用的 Skills（技能）—— AI 可以调用的工具、流程和最佳实践。

- **想使用某个能力** → 浏览下方分类，找到对应的 skill 文件
- **想添加新 skill** → 参考现有文件格式，添加到对应分类
- **想安装更多工具型能力** → 看 [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)，那里列出可单独安装的 public skill repo

## Multi-Agent 能力提示

当前 harness 支持通过 `multi_tool_use.parallel` 并行派发多个 `functions.task` subagent。不要默认使用，但遇到大型、可并行、调研重、代码库探索重、需要独立交叉验证的任务时，应先读 [并行 Subagent 工作流](./workflow_parallel_subagents.md)。

快速判断：subagent 适合并行读、独立探索、反方审稿、事实核查和上下文窗口隔离；不适合单点小任务、强顺序依赖任务，以及多个 agent 同时写同一份状态或同一批文件。

---

## 组件状态

### Tier 1: 核心（clone 后即可开始）
- ✅ Rules 框架（SOUL/USER/COMMUNICATION/WORKSPACE）— 填写即用
- ✅ Skills 框架（本目录）— 填写即用
- ✅ 三层记忆系统 — 需配置 OpenCode + cron

### Tier 2: 扩展（需要额外配置）
- ⚙️ Semantic Search — 需要 LLM Studio 或 OpenAI API
- ⚙️ Share Report — 需要 SSH 服务器或 GitHub Pages
- ⚙️ Delayed Execution — starter fallback；durable/AI 延时任务安装 Process Launcher + OpenCode Skill

### Tier 3: 独立 public skill repos（按需安装）
- 🔧 AI Session Export、ChatGPT/Codex OAuth、AI Agent CLI、图片生成、Tavily、Google Docs、Google Maps、Outlook、Resend、OpenCode、Process Launcher、PPTX、Typefully、Circle Post、Stripe、Firewalla、Smart Home 等能力见 [`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)

### 说明
✅ = 最多 15 分钟即可使用
⚙️ = 需要额外配置，不配不影响核心功能
🔧 = 独立 repo，按需安装到你的 workspace

---

## 分类索引

### API Guide（API 指南）

调用外部系统或工具的操作手册。

- [AI CLI Agent 实用指南](https://github.com/grapeot/ai-agent-cli-skill) → 已迁移到独立 public repo。只把 root skill `skills/skill_ai_agent_cli.md` 接到 workspace index；Claude Code / Codex / OpenCode / Antigravity / Grok 是 repo 内 on-demand 文件
- [OpenReview API](./openreview.md) — 查询 AI 学术会议论文 metadata 和作者 profile（institution history、position、tilde ID）。触发词："OpenReview"、"查作者 profile"、"ICLR papers"、"NeurIPS papers"、"tilde ID"
- [GitHub Actions → Koyeb 部署指南](./deployment_github_actions_koyeb.md) — 通过 GitHub Actions 实现测试通过后自动部署到 Koyeb；适用于任何 Docker 化应用
- [使用 Apple 官方命令行工具发布 App Store Connect](./deployment_app_store_connect_cli.md) ✅ — 用稳定版 Xcode 完成 iOS archive、distribution export、IPA metadata 核验与授权后的上传
- [分享报告到 Web](./share_report.md) ⚙️ — 将 MD 报告转 HTML 发布到你自己的服务器，返回 URL
- [Apple Compressor Skill](./compressor.md) ⚙️ — 本机 Apple Compressor CLI 转码；custom preset 路径、源文件写入完成检测、batch 提交与监控

### Workflow（工作流）

特定任务的完整工作流程。

- [并行 Subagent 工作流](./workflow_parallel_subagents.md) ✅ — 用 `multi_tool_use.parallel` 并行执行多个 `functions.task` subagent
  - **必读**：初次使用并行 subagent 前，必须先读此 skill
  - **核心标准**：适合并行读、独立探索、交叉验证和上下文隔离；不适合强顺序依赖或共享状态写入
  - **正确并行**：必须在同一条消息里用 `multi_tool_use.parallel` 包多个 `functions.task`；逐个调用就是串行
  - 判断标准：任务命中信息面宽、独立读任务、独立判断、高价值不确定性、主线程需保留整合能力中的至少 2 条
  - 核心参数：并行度 ≤5，调研 overlap 30-50%，代码 overlap 0-20%
  - 含 subagent 来源说明、文件优先交接五原则、temperature 警告和 ollama zero-data-retention 路线
- [Workflow Watchdog](./workflow_watchdog.md) — 派出 workflow/后台 agent 后设 ~30 分钟巡检，区分"真忙 vs 鬼打墙"，卡住就 kill 并用部分结果推进。触发词："watchdog"、"workflow 卡住"、"后台任务巡检"
- [深度调研工作流](./workflow_deep_research_survey.md) ✅ — 多 Agent 并行 + 交叉验证（Phase 1-3 信息采集）
- [公开 Consensus Net Income 审计工作流](./workflow_public_consensus_net_income_audit.md) — 用 MarketScreener 等公开网页审计一组股票的 FY/CY consensus net income，区分 direct/derived、current/baseline/revision，并要求逐链接 QA。触发词："consensus net income"、"MarketScreener 审计"、"FY2026E 净利润共识"
- [科研论文调研与写作工作流](./workflow_research_paper_survey_writing.md) — 把科研论文转化为面向技术从业者的分析文章。核心：按读者重要性排序（不按论文章节）、三层分离（paper claim / 外部验证 / 我们的判断）、强制生态位分析（bottleneck / 替代路径 / stack 层级 / 相邻影响）。触发词："分析这篇论文"、"写论文解读"、"paper analysis"
- [外部写作工作流](./workflow_external_writing.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/workflow_external_writing.md) — external-facing 分析文章操作主干；双生成单审查、分离冷读验收、终端冷读一票放行
- [External Prose Lint CLI](./external_prose_lint.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/external_prose_lint.md) — 确定性中文 prose 扫描；`python -m writing_skill.external_prose_lint_cli <md>`
- [内部写作工作流](./workflow_internal_writing.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/workflow_internal_writing.md) — 内部文档写作；结论前置、概念出场顺序、可验证性
- [认知画像提取工作流](./workflow_cognitive_profile_extraction.md) — 从非结构化对话数据提取可预测的认知公理
  - 适用：群聊/Slack/Discord/邮件/播客转录等任意对话数据
  - 流程：Round 驱动的迭代引擎（Discover / Verify / Finalize / Restructure），动态滚动
  - 含口号检测、R01 可信度虚高警告、候选重构等陷阱对策
  - **要求 Opus 模型**：写作由 Opus 亲自完成，调研全部 delegate + 并行
- 语义搜索技能 → 见 ecosystem [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)：本地文本 embedding + cosine 相似度检索，支持任意 OpenAI-compatible endpoint
- [知识飞轮设计模式](./workflow_knowledge_flywheel.md) — 笨数据+笨方法+笨模型=精知识
- [视频下载与语音识别工作流（Qwen ASR 优先）](./workflow_bilibili_whisper_transcription.md) — Bilibili/YouTube 视频处理；默认 MLX Qwen ASR 1.7B，Whisper 作为 fallback
- [延时执行技能](./delayed_execution.md) ⚙️ — 低风险 `sleep + nohup` fallback；durable/AI 延时任务见 ecosystem 的 Process Launcher + OpenCode Skill
- [项目脚手架与重整](./project_scaffold.md) ✅ — 把散装目录升级成标准项目结构：`docs/`、`src/`、`scripts/`、`tests/`、`AGENTS.md` 与独立 git
- [AI Session Search & Archive](./ai_session_search_archive.md) — 在 OpenCode、Claude Code、Codex、Antigravity 与 Second Mind 的统一 Markdown 归档中按来源检索；named entity 先走 lexical search，模糊记忆再走 semantic search
- [iOS UI 自动化测试工作流](./ios_ui_automation.md) — 基于 Xcode 模拟器、XCTest 与 simctl 的 iOS 界面及功能自动化验证指南

### BestPractice（最佳实践）

通用的最佳实践和经验教训。

- [外部中文 prose 诊断词汇表](./bestpractice_external_prose.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/bestpractice_external_prose.md) — Manager 参考词汇表；不是 gate 清单，不进 Writer 上下文
- [外部文章启发性分析视角（Thesis Catalog）](./reference_writing_thesis_catalog.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/reference_writing_thesis_catalog.md) — L1-L8 启发性分析视角及相关 axiom 映射
- [内部文档排版与自适应视觉组件规范](./bestpractice_internal_visuals.md) ✅ — 内部 Memo/RFC/周报的自适应 HTML 卡片、主题变量、暗色模式兼容与视觉组件规范
- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70%问题、成功标准、可验证性
- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill 时使用，强调结果确定性、验收标准和边界条件
- [API Key 管理与调用](./bestpractice_api_key_management_1password_cli.md) ✅ — 使用 1Password CLI 安全管理密钥；含字段命名约定（`<service>_api_key` / `_token` / `_app_password` 等）和推断新 service 1Password 路径的方法
- [学术论文下载与格式转换](./bestpractice_academic_paper_conversion.md) ✅ — 基于 arXiv ID 检索、HTML/PDF 抓取并转化为 Markdown 的质量控制最佳实践
- [面试评估框架](./bestpractice_interview_evaluation.md) ✅ — Trait > Skill、AI 作弊识别、技术深度探测
- [Markdown 转 HTML 最佳实践](./bestpractice_markdown_html_conversion.md) ✅
- [PDF 转 Markdown](./bestpractice_pdf_to_markdown.md) ✅ — 默认用 Docling，避免 PDF 场景下 MarkItDown / PyMuPDF4LLM / Marker 的质量或许可问题
- [时间敏感信息验证](./bestpractice_temporal_info_verification.md) ✅ — 验证可能超出 knowledge cutoff 的信息
- [分阶段工作法](./bestpractice_staged_approach.md) ✅ — 隔离-处理-验证闭环，破坏性操作前 Dry Run
- [GUI 自动化方法论](./bestpractice_gui_automation.md) ✅ — 把没有 API 的界面转化为可编程接口
- [AI 辅助调试诊断](./bestpractice_ai_debugging_diagnosis.md) ✅ — "代码改不好"的根因诊断决策树
- [Mac Universal Clipboard 重置](./mac_universal_clipboard.md) ✅ — Mac 与 iPhone/iPad 剪贴板不同步时，重置 `useractivityd` / `sharingd` / `pboard`
- [AI 产品设计原则](./bestpractice_ai_product_design.md) ✅ — 线性聊天 vs 知识工作、感知规则解耦
- [产品/技术决策逆向工程](./bestpractice_product_decision_analysis.md) ✅ — 从设计空间、约束和 trade-off 分析产品或技术决策
- [iOS Test Acceleration](./ios_test_acceleration.md) — iOS unit/UI test iteration tips：sequential `xcodebuild`、`build-for-testing` + `test-without-building`、fixed simulator UUID、focused `-only-testing`、fixture launch arguments 和 `.xcresult` inspection
- [Playwright E2E 测试方法论](https://github.com/grapeot/playwright-test-skill) 🔗 — CDP step-by-step debugging CLI + E2E methodology。独立 public repo，CLI: `pw-test`。触发词："Playwright E2E"、"CDP debugging"、"SSO login test"、"browser step debugging"
- [Playwright Ajax Capture](./playwright_ajax_capture.md) — 在已登录的 CDP 浏览器 session 里拦截 fetch/XHR，逆向 web app 的 internal API contract（URL/method/payload/auth），再用 plain requests 复现，绕过 Admin API 限制。触发词："抓 ajax"、"逆向 internal API"、"browser session 调 API"、"不用 admin key"

---

## 如何添加你自己的 Skill

创建或重写 skill 前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。它说明如何用目标、验收标准、可用资源和输出规格定义一个 skill，而不是把 skill 写成机械步骤清单。

文件命名建议采用 `<category>_<name>.md`，例如 `workflow_my_process.md`、`bestpractice_my_insight.md`。写完后在本 INDEX 的对应分类下添加入口，确保后续 agent 能找到。

## Progressive Disclosure

Skills 采用渐进式披露原则：
- **INDEX.md** 提供概览，快速定位
- **具体 skill 文件** 包含完整的操作步骤和示例
