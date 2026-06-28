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
- 🔧 图片生成、Tavily、Google Docs、Google Maps、Outlook、Resend、OpenCode、Process Launcher、PPTX、Typefully、Circle Post、Stripe、Firewalla、Smart Home 等能力见 [`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)

### 说明
✅ = 最多 15 分钟即可使用
⚙️ = 需要额外配置，不配不影响核心功能
🔧 = 独立 repo，按需安装到你的 workspace

---

## 分类索引

### API Guide（API 指南）

调用外部系统或工具的操作手册。

- [AI CLI Agent 实用指南](./ai_agent_cli_guide.md) — CLI Agent 设计原则、工具对比（Claude Code / Codex / OpenCode）、文件响应模式、AI 调用 AI
- [Claude Code 使用指南](./claude_code.md) — Claude Code 的默认 runtime 设置（adaptive thinking 规避）、非交互命令行调用、嵌套调用硬规则及 Timeout 管理
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
- [深度调研工作流](./workflow_deep_research_survey.md) ✅ — 多 Agent 并行 + 交叉验证（Phase 1-3 信息采集）
- [外部写作工作流](./workflow_external_writing.md) ✅ — 将调研素材转化为有判断力的 external-facing 分析文章。包含 Thesis Catalog（核心分析视角 L1-L6）和判断合成步骤。**做深度调研并写 external 文章时，两个 skill 都要读**
- [内部写作工作流](./workflow_internal_writing.md) ✅ — 面向用户本人、共享上下文协作者和未来 AI agent 的内部文档写作。核心是低决策摩擦：结论前置、skimmable、inline evidence、方便跳转和验证，必要时用图表降低认知负担。
- [认知画像提取工作流](./workflow_cognitive_profile_extraction.md) — 从非结构化对话数据提取可预测的认知公理
  - 适用：群聊/Slack/Discord/邮件/播客转录等任意对话数据
  - 流程：广泛扫描 → 深度验证 → 压力测试 → 定稿（≥3 轮动态滚动）
  - **要求 Opus 模型**：写作由 Opus 亲自完成，调研全部 delegate + 并行
- [语义搜索技能](./semantic_search.md) ⚙️ — 利用向量相似度检索深层背景与观点演变
- [知识飞轮设计模式](./workflow_knowledge_flywheel.md) — 笨数据+笨方法+笨模型=精知识
- [视频下载与语音识别工作流](./workflow_bilibili_whisper_transcription.md) — Bilibili/YouTube 视频处理
- [延时执行技能](./delayed_execution.md) ⚙️ — 低风险 `sleep + nohup` fallback；durable/AI 延时任务见 ecosystem 的 Process Launcher + OpenCode Skill
- [项目脚手架与重整](./project_scaffold.md) ✅ — 把散装目录升级成标准项目结构：`docs/`、`src/`、`scripts/`、`tests/`、`AGENTS.md` 与独立 git
- [iOS UI 自动化测试工作流](./ios_ui_automation.md) — 基于 Xcode 模拟器、XCTest 与 simctl 的 iOS 界面及功能自动化验证指南

### BestPractice（最佳实践）

通用的最佳实践和经验教训。

- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70%问题、成功标准、可验证性
- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill 时使用，强调结果确定性、验收标准和边界条件
- [API Key 管理与调用](./bestpractice_api_key_management_1password_cli.md) ✅ — 使用 1Password CLI 安全管理密钥
- [学术论文下载与格式转换](./bestpractice_academic_paper_conversion.md) ✅ — 基于 arXiv ID 检索、HTML/PDF 抓取并转化为 Markdown 的质量控制最佳实践
- [面试评估框架](./bestpractice_interview_evaluation.md) ✅ — Trait > Skill、AI 作弊识别、技术深度探测
- [Markdown 转 HTML 最佳实践](./bestpractice_markdown_html_conversion.md) ✅
- [PDF 转 Markdown](./bestpractice_pdf_to_markdown.md) ✅ — 默认用 Docling，避免 PDF 场景下 MarkItDown / PyMuPDF4LLM / Marker 的质量或许可问题
- [时间敏感信息验证](./bestpractice_temporal_info_verification.md) ✅ — 验证可能超出 knowledge cutoff 的信息
- [分阶段工作法](./bestpractice_staged_approach.md) ✅ — 隔离-处理-验证闭环，破坏性操作前 Dry Run
- [GUI 自动化方法论](./bestpractice_gui_automation.md) ✅ — 把没有 API 的界面转化为可编程接口
- [AI 辅助调试诊断](./bestpractice_ai_debugging_diagnosis.md) ✅ — "代码改不好"的根因诊断决策树
- [AI 产品设计原则](./bestpractice_ai_product_design.md) ✅ — 线性聊天 vs 知识工作、感知规则解耦
- [产品/技术决策逆向工程](./bestpractice_product_decision_analysis.md) ✅ — 从设计空间、约束和 trade-off 分析产品或技术决策
- [Playwright E2E 测试方法论](./playwright_e2e.md) ✅ — 用 Playwright 建立 E2E 测试的核心方法论：CDP 手动调试法（先跑通再自动化）、SSO 登录流程的已知陷阱（SDK callback、JWT algorithm/issuer、新用户多步 modal、register vs sign-in）。触发词："Playwright E2E"、"前端端到端测试"、"SSO 登录测试"、"Logto 登录自动化"

---

## 如何添加你自己的 Skill

创建或重写 skill 前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。它说明如何用目标、验收标准、可用资源和输出规格定义一个 skill，而不是把 skill 写成机械步骤清单。

文件命名建议采用 `<category>_<name>.md`，例如 `workflow_my_process.md`、`bestpractice_my_insight.md`。写完后在本 INDEX 的对应分类下添加入口，确保后续 agent 能找到。

## Progressive Disclosure

Skills 采用渐进式披露原则：
- **INDEX.md** 提供概览，快速定位
- **具体 skill 文件** 包含完整的操作步骤和示例
