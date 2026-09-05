# Skills Index

本索引只做路由：告诉你「什么时候该看哪个 skill」，不教你怎么调。命中后先读对应 skill 文件再动手。

- **要用某个能力** → 按下方分类定位到 skill 文件，然后**读它**
- **要加新 skill** → 参考现有格式，加到对应分类
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

- [AI CLI Agent 实用指南](https://github.com/grapeot/ai-agent-cli-skill) → 已迁移到独立 public repo；Claude Code / Codex / OpenCode / Antigravity / Grok 能力从该 repo 按需安装
- [OpenReview API](./openreview.md) — 查询 AI 学术会议论文 metadata 和作者 profile（institution history、position、tilde ID）。触发词："OpenReview"、"查作者 profile"、"ICLR papers"、"NeurIPS papers"、"tilde ID"
- [GitHub Actions → Koyeb 部署指南](./deployment_github_actions_koyeb.md) — 通过 GitHub Actions 实现测试通过后自动部署到 Koyeb；适用于任何 Docker 化应用
- [使用 Apple 官方命令行工具发布 App Store Connect](./deployment_app_store_connect_cli.md) ✅ — 用稳定版 Xcode 完成 iOS archive、distribution export、IPA metadata 核验与授权后的上传
- [分享报告到 Web](./share_report.md) ⚙️ — 将 MD 报告转 HTML 发布到你自己的服务器，返回 URL
- [Apple Compressor Skill](./compressor.md) ⚙️ — 本机 Apple Compressor CLI 转码；custom preset 路径、源文件写入完成检测、batch 提交与监控

### Workflow（工作流）

特定任务的完整工作流程。

- [并行 Subagent 工作流](./workflow_parallel_subagents.md) ✅ — 并行派发多个 `functions.task` subagent 的调度方法；首次使用前必读，任务必须打包在单条消息内同时发起
- [Workflow Watchdog](./workflow_watchdog.md) — 派出后台 workflow/agent 任务后设 ~30 分钟定时巡检，识别正常执行与死循环挂起。触发词："watchdog"、"workflow 卡住"、"后台任务巡检"
- [深度调研工作流](./workflow_deep_research_survey.md) ✅ — 多 Agent 并行 + 交叉验证（Phase 1-3 信息采集）
- [公开 Consensus Net Income 审计工作流](./workflow_public_consensus_net_income_audit.md) — 用 MarketScreener 等公开金融站点核验一组股票的 FY/CY consensus net income。触发词："consensus net income"、"MarketScreener 审计"、"FY2026E 净利润共识"
- [科研论文调研与写作工作流](./workflow_research_paper_survey_writing.md) — 把科研论文重构为面向技术从业者的深度解读文章。触发词："分析这篇论文"、"写论文解读"、"paper analysis"
- [外部写作工作流](./workflow_external_writing.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/workflow_external_writing.md) — external-facing 分析文章操作主干；双生成单审查、分离冷读验收、终端冷读一票放行
- [External Prose Lint CLI](./external_prose_lint.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/external_prose_lint.md) — 确定性中文 prose 扫描；`python -m writing_skill.external_prose_lint_cli <md>`
- [内部写作工作流](./workflow_internal_writing.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/workflow_internal_writing.md) — 内部文档写作；结论前置、概念出场顺序、可验证性
- [认知画像提取工作流](./workflow_cognitive_profile_extraction.md) — 从群聊/Slack/Discord/邮件/播客转录等非结构化对话数据提取可预测的认知公理；要求 Opus 模型亲自完成写作
- 语义搜索技能 → 见 ecosystem [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)：本地文本 embedding + cosine 相似度检索，支持任意 OpenAI-compatible endpoint
- [知识飞轮设计模式](./workflow_knowledge_flywheel.md) — 笨数据+笨方法+笨模型=精知识
- [视频下载与语音识别工作流（Qwen ASR 优先）](./workflow_bilibili_whisper_transcription.md) — Bilibili/YouTube 音视频下载与语音识别处理流程
- [延时执行技能](./delayed_execution.md) ⚙️ — 低风险 `sleep + nohup` fallback；durable/AI 延时任务见 ecosystem 的 Process Launcher + OpenCode Skill
- [项目脚手架与重整](./project_scaffold.md) ✅ — 把散落文件升级为规范工程目录并初始化独立 Git 仓库
- [AI Session Search & Archive](./ai_session_search_archive.md) — 在 OpenCode、Claude Code、Codex、Antigravity 与 Second Mind 的统一 Markdown 归档中按来源检索历史会话
- [iOS UI 自动化测试工作流](./ios_ui_automation.md) — 基于 Xcode 模拟器、XCTest 与 simctl 的 iOS 界面及功能自动化验证指南

### BestPractice（最佳实践）

通用的最佳实践和经验教训。

- [外部中文 prose 诊断词汇表](./bestpractice_external_prose.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/bestpractice_external_prose.md) — Manager 参考词汇表；不是 gate 清单，不进 Writer 上下文
- [外部文章启发性分析视角（Thesis Catalog）](./reference_writing_thesis_catalog.md) → 已迁移到 [grapeot/writing-skill](https://github.com/grapeot/writing-skill/blob/master/skills/reference_writing_thesis_catalog.md) — L1-L8 启发性分析视角及相关 axiom 映射
- [内部文档排版与自适应视觉组件规范](./bestpractice_internal_visuals.md) ✅ — 内部 Memo/RFC/周报的自适应 HTML 卡片、主题变量、暗色模式兼容与视觉组件规范
- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70%问题、成功标准、可验证性
- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill 时使用，强调结果确定性、验收标准和边界条件
- [API Key 管理与调用](./bestpractice_api_key_management_1password_cli.md) ✅ — 通过 1Password CLI 统一管理与调用接口密钥；含字段命名约定与凭证检索路径推断规则
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
- [Playwright Ajax Capture](./playwright_ajax_capture.md) — 在已登录的 CDP 浏览器 session 中监听并拦截 fetch/XHR，逆向解析 web app 的 internal API 协议。触发词："抓 ajax"、"逆向 internal API"、"browser session 调 API"、"不用 admin key"

---

## 如何添加你自己的 Skill

创建或重写 skill 前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。它说明如何用目标、验收标准、可用资源和输出规格定义一个 skill，而不是把 skill 写成机械步骤清单。

文件命名建议采用 `<category>_<name>.md`，例如 `workflow_my_process.md`、`bestpractice_my_insight.md`。写完后在本 INDEX 的对应分类下添加入口，确保后续 agent 能找到。

## Progressive Disclosure

Skills 采用渐进式披露原则：
- **INDEX.md** 只提供路由，不含操作细节
- **具体 skill 文件** 包含完整的操作步骤和示例——命中后必须读它
