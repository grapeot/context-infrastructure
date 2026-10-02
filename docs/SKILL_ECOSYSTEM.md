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
| Web search | [firecrawl-skill](https://github.com/grapeot/firecrawl-skill) | 使用 Firecrawl v2 的搜索/提取 CLI，纯标准库没有第三方依赖。命令行和 JSON 输出完全兼容 tavily-skill，可以直接平替。搜索默认包含网页全文 Markdown，网页提取支持按查询高亮，调用前会在 stderr 输出 credit 预估 |
| Documents | [gdocs-skill](https://github.com/grapeot/gdocs-skill) | Google Docs 创建、搜索、修改、分享，支持 Markdown 和 tab |
| Maps / travel | [google-maps-routing-skill](https://github.com/grapeot/google-maps-routing-skill) | Google Maps Routes + Geocoding CLI，支持地址解析、实时 drive time 和 leave-by 规划 |
| Domains / DNS | [go-daddy-skill](https://github.com/grapeot/go-daddy-skill) | GoDaddy 域名与权威 DNS read-first CLI；完整清单、敏感字段脱敏，以及独立 write PAT 保护的 TXT create plan/apply |
| Cloud operations | [koyeb-skill](https://github.com/grapeot/koyeb-skill) | 基于官方 Koyeb CLI 5.12.0 的 Markdown 运维技能与轻量凭证加载器，从 `.env` 读取字面 key 或通过 1Password 解析 `op://` 引用。覆盖应用与实例盘点、构建和运行时日志、授权配置变更、休眠与扩缩容，并结合配置回读、部署状态和线上入口核验结果 |
| Email | [outlook_skill](https://github.com/grapeot/outlook_skill) | Outlook.com 邮件下载、归档、Markdown 渲染、发送和日历邀请 |
| Email | [resend_email_skill](https://github.com/grapeot/resend_email_skill) | Resend 自定义域名发信、收件读取、Markdown 导出和附件检查 |
| Email / newsletter | [kit-skill](https://github.com/grapeot/kit-skill) | Kit Broadcast Markdown 发信 CLI，支持 dry-run、draft-only、web-only 和 tag/segment 定向；账号默认值放本地 overlay |
| Messaging | [imessage_skill](https://github.com/grapeot/imessage_skill) | macOS iMessage send-only CLI；联系人 alias 放本地 overlay |
| Agent operations | [opencode_skill](https://github.com/grapeot/opencode_skill) | OpenCode `submit` / `submit --dry-run` / batch submission、recurring cron workflow、SQLite 数据维护和 archive |
| Agent operations | [ai-agent-cli-skill](https://github.com/grapeot/ai-agent-cli-skill) | 用文件响应方式非交互调用 Claude Code、Codex、OpenCode、Antigravity、Grok Build；只暴露一个 root skill，CLI 细节按需加载 |
| Agent authentication | [chat-gpt-oauth-skill](https://github.com/grapeot/chat-gpt-oauth-skill) | 用户需自行订阅 ChatGPT Plus/Pro 并在本地手动授权；提供 browser PKCE、明文 token lifecycle、refresh 与最小 Codex Responses 示例。仅推荐 owner experiment，兼容 endpoint 不稳定，不用于生产 |
| Agent authentication | [grok-oauth-skill](https://github.com/grapeot/grok-oauth-skill) | 用户需自行订阅 SuperGrok / X Premium+ 并在本地手动授权；提供 browser PKCE、device code、明文 token lifecycle、refresh 与最小 xAI Chat Completions 示例。仅推荐 owner experiment，兼容 endpoint 不稳定，不用于生产 |
| Agent operations | [ai_session_export](https://github.com/grapeot/ai_session_export) | 将 OpenCode、Claude Code、Codex、Antigravity 和 Second Mind 会话增量导出为统一 Markdown 归档，供浏览和检索 |
| Usage analytics | [ai-session-profanity-rate](https://github.com/grapeot/ai-session-profanity-rate) | 对本地 AI session 的人类 user message 做 sub-agent 粗口词元计数，提供版本化 cache、脱敏 JSON、每日 incidence 和模型构成图；真实会话与结果留在本地 |
| Agent operations | [process-launcher](https://github.com/grapeot/process-launcher) | 本地 HTTP process launcher，适合 TCC / GUI 权限桥接、durable one-shot delayed jobs、进程日志 and 取消 |
| Agent operations | [opencode-docker](https://github.com/grapeot/opencode-docker) | Docker 部署模版，用于快速配置 OpenCode Server 容器化运行环境 |
| Usage analytics | [ai_usage_dashboard](https://github.com/grapeot/ai_usage_dashboard) | 多平台 AI token usage、成本估算、本地 dashboard 和 E1002 JSON |
| Social / growth | [typefully-twitter-skill](https://github.com/grapeot/typefully-twitter-skill) | Typefully 发帖、账号指标和 X/Twitter 单帖 analytics |
| Community publishing | [circle-post-skill](https://github.com/grapeot/circle-post-skill) | Circle community Markdown conversion, dry-run preflight, publish/update/delete CLI；社区默认值放本地 overlay |
| Payments / growth | [stripe-skill](https://github.com/grapeot/stripe-skill) | Stripe 只读 finance / sales analytics，live tests 默认 opt-in |
| Media | [online-media-skill](https://github.com/grapeot/online-media-skill) | 在线媒体下载、ASR artifact、query pack、source identification，以及 Agent 主导的双语 SRT：Agent 负责纠错、语义断句和翻译，CLI 负责 coverage、render 和 validate |
| Photos | [apple-photos-skill](https://github.com/grapeot/apple-photos-skill) | macOS Photos metadata 搜索、筛选、导出和备份，以及默认 dry-run、显式授权的 PhotoKit import/delete；当前 mutation 能力为 live-unverified alpha，不用于 production library |
| Family media | [bright-horizons-photo-sync-skill](https://github.com/grapeot/bright-horizons-photo-sync-skill) | 增量备份已授权家庭账号可见的 My Bright Day 事件与媒体，支持断点续传、完整性校验和 macOS Photos 去重导入；凭证与家庭数据留在本地 |
| Slides | [presentation_skill](https://github.com/grapeot/presentation_skill) | 默认 image-generated full-slide deck；明确不用图像生成时 fallback 到 HTML module deck |
| Slides | [pptx.skill](https://github.com/grapeot/pptx.skill) | AI-first PPTX 读取、编辑和渲染 |
| Images | [image-generation-skill](https://github.com/grapeot/image-generation-skill) | Gemini Flash / Gemini Pro / GPT-Image-2 文生图、图片编辑、分辨率放大 |
| Voice clone | [tts-clone-skill](https://github.com/grapeot/tts-clone-skill) | Gemini 3.8 Flash TTS 声音复制与本地 Qwen3-TTS 克隆：同意句校验、24 kHz WAV、voice key 不进 stdout |
| 3D / animation | [gpt_3d_skill](https://github.com/grapeot/gpt_3d_skill) | 专为用好 GPT-6 跃升后的三维建模能力而设计：通过参考分解、材质、镜头编排与反复视觉检查，改善缺少方法时仍停留在粗糙 demo 的问题。引导制作 Blender 模型、动画与 Three.js 网页漫游，含角色绑骨与本地动捕工作流 |
| Music | [zun-music-skill](https://github.com/grapeot/zun-music-skill) | 把公有领域旋律改编成 ZUN（东方 Project 作曲者）风格的短乐句（通常 8 小节约 15 秒）：保留原曲强拍骨架并自动校验，叠加 ZUN 进行、3-3-2 切分、16 分音符装饰、小号+钢琴主旋律和机械感鼓组，用 FluidSynth + 东方向 SoundFont 渲染 MIDI/MP3，并提供局域网试听页做 A/B 对比；含公有领域边界和真实多轮试听踩坑 |
| Video | [opus-video-audio-skill](https://github.com/grapeot/opus-video-audio-skill) | 专为 Claude Opus 设计与验证：用代码逐帧渲染短视频并按分镜配乐或对齐歌曲。画面侧覆盖先定概念并由独立 critic 逐轮审阅、按真实角大小定焦段、线性合成与一次 tone map、光晕/倒影/屏幕文字的常见坑、防止审阅旧帧的逐帧验收、关键帧拼图与手机预览；支持解说旁白（TTS 转录校验与字幕）及随现成歌曲剪辑（分轨测算、节拍与唱句吸附到真实起音、鼓点包络驱动辉光、单画布揭示、把歌词放在画面空白处）；音频侧用 MIDI + FluidSynth 让音符落在画面节拍上，也能铺旁白下的垫乐，因 agent 听不见而以时长、峰值、RMS 包络和频谱质心客观校验并做标准化。附 check_frames、score_cue 等 5 个 CLI 及 lib/opusvid 库；未在其他模型上测试 |
| iOS 开发 | [ios-development-skill](https://github.com/grapeot/ios-development-skill) | 直接调用 xcodebuild、simctl 与 devicectl 不经封装 CLI；覆盖模拟器 UI 测试与快速测试循环、配对 iPhone 免 Xcode 部署与真机 benchmark，以及 App Store Connect 归档导出与授权上传 |
| Portraits | [genai_portrait_skill](https://github.com/grapeot/genai_portrait_skill) | vision agent 驱动的人像、头像和证件照编辑；强调身份保真、摄影整体一致性、多图灯光迁移和 alpha 输出 |
| Images | [tiff-icc-profile](https://github.com/grapeot/tiff-icc-profile) | 给未标记 TIFF 嵌入 ICC profile，常用于 DaVinci still workflow |
| Health | [health-quantification](https://github.com/grapeot/health-quantification) | Apple Health / 手动记录 → SQLite → CLI → AI 分析 |
| Health / education | [ct-education-skill](https://github.com/grapeot/ct-education-skill) | 支持外部胸部 CT DICOM，提供与原始切片联动的本地交互式 3D 可视化及 Blender 教学影片。仅用于教学，不用于诊断；检查数据及所有衍生产物均私下保存在仓库外。 |
| Home network | [firewalla-local-skill](https://github.com/grapeot/firewalla-local-skill) | Firewalla 本地导出分析、设备/流量报告和 redacted artifact 工作流；家庭网络细节留在本地 overlay |
| Coffee | [roest-analysis](https://github.com/grapeot/roest-analysis) | Roest roast log 抓取与分析 |
| Intake | [intake-skill](https://github.com/grapeot/intake-skill) | Voice memos / intake workflow 的 public-ready skill |
| Testing | [playwright-test-skill](https://github.com/grapeot/playwright-test-skill) | CDP step-by-step debugging CLI for AI agents writing Playwright E2E tests |
| Semantic search | [semantic-search-skill](https://github.com/grapeot/semantic-search-skill) | 本地文本 embedding + cosine 相似度检索 CLI，支持任意 OpenAI-compatible endpoint，带 atomic cache |
| LLM market data | [open_router_data_scraper](https://github.com/grapeot/open_router_data_scraper) | 定期抓取 OpenRouter 模型流量数据（token 用量、请求数、排名），存入本地 SQLite 突破 31 天 trailing window |
| Innovation | [innovation-assistant-skill](https://github.com/grapeot/innovation-assistant-skill) | 将 SIT 与 Think Bigger 编码为带硬校验的可执行流水线，让 Agent 成为结构化创新引擎，产出带推导链的可落地候选方案 |
| Documents | [docx-skill](https://github.com/grapeot/docx-skill) | DOCX inspection and editing scaffold |
| SEO / marketing | [dataforseo-skill](https://github.com/grapeot/dataforseo-skill) | DataForSEO keyword / SERP / ranked keyword API CLI |
| Design | [design_skill](https://github.com/grapeot/design_skill) | UI evaluation and improvement judgment framework |
| Home automation | [smart_home_skill](https://github.com/grapeot/smart_home_skill) | Smart home CLI；device aliases and household details in local overlay |
| E-ink display | [eink_diary](https://github.com/grapeot/eink_diary) | Visual diary generation for e-ink displays |
| Embedded hardware | [m5stack-sticks3-skill](https://github.com/grapeot/m5stack-sticks3-skill) | M5StickS3 板级 bring-up 与实机验收指南；覆盖 Arduino/ESP-IDF、按钮、电源、LCD、IR、ES8311 音频、NVS 和 BLE HID 陷阱，不回显设备 secret |
| Identity | [logto-management-skill](https://github.com/grapeot/logto-management-skill) | 安全发现、审计和管理 Logto 租户配置的 CLI + Python 库；支持租户 Swagger 检索、配置写入强制备份与回读校验、快照 diff、MFA 运维和破坏性操作 dry-run |
| Writing | [writing-skill](https://github.com/grapeot/writing-skill) | 内部写作与外部写作两条工作流，共享诊断词汇表与 L1-L8 thesis catalog，以及确定性中文 prose lint CLI；内部文档降决策摩擦，外部文章防教材声、防认知超载 |
| Writing | [voice-lora](https://github.com/grapeot/voice-lora) | 包含一个随包分发的 0.55 MB 轻量级 CPU 分类器（voice-lora-detect）和一个基于 Qwen3.5-9B 的改写模型（voice-lora-rewrite）。前者评估中文文章的 AI 味并分档，同时标出 AI 腔词；后者用 llama-server 逐段润色，保证结构、论证顺序和事实不变，改写后的文章带有鸭哥（yage.ai）的口吻，在 Mac 上处理 40 段约 45 秒，生成的内容需要复核事实漂移和格式。此外还提供一套反向合成数据的工具链（voice-lora），方便 agent 在有足够个人语料和一张 32 GB 显存 GPU 的前提下训练专属的改写模型和分类器。 |
| Vision | [dinov3-classifier-skill](https://github.com/grapeot/dinov3-classifier-skill) | 把未标注图像转成精简本地视觉模型的完整流程：主动采样、人机校准、ONNX 导出、低成本端侧部署 |

## 选择原则

如果一个能力需要完整 CLI、测试、fixtures 或长期维护，把它做成独立 repo。`context-infrastructure` 只链接它，不复制它。这样用户可以按需安装，不会让 starter workspace 变成巨大的工具合集。

如果一个能力只是通用工作方法，例如深度调研、并行 subagent、分析写作、skill 写作、项目脚手架，可以留在本仓库的 `rules/skills/`。这些文件是 reference implementation 的核心，clone 后就能阅读和改造。

如果一个能力依赖私人数据、私人账号或业务上下文，把通用部分放 public repo，把私人部分留在用户自己的 workspace overlay。不要把真实联系人、服务器、路径、API key、客户名、交易数据或使用记录写进 public repo。
