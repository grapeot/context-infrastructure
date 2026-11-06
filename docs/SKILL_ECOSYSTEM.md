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
| 视频导出与转码 | [video_export_skill](https://github.com/grapeot/video_export_skill) | macOS 视频导出与转码 CLI 及配套 skill：支持独立调用 DaVinci Resolve Studio（Deliver 队列导出）与 Apple Compressor（`.compressorsetting` 预设解析与批量转码），也可串联为带 `lsof`/`ffprobe` 校验闸门的流水线；默认 dry-run、显式 `--execute` 执行并写入私有运行清单，已完成 2 秒 SDR 合成测试片端到端实测（不含 HDR/杜比视界主观色彩校验）。 |
| Live monitoring | [bilibili-live-monitor](https://github.com/grapeot/bilibili-live-monitor) | Apple Silicon Mac多路B站直播文本监控：静音Chrome与Web Audio独立采音、本地Qwen3-ASR-1.7B/MLX共享串行转写，复用网页WebSocket解码弹幕并合为每房间时间线，支持SQLite持久化、SSE、全宽全屏自动跟随和JSONL导出。不依赖付费识别API；不展示视频、不做图像理解或音频回放，运行消耗本机算力与网络。 |
| Web search | [tavily-skill](https://github.com/grapeot/tavily-skill) | Tavily search/extract CLI，给 agent 稳定 JSON 输出 |
| Web search | [firecrawl-skill](https://github.com/grapeot/firecrawl-skill) | 使用 Firecrawl v2 的搜索/提取 CLI，纯标准库没有第三方依赖。命令行和 JSON 输出完全兼容 tavily-skill，可以直接平替。搜索默认包含网页全文 Markdown，网页提取支持按查询高亮，调用前会在 stderr 输出 credit 预估 |
| Documents | [gdocs-skill](https://github.com/grapeot/gdocs-skill) | Google Docs 创建、搜索、修改、分享，支持 Markdown 和 tab |
| Maps / travel | [google-maps-routing-skill](https://github.com/grapeot/google-maps-routing-skill) | Google Maps Routes + Geocoding CLI，支持地址解析、实时 drive time 和 leave-by 规划 |
| Domains / DNS | [go-daddy-skill](https://github.com/grapeot/go-daddy-skill) | GoDaddy 域名与权威 DNS read-first CLI；完整清单、敏感字段脱敏，以及独立 write PAT 保护的 TXT create plan/apply |
| Cloud operations | [koyeb-skill](https://github.com/grapeot/koyeb-skill) | 基于官方 Koyeb CLI 5.12.0 的 Markdown 运维技能与轻量凭证加载器，从 `.env` 读取字面 key 或通过 1Password 解析 `op://` 引用。覆盖应用与实例盘点、构建和运行时日志、授权配置变更、休眠与扩缩容，并结合配置回读、部署状态和线上入口核验结果 |
| Cloud GPU | [colab-skill](https://github.com/grapeot/colab-skill) | 用官方 `google-colab-cli` 无头跑 Google Colab 的 GPU/TPU 作业（最高 G4 = RTX PRO 6000 96GB），面向批量数据生成与微调。登录用脚本自动 `open` 授权 URL（无需手动 copy），并写清 G4 的 Premium 档位门槛、按小时计费与会话上限、`/content` 不持久，以及禁止常驻服务等边界。私有账号与档位决策留本地 overlay |
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
| Course operations | [maven-skill](https://github.com/grapeot/maven-skill) | 基于 CDP 连接已登录 Chrome 浏览器，支持课程与班期（Cohort）动态发现，以及报名学员（Enrolled）CSV 导出、格式校验与收据生成 |
| Payments / growth | [stripe-skill](https://github.com/grapeot/stripe-skill) | Stripe 只读 finance / sales analytics，live tests 默认 opt-in |
| Media | [online-media-skill](https://github.com/grapeot/online-media-skill) | 在线媒体下载、ASR artifact、query pack、source identification，以及 Agent 主导的双语 SRT：Agent 负责纠错、语义断句和翻译，CLI 负责 coverage、render 和 validate |
| Speech transcription | [asr-skill](https://github.com/grapeot/asr-skill) | 本地音频转写与说话人分离：CPU Nemotron 做说话人分离，Qwen3-ASR 经 MLX 在 Apple Silicon 识别（macOS 26+ / CPython 3.12）。保留原始时间轴、说话人区间与原始转写，由 Agent 经 prepare-edit、语义清理、finalize-edit 分步生成可读文本，不确定片段按原序保留并附 source map；说话人姓名使用调用方提供的映射或有文本依据的推断，未确认项保留标记。 |
| Photos | [apple-photos-skill](https://github.com/grapeot/apple-photos-skill) | macOS Photos metadata 搜索、筛选、导出和备份，以及默认 dry-run、显式授权的 PhotoKit import/delete；当前 mutation 能力为 live-unverified alpha，不用于 production library |
| Family media | [bright-horizons-photo-sync-skill](https://github.com/grapeot/bright-horizons-photo-sync-skill) | 增量备份已授权家庭账号可见的 My Bright Day 事件与媒体，支持断点续传、完整性校验和 macOS Photos 去重导入；凭证与家庭数据留在本地 |
| Slides | [presentation_skill](https://github.com/grapeot/presentation_skill) | 默认 image-generated full-slide deck；明确不用图像生成时 fallback 到 HTML module deck |
| Slides | [pptx.skill](https://github.com/grapeot/pptx.skill) | AI-first PPTX 读取、编辑和渲染 |
| Images | [image-generation-skill](https://github.com/grapeot/image-generation-skill) | Gemini Flash / Gemini Pro / GPT-Image-2 文生图、图片编辑、分辨率放大 |
| Voice clone | [tts-clone-skill](https://github.com/grapeot/tts-clone-skill) | Gemini 3.8 Flash TTS 声音复制与本地 Qwen3-TTS 克隆：同意句校验、24 kHz WAV、voice key 不进 stdout |
| 3D / animation | [gpt_3d_skill](https://github.com/grapeot/gpt_3d_skill) | 专为用好 GPT-6 跃升后的三维建模能力而设计：通过参考分解、材质、镜头编排与反复视觉检查，改善缺少方法时仍停留在粗糙 demo 的问题。引导制作 Blender 模型、动画与 Three.js 网页漫游，含角色绑骨与本地动捕工作流 |
| 3D / figures | [image-to-figure-skill](https://github.com/grapeot/image-to-figure-skill) | 英文 agent skill 加 Python CLI `img2fig`（MIT）：从一张角色图做出软胶质感的 3D 收藏手办。先用 OpenAI 图像模型出手办风格的 look-dev 和四视图，按背景色列把四视图切成等大的单张；图像模型凭空添加的细节会被 3D 模型照样建出来，所以在图像阶段定点修改后重跑，不去修网格。随后经 fal 做多视图 image-to-3D（默认 Tripo，可选四家对比），再把 Blender 当外部程序调用：与正视图比对自动校正朝向、归一化、减面、软胶材质调色和可选腮红，输出 .blend、干净的 GLB、与四视图逐张对照的渲染图，以及带亚克力底座的转台视频。所有付费调用默认只给出计划和费用估算，加 `--execute` 才执行，并按工作目录账本做预算拦截；每条命令输出单个 JSON，退出码固定，原样透传服务商与 Blender 的错误。附离线测试，在一个自己生成的原创角色上端到端跑通，花费 0.82 美元 |
| Live2D | [live2d-modifier-skill](https://github.com/grapeot/live2d-modifier-skill) | 在保留原有动作和物理绑定的前提下，结合外部图像编辑根据描述或参考图对已绑定的Live2D模型进行配色、空间渐变、服装纹样和妆容的修改，支持贴图拆页保署名，接缝修补以及换名安装到VTube Studio。 |
| Music | [orchestral-midi-skill](https://github.com/grapeot/orchestral-midi-skill) | 英文 MIT 管弦乐 Skill 与 Python CLI，单根入口路由至 Art 与 Science。Art 指导 Agent 完成声部角色、乐句呼吸、真实拍号速度、同音重复起音与真短弓等总谱决策，由 CLI 编译显式乐谱 JSON，而非任意 MIDI 自动改编器；Science 渲染按奏法分轨的 SF2/FluidSynth 与 SFZ/sfizz 单声道分轨，合成镜像源早反射与统计混响尾，匹配 LUFS 并校验真峰值，输出附溯源元数据的实测 SOFA 固定头位直达、早反射、厅堂与普通立体声对比。授权 MIDI、音色库与 HRTF 由用户自备。 |
| Music | [zun-music-skill](https://github.com/grapeot/zun-music-skill) | 把公有领域旋律改编成 ZUN（东方 Project 作曲者）风格的短乐句（通常 8 小节约 15 秒）：保留原曲强拍骨架并自动校验，叠加 ZUN 进行、3-3-2 切分、16 分音符装饰、小号+钢琴主旋律和机械感鼓组，用 FluidSynth + 东方向 SoundFont 渲染 MIDI/MP3，并提供局域网试听页做 A/B 对比；含公有领域边界和真实多轮试听踩坑 |
| Video | [opus-video-audio-skill](https://github.com/grapeot/opus-video-audio-skill) | 专为 Claude Opus 设计与验证：用代码逐帧渲染短视频并按分镜配乐或对齐歌曲。画面侧覆盖先定概念并由独立 critic 逐轮审阅、按真实角大小定焦段、线性合成与一次 tone map、光晕/倒影/屏幕文字的常见坑、防止审阅旧帧的逐帧验收、关键帧拼图与手机预览；支持解说旁白（TTS 转录校验与字幕）及随现成歌曲剪辑（分轨测算、节拍与唱句吸附到真实起音、鼓点包络驱动辉光、单画布揭示、把歌词放在画面空白处）；音频侧用 MIDI + FluidSynth 让音符落在画面节拍上，也能铺旁白下的垫乐，因 agent 听不见而以时长、峰值、RMS 包络和频谱质心客观校验并做标准化。附 check_frames、score_cue 等 5 个 CLI 及 lib/opusvid 库；未在其他模型上测试 |
| Video | [vlog-skill](https://github.com/grapeot/vlog-skill) | 人在回路地制作口播讲解视频：画面里是说话人自己的 HeyGen 数字分身，念的是说话人自己录制、再经剪辑的旁白，不用 TTS。覆盖调研与来源契约、按实测语速写稿、真人一次录完；`vlog` CLI 用词级 ASR（Qwen3-ASR，Apple Silicon）和实测静音区间剪掉重录、口头说出的剪辑指令、填充词与讲错的说法，以等功率交叉淡化渲染并记录时间映射与响度，再重新转写逐个核验接缝。HeyGen 渲染后测量音画漂移，以数字人视频自身的转写作为画面时钟；画面从论证地图出发（常驻地图 + 逐论点舞台）降低观众认知负担，并生成带术语表的字幕。agent 听不见声音，试听与终审留给人，也从不发布。提炼自一部约 18 分钟的中文讲解片；B-roll 帧与配乐交给 opus-video-audio-skill，最终合成不在 CLI 里，最终 QA 尚未实跑 |
| Video publishing | [bilibili-upload-skill](https://github.com/grapeot/bilibili-upload-skill) | 中文 agent skill 加 `bili-upload` CLI：用 Playwright 经 CDP 接入一个使用独立持久本机 profile 的可见 Chrome，替视频所有者填写 B 站（哔哩哔哩）投稿表单，包括选视频（拦截文件选择框，绕开经 CDP 远程传文件的 50 MB 上限）、标题、简介、标签、4:3 与 16:9 两张封面、创作声明、分区、`.srt` 字幕、章节、可见范围和粉丝动态，逐项读回核对后停在「立即投稿」之前，由人核对并亲手提交。所有点击都经过点击守卫，拒绝提交和存草稿类按钮；登录由人扫码完成，工具不读取、不导出 cookie；`fill` 默认只做 dry-run。附设计说明，解释为什么走可见浏览器，而不用非官方接口或官方开放平台。各步骤的页面交互已在真实投稿页（2026-10）上逐项验证，完整的 `--execute` 流程尚未端到端跑通过一次；不用于批量或无人值守投稿 |
| Video publishing | [youtube-upload-skill](https://github.com/grapeot/youtube-upload-skill) | 英文agent skill + CLI `yt-upload`: 用官方YouTube Data API v3，不用浏览器自动化。默认离线dry-run校验元数据、渲染章节和估算配额，必填儿童与合成媒体属性；执行时支持分块断点续传、按文件哈希防重、设置封面、传字幕、加入已有播放列表并逐项读回核对。可见范围默认private，只有单次显式指定才用unlisted，不设公开或定时，由频道主人在Studio发布，不删改已有视频；附引导式一次性配置（登录和授权由人完成），有完整离线测试，在真实频道上用unlisted跑过一次端到端上传（同意屏幕的发布由人手动完成；合成内容声明需在Studio确认），不适合批量上传、无人值守发布或搬运内容。 |
| Meeting recordings | [zoom-recording-skill](https://github.com/grapeot/zoom-recording-skill) | 基于英文agent skill + Python CLI `zoom-rec` (MIT license) 实现查找/查看/下载本人Zoom云端录制的MP4视频/M4A音频/带有每行发言人姓名的WebVTT音频转录文件（可以和`circle-client-skill`的`subtitles`模块组合实现双语字幕）/TXT聊天记录/WebVTT CC字幕等功能。无需任何Zoom Marketplace上的app或者API凭证，使用Playwright通过CDP协议连接一个使用指定持久化配置目录的可见Chrome浏览器窗口（在连接前会检查该端口上的浏览器进程是否用这个配置目录启动，如果不是则拒绝连接）。人肉手动登录（不会自动登录，不会读取/打印/导出任何cookie/token）。因为要调用Zoom录制的网页上一些未公开的内部接口，可能会随着Zoom网页的改版而失效（报错时会打印出来是什么接口）。提供`browser`，`status`，`list`（支持突破网页默认的365天的限制，可以查询任何日期的录制，支持主题搜索和分页），`show`，`download`命令，且都只会输出一个JSON对象。使用request和click守卫来保证对Zoom的访问是完全只读的，只会触发下载按钮和确认弹窗，不会删除/修改/分享/更改任何设置，也不会打印/保存签名的下载链接。`download`命令默认只会输出计划而不真的去下载文件，加`--execute`选项才会真的下载（按16MB一块下载，支持`.part`后缀的断点续传），会校验文件大小，记录sha256，对比服务端的ETag和md5，使用ffprobe来检查视频和音频流以及时长与Zoom记录的偏差是否在2秒内，检查WebVTT是否合格，生成一个`manifest.json`文件记录每场的下载情况，下次重跑会跳过已经下载成功的文件。已经通过了121项离线测试（均在CI中），并且在真实账号中成功列出了46场录制，下载了5场会议（每场会议下载5个文件，文件大小/ETag完全匹配，视频时长误差在0.1秒内），成功测试了中断后续传功能。不适合全公司批量归档，获取当前登录账号不可见的录制，无人值守运行。 |
| iOS 开发 | [ios-development-skill](https://github.com/grapeot/ios-development-skill) | 直接调用 xcodebuild、simctl 与 devicectl 不经封装 CLI；覆盖模拟器 UI 测试与快速测试循环、配对 iPhone 免 Xcode 部署与真机 benchmark，以及 App Store Connect 归档导出与授权上传 |
| Portraits | [genai_portrait_skill](https://github.com/grapeot/genai_portrait_skill) | vision agent 驱动的人像、头像和证件照编辑；强调身份保真、摄影整体一致性、多图灯光迁移和 alpha 输出 |
| Images | [tiff-icc-profile](https://github.com/grapeot/tiff-icc-profile) | 给未标记 TIFF 嵌入 ICC profile，常用于 DaVinci still workflow |
| Health | [health-quantification](https://github.com/grapeot/health-quantification) | Apple Health / 手动记录 → SQLite → CLI → AI 分析 |
| Health / education | [ct-education-skill](https://github.com/grapeot/ct-education-skill) | 支持外部胸部 CT DICOM，提供与原始切片联动的本地交互式 3D 可视化及 Blender 教学影片。仅用于教学，不用于诊断；检查数据及所有衍生产物均私下保存在仓库外。 |
| Home network | [firewalla-local-skill](https://github.com/grapeot/firewalla-local-skill) | Firewalla 本地导出分析、设备/流量报告和 redacted artifact 工作流；家庭网络细节留在本地 overlay |
| Home network | [unifi-skill](https://github.com/grapeot/unifi-skill) | 自建 UniFi Network Controller 的只读 CLI：`status` 看每台 AP 的 RF 与信道占用，`clients` 查终端清单并支持信号强度和频段筛选，`aps` 列设备清单（含 `snmp_location`），`wlan` 列 SSID，`export` 生成带时间戳的配置快照；统一 `{command,input,data}` 信封，退出码 0/2/10/12/13，纯标准库 Python，浏览器 cookie 鉴权。硬约束是只读：设计上不做任何 RF、SSID 或配置写入，改配置仍然回到 Controller GUI，因此 coding agent 可以安全观察家庭网络 RF 状态（信道拥塞、弱信号终端、IoT band steering），但不具备改动它的能力 |
| Coffee | [roest-analysis](https://github.com/grapeot/roest-analysis) | Roest roast log 抓取与分析 |
| Intake | [intake-skill](https://github.com/grapeot/intake-skill) | Voice memos / intake workflow 的 public-ready skill |
| Voice Memos | [voice-memos-skill](https://github.com/grapeot/voice-memos-skill) | macOS Apple Voice Memos 只读CLI (`doctor`, `list`, `get`, `export`)，基于数据库 `ZEVICTIONDATE` 区分有效和残留已删录音，无转码导出原生 `m4a`/`qta` 音频并校验大小和SHA-256。 |
| Testing | [playwright-test-skill](https://github.com/grapeot/playwright-test-skill) | CDP step-by-step debugging CLI for AI agents writing Playwright E2E tests |
| Semantic search | [semantic-search-skill](https://github.com/grapeot/semantic-search-skill) | 本地文本 embedding + cosine 相似度检索 CLI，支持任意 OpenAI-compatible endpoint，带 atomic cache |
| LLM market data | [open_router_data_scraper](https://github.com/grapeot/open_router_data_scraper) | 定期抓取 OpenRouter 模型流量数据（token 用量、请求数、排名），存入本地 SQLite 突破 31 天 trailing window |
| Innovation | [innovation-assistant-skill](https://github.com/grapeot/innovation-assistant-skill) | 将 SIT 与 Think Bigger 编码为带硬校验的可执行流水线，让 Agent 成为结构化创新引擎，产出带推导链的可落地候选方案 |
| Documents | [docx-skill](https://github.com/grapeot/docx-skill) | DOCX inspection and editing scaffold |
| SEO / marketing | [dataforseo-skill](https://github.com/grapeot/dataforseo-skill) | DataForSEO keyword / SERP / ranked keyword API CLI |
| Design | [design_skill](https://github.com/grapeot/design_skill) | UI evaluation and improvement judgment framework |
| Home automation | [smart_home_skill](https://github.com/grapeot/smart_home_skill) | Smart home CLI；device aliases and household details in local overlay |
| Home automation | [narwal-skill](https://github.com/grapeot/narwal-skill) | 基于 9002 端口本地 WebSocket 的轻量只读 Python CLI 与 Agent 技能，无需云端账号或 Home Assistant。支持状态快照、户型地图、有界遥测与连接诊断。Flow 2 已完成真机冒烟测试，其他部分 Flow/Freo 机型仍为协议候选。 |
| Home cameras | [niview-skill](https://github.com/grapeot/niview-skill) | 腾讯云 NiView 摄像头 Python CLI：以 0600 权限保存会话 token，列出设备和移动事件，下载并 AES 解密 `.encrypt` 抓拍，以 SQLite 去重做云端轮询；不实现 live P2P，也不唤醒电池摄像头。 |
| E-ink display | [eink_diary](https://github.com/grapeot/eink_diary) | Visual diary generation for e-ink displays |
| Embedded hardware | [m5stack-sticks3-skill](https://github.com/grapeot/m5stack-sticks3-skill) | M5StickS3 板级 bring-up 与实机验收指南；覆盖 Arduino/ESP-IDF、按钮、电源、LCD、IR、ES8311 音频、NVS 和 BLE HID 陷阱，不回显设备 secret |
| Identity | [logto-management-skill](https://github.com/grapeot/logto-management-skill) | 安全发现、审计和管理 Logto 租户配置的 CLI + Python 库；支持租户 Swagger 检索、配置写入强制备份与回读校验、快照 diff、MFA 运维和破坏性操作 dry-run |
| Writing | [writing-skill](https://github.com/grapeot/writing-skill) | 内部写作与外部写作两条工作流，共享诊断词汇表与 L1-L8 thesis catalog，以及确定性中文 prose lint CLI；内部文档降决策摩擦，外部文章防教材声、防认知超载 |
| Writing | [voice-lora](https://github.com/grapeot/voice-lora) | 包含一个随包分发的 0.55 MB 轻量级 CPU 分类器（voice-lora-detect）和一个基于 Qwen3.5-9B 的改写模型（voice-lora-rewrite）。前者评估中文文章的 AI 味并分档，同时标出 AI 腔词；后者用 llama-server 逐段润色，保证结构、论证顺序和事实不变，改写后的文章带有鸭哥（yage.ai）的口吻，在 Mac 上处理 40 段约 45 秒，生成的内容需要复核事实漂移和格式。此外还提供一套反向合成数据的工具链（voice-lora），方便 agent 在有足够个人语料和一张 32 GB 显存 GPU 的前提下训练专属的改写模型和分类器。 |
| Vision | [dinov3-classifier-skill](https://github.com/grapeot/dinov3-classifier-skill) | 把未标注图像转成精简本地视觉模型的完整流程：主动采样、人机校准、ONNX 导出、低成本端侧部署 |
| Calendar | [apple-calendar-skill](https://github.com/grapeot/apple-calendar-skill) | 通过本地数据库快照只读查询 Apple Calendar 的轻量 CLI 与 Agent 技能，直接以只读模式读取数据库及 sidecar 文件，无需 TCC 自动化权限。提供 `calendars`、`list`、`search`、`get` 与 `selftest` 五项命令，以 JSON 格式输出日历清单、按日期区间过滤日程并检索事件详情。针对底层存储基于 2001 年 Cocoa 参考时刻绝对秒数的机制，工具在结构上严格保证时间语义，同时输出 `start_utc` 真值与 `start_local` 本地显示时间，避免墙钟误读。包含 31 项离线 pytest 单元测试并通过 GitHub Actions CI，内置 `selftest` 在真实数据库上校验七项不变式。 |

## 选择原则

如果一个能力需要完整 CLI、测试、fixtures 或长期维护，把它做成独立 repo。`context-infrastructure` 只链接它，不复制它。这样用户可以按需安装，不会让 starter workspace 变成巨大的工具合集。

如果一个能力只是通用工作方法，例如深度调研、并行 subagent、分析写作、skill 写作、项目脚手架，可以留在本仓库的 `rules/skills/`。这些文件是 reference implementation 的核心，clone 后就能阅读和改造。

如果一个能力依赖私人数据、私人账号或业务上下文，把通用部分放 public repo，把私人部分留在用户自己的 workspace overlay。不要把真实联系人、服务器、路径、API key、客户名、交易数据或使用记录写进 public repo。
