# Public Skill Ecosystem

`context-infrastructure` 自带的 `rules/skills/` 是 starter set：它展示 skill 应该如何被组织、索引和调用。更完整的能力不应该全部复制进这个仓库，而是通过独立 public skill repo 安装。这样做有两个好处：第一，每个 skill repo 可以保留自己的 README、CLI、测试和发布节奏；第二，用户 workspace 里的私有 alias、路径、token 和业务上下文可以留在本地 overlay，不会混进 public repo。

这个页面同时给人和 AI 看。人可以用它发现还可以安装哪些能力；AI 可以按这里的安装协议，把某个 public skill repo 接入目标 workspace。

## 安装协议

把下面这段话连同目标 repo URL 交给你的 coding agent：

```text
Install this public skill repo into my workspace:
<GitHub URL>

Start from my workspace AGENTS.md or CLAUDE.md. Follow any WORKSPACE.md or skills/INDEX.md routing rules. Clone or vendor the repo under an appropriate project directory. Expose exactly one root skill to my global skill index or agent instructions. Keep private aliases, local paths, credentials, endpoint defaults, and business context in a local overlay, not in the public repo.
```

安装完成后，workspace 通常会形成两层：public repo 负责通用技术 contract，本地 `rules/skills/` 或 `.env` 负责私有配置。例如 iMessage public repo 只提供 send-only CLI，本地 overlay 才保存联系人 alias；Stripe public repo 只提供只读分析 contract，本地 overlay 才保存具体业务归因。

## 推荐安装的 public skill repos

| 方向 | Repo | 能力 |
|---|---|---|
| Web search | [tavily-skill](https://github.com/grapeot/tavily-skill) | Tavily search/extract CLI，给 agent 稳定 JSON 输出 |
| Documents | [gdocs-skill](https://github.com/grapeot/gdocs-skill) | Google Docs 创建、搜索、修改、分享，支持 Markdown 和 tab |
| Maps / travel | [google-maps-routing-skill](https://github.com/grapeot/google-maps-routing-skill) | Google Maps Routes + Geocoding CLI，支持地址解析、实时 drive time 和 leave-by 规划 |
| Email | [outlook_skill](https://github.com/grapeot/outlook_skill) | Outlook.com 邮件下载、归档、Markdown 渲染、发送和日历邀请 |
| Email | [resend_email_skill](https://github.com/grapeot/resend_email_skill) | Resend 自定义域名发信、收件读取、Markdown 导出和附件检查 |
| Email / newsletter | [kit-skill](https://github.com/grapeot/kit-skill) | Kit Broadcast Markdown 发信 CLI，支持 dry-run、draft-only、web-only 和 tag/segment 定向；账号默认值放本地 overlay |
| Messaging | [imessage_skill](https://github.com/grapeot/imessage_skill) | macOS iMessage send-only CLI；联系人 alias 放本地 overlay |
| Agent operations | [opencode_skill](https://github.com/grapeot/opencode_skill) | OpenCode `submit` / `submit --dry-run` / batch submission、recurring cron workflow、SQLite 数据维护和 archive |
| Agent operations | [process-launcher](https://github.com/grapeot/process-launcher) | 本地 HTTP process launcher，适合 TCC / GUI 权限桥接、durable one-shot delayed jobs、进程日志 and 取消 |
| Agent operations | [opencode-docker](https://github.com/grapeot/opencode-docker) | Docker 部署模版，用于快速配置 OpenCode Server 容器化运行环境 |
| Usage analytics | [ai_usage_dashboard](https://github.com/grapeot/ai_usage_dashboard) | 多平台 AI token usage、成本估算、本地 dashboard 和 E1002 JSON |
| Social / growth | [typefully-twitter-skill](https://github.com/grapeot/typefully-twitter-skill) | Typefully 发帖、账号指标和 X/Twitter 单帖 analytics |
| Community publishing | [circle-post-skill](https://github.com/grapeot/circle-post-skill) | Circle community Markdown conversion, dry-run preflight, publish/update/delete CLI；社区默认值放本地 overlay |
| Payments / growth | [stripe-skill](https://github.com/grapeot/stripe-skill) | Stripe 只读 finance / sales analytics，live tests 默认 opt-in |
| Media | [online-media-skill](https://github.com/grapeot/online-media-skill) | 在线媒体下载、ASR artifact、query pack 和 source identification 工作流 |
| Slides | [presentation_skill](https://github.com/grapeot/presentation_skill) | 默认 image-generated full-slide deck；明确不用图像生成时 fallback 到 HTML module deck |
| Slides | [pptx.skill](https://github.com/grapeot/pptx.skill) | AI-first PPTX 读取、编辑和渲染 |
| Images | [image-generation-skill](https://github.com/grapeot/image-generation-skill) | Gemini Flash / Gemini Pro / GPT-Image-2 文生图、图片编辑、分辨率放大 |
| Images | [tiff-icc-profile](https://github.com/grapeot/tiff-icc-profile) | 给未标记 TIFF 嵌入 ICC profile，常用于 DaVinci still workflow |
| Health | [health-quantification](https://github.com/grapeot/health-quantification) | Apple Health / 手动记录 → SQLite → CLI → AI 分析 |
| Home network | [firewalla-local-skill](https://github.com/grapeot/firewalla-local-skill) | Firewalla 本地导出分析、设备/流量报告和 redacted artifact 工作流；家庭网络细节留在本地 overlay |
| Coffee | [roest-analysis](https://github.com/grapeot/roest-analysis) | Roest roast log 抓取与分析 |
| Intake | [intake-skill](https://github.com/grapeot/intake-skill) | Voice memos / intake workflow 的 public-ready skill |
| Testing | [playwright-test-skill](https://github.com/grapeot/playwright-test-skill) | CDP step-by-step debugging CLI for AI agents writing Playwright E2E tests |
| Semantic search | [semantic-search-skill](https://github.com/grapeot/semantic-search-skill) | 本地文本 embedding + cosine 相似度检索 CLI，支持任意 OpenAI-compatible endpoint，带 atomic cache |
| LLM market data | [open_router_data_scraper](https://github.com/grapeot/open_router_data_scraper) | 定期抓取 OpenRouter 模型流量数据（token 用量、请求数、排名），存入本地 SQLite 突破 31 天 trailing window |

## 选择原则

如果一个能力需要完整 CLI、测试、fixtures 或长期维护，把它做成独立 repo。`context-infrastructure` 只链接它，不复制它。这样用户可以按需安装，不会让 starter workspace 变成巨大的工具合集。

如果一个能力只是通用工作方法，例如深度调研、并行 subagent、分析写作、skill 写作、项目脚手架，可以留在本仓库的 `rules/skills/`。这些文件是 reference implementation 的核心，clone 后就能阅读和改造。

如果一个能力依赖私人数据、私人账号或业务上下文，把通用部分放 public repo，把私人部分留在用户自己的 workspace overlay。不要把真实联系人、服务器、路径、API key、客户名、交易数据或使用记录写进 public repo。
