# Skills Index

本索引指向可复用的 Skills（技能）—— AI 可以调用的工具、流程和最佳实践。

- **想使用某个能力** → 浏览下方分类，找到对应的 skill 文件
- **想添加新 skill** → 参考现有文件格式，添加到对应分类
- **想安装更多工具型能力** → 看 [`../../docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)，那里列出可单独安装的 public skill repo

## Multi-Agent 能力提示

当前 harness 支持通过 `multi_tool_use.parallel` 并行派发多个 `functions.task` subagent。不要默认使用，但遇到大型、可并行、调研重、代码库探索重、需要独立交叉验证的任务时，应先读 [并行 Subagent 工作流](./workflow_parallel_subagents.md)。

快速判断：subagent 适合并行读、独立探索、反方审稿、事实核查和上下文窗口隔离；不适合单点小任务、强顺序依赖任务，以及多个 agent 同时写同一份状态或同一批文件。

## 芯片 / 加速器问题路由（优先）

遇到 **AI 芯片、ML 加速器、编译器 toolchain、运行时 internals** 相关问题时，**先读** [Crucible Notes 查阅指南](./reference_crucible_notes.md)，再决定是否需要并行 subagent 或深度调研 workflow。

| 问题类型 | 第一步 | 第二步 |
|----------|--------|--------|
| NEFF / NKI / Penguin IR / GPSIMD / Trainium ISA | `reference_crucible_notes.md` | 官方 AWS Neuron docs 对照 |
| CUDA PTX/SASS、cicc/ptxas/nvlink 编译链 | `reference_crucible_notes.md` | CUDA Toolkit docs 对照 |
| TPU PJRT / LLO ISA | `reference_crucible_notes.md` | Google TPU docs 对照 |
| 芯片代际、规格、软件栈、产品对比 | `contexts/survey_sessions/*_survey_*.md`（若已有） | `workflow_deep_research_survey.md` |
| internals + 产品层混合 | 先 `reference_crucible_notes.md` 定下层 | 再 survey workflow / 已有报告补产品层 |

**触发词示例**：Neuron、Trainium、Inferentia、NEFF、NKI、GPSIMD、neuronx-cc、PTX、SASS、ptxas、cicc、TPU PJRT、libtpu、编译 pass、IR lowering、runtime ioctl、fatbin。

**不在 crucible 覆盖范围**（如 Meta MTIA、AMD MI、通用 GPU 微架构）→ 跳过 crucible，直接用 `workflow_deep_research_survey.md`。

---

## 组件状态

### Tier 1: 核心（clone 后即可开始）
- ✅ Rules 框架（SOUL/USER/COMMUNICATION/WORKSPACE）— 填写即用
- ✅ Skills 框架（本目录）— 填写即用
- ✅ 三层记忆系统 — 需配置 OpenCode + cron

### Tier 2: 扩展（需要额外配置）
- ⚙️ Semantic Search — 需要 LLM Studio 或 OpenAI API
- ⚙️ Share Report — 需要 SSH 服务器或 GitHub Pages
- ⚙️ Google Docs — 需要 Google OAuth
- ⚙️ Send Email — 需要 Gmail App Password
- ⚙️ Delayed Execution — starter fallback；durable/AI 延时任务安装 Process Launcher + OpenCode Skill

### Tier 3: 独立 public skill repos（按需安装）
- 🔧 图片生成、Tavily、Google Docs、Google Maps、Outlook、Resend、OpenCode、Process Launcher、PPTX、Typefully、Circle Post、Stripe 等能力见 [`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)

### 说明
✅ = 最多 15 分钟即可使用
⚙️ = 需要额外配置，不配不影响核心功能
🔧 = 独立 repo，按需安装到你的 workspace

---

## 分类索引

### API Guide（API 指南）

调用外部系统或工具的操作手册。

- [AI CLI Agent 实用指南](./ai_agent_cli_guide.md) — CLI Agent 设计原则、工具对比（Claude Code / Codex / OpenCode）、文件响应模式、AI 调用 AI
- [给自己发邮件技能](./send_email.md) ⚙️ — 通过 Gmail 发送邮件通知，需配置 App Password
- [分享报告到 Web](./share_report.md) ⚙️ — 将 MD 报告转 HTML 发布到你自己的服务器，返回 URL
- [Google Docs 操作](./google_docs.md) ⚙️ — CLI 工具：发布 Markdown、创建/搜索/修改/分享文档
- [增长数据分析](./growth_analytics.md) ⚙️ — 三个 CLI 查询网站流量（GA4）、邮件订阅（Kit）、Twitter 互动（Typefully）
- [Typefully Metrics CLI](./typefully_metrics.md) ⚙️ — 通过浏览器 session 凭据查询 Twitter impression、engagement、followers 数据
- [Typefully 发帖 CLI](./typefully_post.md) ⚙️ — 通过 Typefully v2 API 创建草稿、排期发布和直接发布 tweet / thread
- [Apple Compressor Skill](./compressor.md) ⚙️ — 本机 Apple Compressor CLI 转码；custom preset 路径、源文件写入完成检测、batch 提交与监控
- [Crucible Notes 查阅指南](./reference_crucible_notes.md) ✅ — CUDA / AWS Neuron / TPU 编译器与运行时 internals 逆向 wiki；含可信度分层、组件路由与 Neuron 栈阅读顺序

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
- [AI 生成 Slide Deck 工作流](./workflow_presentation_slides.md) — Gemini 渲染、Clean Ink 风格、8 进程并行、4K 放大前验证
- [语义搜索技能](./semantic_search.md) ⚙️ — 利用向量相似度检索深层背景与观点演变
- [知识飞轮设计模式](./workflow_knowledge_flywheel.md) — 笨数据+笨方法+笨模型=精知识
- [视频下载与语音识别工作流](./workflow_bilibili_whisper_transcription.md) — Bilibili/YouTube 视频处理
- [延时执行技能](./delayed_execution.md) ⚙️ — 低风险 `sleep + nohup` fallback；durable/AI 延时任务见 ecosystem 的 Process Launcher + OpenCode Skill
- [项目脚手架与重整](./project_scaffold.md) ✅ — 把散装目录升级成标准项目结构：`docs/`、`src/`、`scripts/`、`tests/`、`AGENTS.md` 与独立 git

### Cursor Skills（awesome-cursor-skills）

来自 [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources)，kebab-case 目录名 → snake_case 文件名。上游更新时可重新运行 `adhoc_jobs/import_awesome_cursor_skills/import_skills.py`。

#### Cursor-Native

- [Suggesting Cursor Rules](./suggesting_cursor_rules.md) — When the user repeats the same correction or convention multiple times, suggest a Cursor rule to encode it permanently.
- [Suggesting Cursor Hooks](./suggesting_cursor_hooks.md) — When the user keeps asking for the same check to run (lint, tests, type-check), suggest a Cursor hook to automate it.
- [Switch Project](./switching_projects.md) — Switch the current Cursor workspace to a different project directory using the cursor-app-control MCP. Use when the user asks to switch projects, open another repo, jump to a different codebase, or move to a worktree.
- [Saving Workspace Context](./saving_workspace_context.md) — Automatically persist useful context — research, decisions, learnings, templates — to workspace files so knowledge survives across conversations.
- [Visual QA](./visual_qa_testing.md) — Visually QA a web application by launching it in Cursor's built-in browser, taking screenshots, checking console errors, and auditing network requests. Use after making UI changes to verify they look correct.
- [Verify in Browser](./verifying_in_browser.md) — After making code changes, start the dev server, open the app in Cursor's built-in browser, and verify everything works — check rendering, console errors, and network health. Use proactively after any UI or API change.
- [Performance Profile](./profiling_performance.md) — Profile a running web application's CPU performance using Cursor's built-in browser profiler. Captures call stacks, identifies slow functions, and suggests optimizations. Use when a page feels slow or janky.
- [Screenshot Changelog](./screenshotting_changelog.md) — Generate a visual changelog or PR description by taking before/after screenshots of UI changes using Cursor's built-in browser. Use when preparing a PR with visual changes.
- [Best-of-N Problem Solving](./best_of_n_solving.md) — Solve a hard problem by trying multiple approaches in parallel using isolated git worktrees. Each attempt runs in its own branch, and the best solution is selected. Use for complex refactors, tricky bugs, or architectural decisions where multiple strategies could work.
- [Parallel Explore](./parallel_exploring.md) — Explore a large codebase in parallel by launching multiple explore subagents that each investigate a different area simultaneously. Use when onboarding onto a new project, understanding architecture, or investigating a cross-cutting concern.
- [Grind Until Pass](./grinding_until_pass.md) — Keep iterating on code changes until the tests pass, the build succeeds, or linting is clean. Runs in a tight loop of fix → run → check → repeat. Use when you want the agent to autonomously grind through test failures or build errors.
- [Finding Dev Server URL](./finding_dev_server_url.md) — Scan running terminals for dev server URLs (localhost ports), report them, and optionally open the app in Cursor's built-in browser.
- [Monitoring Terminal Errors](./monitoring_terminal_errors.md) — Watch running terminal processes for crashes and stack traces. When an error appears, navigate to the failing file and line, diagnose, and fix it automatically.
- [Detecting Port Conflicts](./detecting_port_conflicts.md) — Detect EADDRINUSE and port conflicts, find what's using the port, and resolve it by killing the process or suggesting an alternative port.
- [Tailing Build Output](./tailing_build_output.md) — Monitor a build process (webpack, turbo, docker) for warnings and errors as they stream. Summarize issues and fix them before the build finishes.
- [Responsive Testing](./responsive_testing.md) — Open the app in Cursor's browser at multiple viewport sizes, screenshot each, and report any layout breakage.
- [Dark Mode Testing](./dark_mode_testing.md) — Toggle between light and dark mode in Cursor's browser, screenshot both states, and flag missing token mappings or contrast issues.
- [Accessibility Auditing](./accessibility_auditing.md) — Use Cursor's browser aria snapshots to audit a page for accessibility issues — missing labels, broken tab order, contrast, and ARIA misuse.
- [Form Testing](./form_testing.md) — Use Cursor's browser to fill and submit every form in the app with valid and invalid data, verifying validation, error states, and success flows.
- [Parallel Test Fixing](./parallel_test_fixing.md) — When multiple tests fail, assign each failing test file to a separate subagent that fixes it independently in parallel.
- [Codebase Onboarding](./codebase_onboarding.md) — Launch multiple explore subagents in parallel to investigate architecture, data models, auth, APIs, and deployment. Synthesize into an onboarding document.
- [Comparing Branches Visually](./comparing_branches_visually.md) — Check out two branches in separate worktrees, start both dev servers on different ports, screenshot the same pages, and produce a visual diff.
- [Auto Type Checking](./auto_type_checking.md) — Run TypeScript type checking after file edits and immediately flag type errors before moving on. Uses Cursor hooks for automatic enforcement.
- [Suggesting Skills](./suggesting_skills.md) — When the user struggles with a task that a known skill could handle, suggest installing it.
- [Parallel CI Triage](./parallel_ci_triage.md) — When GitHub Actions fails, fetch failing job logs and assign each failing job to a separate subagent that fixes its slice of the problem in parallel. Use for multi-job CI failures where jobs are independent.
- [Parallel Code Review](./parallel_code_review.md) — Run four parallel read-only subagents that each review the same diff from a different lens — security, performance, correctness, and readability — then merge findings into one report. Use before merging large or risky PRs.
- [Network Request Auditing](./network_request_auditing.md) — After navigating and interacting in Cursor's built-in browser, use browser_network_requests to audit every fetch/XHR for failures, slowness, duplicate calls, and suspicious payloads. Use for API-heavy pages and after backend or client networking changes.
- [Recording Browser Flow as Playwright Test](./recording_browser_flow_as_test.md) — Execute a user flow step-by-step in Cursor's built-in browser while documenting each action, then emit a Playwright test that replays the same flow using stable selectors derived from the accessibility tree.
- [Building Skills From Patterns](./building_skills_from_patterns.md) — When the same multi-step workflow repeats in Cursor (user corrections or agent redos), capture it as a new SKILL.md under .cursor/skills/ so future sessions load it automatically.

#### Analytics & Tracking

- [Add Analytics (PostHog)](./adding_analytics.md) — Add PostHog analytics to a web application, including event tracking, page views, feature flags, and session replay.
- [Add Feature Flags](./adding_feature_flags.md) — Add feature flags to an application for gradual rollouts, A/B testing, and kill switches using PostHog, LaunchDarkly, or a simple local implementation.

#### Error Tracking

- [Add Error Tracking (Sentry)](./adding_error_tracking.md) — Add Sentry error tracking, performance monitoring, and source maps to a web application.

#### Auth & Payments

- [Add Authentication (Auth.js)](./adding_auth.md) — Add authentication to a web application using NextAuth.js (Auth.js), including OAuth providers, session management, and protected routes.
- [Add Stripe Payments](./adding_stripe.md) — Integrate Stripe payments into a web application, including checkout sessions, webhooks, and customer portal.

#### Testing

- [Add E2E Tests (Playwright)](./adding_e2e_tests.md) — Set up Playwright end-to-end testing in a project, including test configuration, example tests, and CI integration.
- [Writing Tests](./writing_tests.md) — Analyze existing code and write comprehensive unit and integration tests for it. Detects the test framework, identifies untested code paths, and generates tests with proper mocking, edge cases, and assertions. Use when the user asks to add tests, improve coverage, or test a specific module.
- [Python TDD with uv](./python_tdd_with_uv.md) — Test-driven development in Python using uv as the package manager. Covers the red-green-refactor cycle, vertical slicing, and uv project setup.
- [API Smoke Testing](./api_smoke_testing.md) — Start the dev server, discover API routes from the codebase, hit every endpoint, and report which ones return errors.

#### Workflow

- [Babysitting a PR](./babysitting_pr.md) — Monitor a pull request for CI failures, review comments, and merge conflicts — then fix them automatically. Use when a PR is open and you want the agent to keep it merge-ready.
- [Creating a PR](./creating_pr.md) — Create a clean, review-ready pull request with a good title, structured description, linked issues, and appropriate reviewers.
- [Writing Commit Messages](./writing_commit_messages.md) — Write clear, conventional commit messages with proper type prefixes, scopes, and body content.
- [Incident Response](./incident_response.md) — Handle production incidents — triage, mitigate, communicate, and write postmortems.
- [Systematic Debugging](./systematic_debugging.md) — Structured debugging methodology — reproduce, isolate, hypothesize, verify. Covers git bisect, binary search, logging, and minimal reproduction.

#### Infrastructure & DevOps

- [Add Docker](./adding_docker.md) — Dockerize an application with a production-ready Dockerfile, docker-compose setup, and .dockerignore.
- [Setup CI (GitHub Actions)](./setting_up_ci.md) — Set up a GitHub Actions CI/CD pipeline with linting, testing, type-checking, and deployment steps.
- [Setup Terraform](./setting_up_terraform.md) — Set up Terraform infrastructure-as-code for cloud resources, including provider configuration, modules, state management, and CI integration.
- [Kubernetes Deploying](./kubernetes_deploying.md) — Deploy applications to Kubernetes — Deployments, Services, Ingress, ConfigMaps, Secrets, health checks, and scaling.

#### Code Quality & Security

- [Code Review](./reviewing_code.md) — Perform a thorough code review focused on correctness, maintainability, performance, and best practices.
- [Security Audit](./auditing_security.md) — Perform a systematic security audit of a codebase, checking for OWASP Top 10 vulnerabilities, secrets exposure, and insecure patterns.
- [Performance Audit](./auditing_performance.md) — Audit and optimize application performance, including bundle size, rendering, database queries, and Core Web Vitals.
- [Verifying Markdown Formatting](./verifying_markdown_formatting.md) — Verify that a Markdown file has correct formatting — headings, lists, links, code blocks, spacing, and consistent style.
- [Fixing Broken Links](./fixing_broken_links.md) — Crawl all links in a file or project, test each for a valid HTTP response, report broken ones, and fix or remove them.

#### Dependencies

- [Updating an npm Package](./updating_npm_package.md) — Safely update an npm package by checking npmjs.com for the latest version, reading release notes, and handling minor vs major upgrades differently. For minor updates, just do it. For major updates, find the upgrade guide, validate breaking changes, and produce a detailed migration report.

#### Frontend & UI

- [Using UI Stack](./using_ui_stack.md) — Enforce a configuration-driven design system when generating UI. Ensures consistent spacing, colors, typography, dark mode, interactions, and accessibility across all AI-generated components.
- [Converting CSS to Tailwind](./converting_css_to_tailwind.md) — Convert plain CSS stylesheets to Tailwind CSS utility classes. Handles selectors, media queries, pseudo-classes, custom properties, and animations.
- [Converting CSS Modules to Tailwind](./converting_css_modules_to_tailwind.md) — Migrate CSS Modules (.module.css/.module.scss) to Tailwind utility classes. Handles styles object removal, className interpolation, composition, and global overrides.
- [React Native Patterns](./react_native_patterns.md) — Build mobile apps with React Native and Expo — navigation, platform-specific code, performance, and native modules.

#### Planning & Architecture

- [Architecture Decision Records](./architecture_decision_records.md) — Document technical decisions as Architecture Decision Records (ADRs) with context, options considered, and rationale.
- [Database Design](./database_design.md) — Design database schemas — tables, relationships, indexes, constraints, and ORM setup. Covers relational design, normalization, and common patterns.

#### Documentation

- [Add API Documentation (OpenAPI)](./adding_api_docs.md) — Generate OpenAPI/Swagger documentation for an API, including endpoint schemas, request/response types, and interactive docs UI.

#### Utilities

- [Exporting to PNG](./exporting_to_png.md) — Export code, terminal output, diagrams, or UI components to PNG images using headless browser rendering or CLI tools.
- [Generating Images (OpenAI gpt-image-2)](./generating_images.md) — >-
- [Prompt Engineering](./prompt_engineering.md) — Write effective prompts for LLMs — structure, few-shot examples, chain-of-thought, system prompts, and output parsing.
- [SEO Auditing](./seo_auditing.md) — Audit technical SEO — meta tags, structured data, Open Graph, sitemaps, robots.txt, performance, and accessibility signals.
- [Writing Copy](./writing_copy.md) — Write marketing copy for landing pages, product descriptions, CTAs, emails, and app UI text.

### BestPractice（最佳实践）

通用的最佳实践和经验教训。

- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70%问题、成功标准、可验证性
- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill 时使用，强调结果确定性、验收标准和边界条件
- [API Key 管理与调用](./bestpractice_api_key_management_1password_cli.md) ✅ — 使用 1Password CLI 安全管理密钥
- [面试评估框架](./bestpractice_interview_evaluation.md) ✅ — Trait > Skill、AI 作弊识别、技术深度探测
- [Markdown 转 HTML 最佳实践](./bestpractice_markdown_html_conversion.md) ✅
- [PDF 转 Markdown](./bestpractice_pdf_to_markdown.md) ✅ — 默认用 Docling，避免 PDF 场景下 MarkItDown / PyMuPDF4LLM / Marker 的质量或许可问题
- [时间敏感信息验证](./bestpractice_temporal_info_verification.md) ✅ — 验证可能超出 knowledge cutoff 的信息
- [分阶段工作法](./bestpractice_staged_approach.md) ✅ — 隔离-处理-验证闭环，破坏性操作前 Dry Run
- [GUI 自动化方法论](./bestpractice_gui_automation.md) ✅ — 把没有 API 的界面转化为可编程接口
- [AI 辅助调试诊断](./bestpractice_ai_debugging_diagnosis.md) ✅ — "代码改不好"的根因诊断决策树
- [AI 产品设计原则](./bestpractice_ai_product_design.md) ✅ — 线性聊天 vs 知识工作、感知规则解耦
- [产品/技术决策逆向工程](./bestpractice_product_decision_analysis.md) ✅ — 从设计空间、约束和 trade-off 分析产品或技术决策

---

## 如何添加你自己的 Skill

创建或重写 skill 前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。它说明如何用目标、验收标准、可用资源和输出规格定义一个 skill，而不是把 skill 写成机械步骤清单。

文件命名建议采用 `<category>_<name>.md`，例如 `workflow_my_process.md`、`bestpractice_my_insight.md`。写完后在本 INDEX 的对应分类下添加入口，确保后续 agent 能找到。

## Progressive Disclosure

Skills 采用渐进式披露原则：
- **INDEX.md** 提供概览，快速定位
- **具体 skill 文件** 包含完整的操作步骤和示例
