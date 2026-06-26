# AI 简报 Vol.1 | 2026年6月26日

> 本周最值得关注的几件事：美国政府出手干预前沿模型发布，OpenAI 发布自研推理芯片，DeepSeek 完成中国 AI 史上最大单轮融资，Vercel 给 agent 开发者端上了一个生产级框架。

---

## 美国政府开始管模型发布

这周最大的结构性变化不是哪个新模型，是政府角色的介入。

6月12日，美国政府向 Anthropic 发出出口管制令，要求其立即对所有用户——包括 Anthropic 自家非美籍员工——关闭 Fable 5 和 Mythos 5 的访问权限。理由是"国家安全"，具体依据是有人发现了一个 jailbreak：要求模型读取某个代码库并修复其中的安全漏洞。Anthropic [随即合规执行](https://www.anthropic.com/news/fable-mythos-access)，并公开声明自己认为这是误判——同样的能力在 GPT-5.5 上同样存在，每天被安全防御人员正常使用，不构成下架整个商用模型的理由。

6月25日轮到 OpenAI。白宫国家网络总监办公室和科技政策办公室要求 OpenAI 在 GPT-5.6 发布时先给一小批企业客户，由政府逐案审批接入资格，再考虑更大范围的开放。Sam Altman 在内部全员沟通中说他接受这个安排，但表示这"不是我们希望的长期模式"，预计最终推迟"几周"。

这是美国政府首次在模型公开发布前主动介入。两家公司收到的待遇明显不同：Anthropic 几乎是被命令关停，OpenAI 是被协商延期。[The Verge 指出](https://www.theverge.com/ai-artificial-intelligence/957372/openai-will-delay-gpt-5-6-after-trump-administration-request)，这种差别本身已经在行业里引发了担忧。

对开发者来说，短期影响是 GPT-5.6 的上线时间不确定，Fable 5 / Mythos 5 何时恢复访问也没有明确时间表。如果你的产品在等这两个模型，现在需要重新估计时间线。

---

## OpenAI 自研推理芯片 Jalapeño

6月24日，OpenAI 和 Broadcom 联合发布了第一代自研推理加速器 [Jalapeño](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)。

几个关键数字：从设计到流片（tape-out）只用了九个月，这在高性能 ASIC 领域被认为是史上最快的；Broadcom CEO Hock Tan 称其推理成本大约是现有 GPU 方案的一半；芯片采用 TSMC 3nm 工艺，中央逻辑 tile 旁侧是 8 个 HBM3E 内存堆栈。目前已经在实验室中以生产频率和功耗跑通了 GPT-5.3-Codex-Spark。

定位很清晰：只做推理，不做训练。Google TPU 是训练推理两用，Jalapeño 专注于推理的成本结构。OpenAI 把它定位为"多代平台的第一步"，2026年底开始部署到微软等合作伙伴的数据中心，下一代计划 2028 年左右推出。

[Ars Technica 指出](https://arstechnica.com/gadgets/2026/06/openai-and-broadcom-announce-chip-designed-for-llm-inference-at-scale/)，声称 per-watt 性能"大幅优于现有最优"这件事目前还没有第三方基准测试背书，OpenAI 说详细技术报告"后续数月内"发布。

这里面有一条更长的逻辑：OpenAI 今天最贵的成本是推理。每次用户按下 Enter，都在消耗昂贵的 GPU 计算。拥有自己的推理芯片，不是要甩掉英伟达，而是要把成本曲线重新拉回自己手里。如果 Jalapeño 的性能数字属实，对 OpenAI 的单位经济学影响会非常显著。

---

## DeepSeek 完成史上最大 A 轮

6月16日，[DeepSeek 宣布完成首次外部融资](https://letsdatascience.com/news/deepseek-raises-74-billion-series-a-round-f87c8c65)：约 500 亿人民币（74 亿美元），估值超过 500 亿美元。这是中国 AI 行业迄今最大单轮融资。

融资结构非常特别，值得单独说。腾讯投了约 100 亿人民币，CATL 投了约 50 亿，JD.com、NetEase、IDG Capital 参与，但他们的钱不是直接进入 DeepSeek——而是进入一个由梁文峰本人管理的有限合伙。商业 LP 全部无投票权，五年锁定期。只有国家 AI 产业投资基金拿到了直接股权和投票权。梁文峰自己投了约 200 亿人民币，占整轮将近一半，并且据报道核查了每个 LP 背后的身份，确保没有境外资本混入。

这笔钱主要用于：自建算力基础设施（摆脱对租赁 GPU 的依赖）、下一代模型预训练、企业软件应用扩张。[南华早报报道](https://www.scmp.com/tech/big-tech/article/3357525/how-deepseeks-landmark-funding-secures-liang-wenfengs-grip-chinas-ai-rivalry-heats)称梁文峰在投资人会议上反复强调，DeepSeek 只做一件事：提升模型智能，其他都不感兴趣。

DeepSeek-V4-Flash 连续三周在全球 AI 路由平台排名第一，周处理量 3.6 万亿 tokens。与此同时，核心研究员流失的问题没有掩盖：V3 主要贡献者 Luo Fuli 去了小米，另一位核心研究员 Guo Daya 去了字节跳动。这笔融资有相当一部分是在用钱应对这个问题。

---

## Agent 开发生态：几个可用的东西

Gartner 在 2026 Agentic AI Hype Cycle 报告中给出了一组数字：目前只有 17% 的企业实际部署了 AI agent，但 60% 以上表示会在未来两年内部署——这是他们追踪的所有新兴技术里采用曲线最陡的一个。

这个周期里有几个具体的工具发布值得关注。

**Vercel eve**（6月17日）：Vercel 开源了一个 agent 框架，设计哲学是"durable by default"。每个 agent session 的每一步都有 checkpoint，崩溃或部署重启后可以从中断点恢复。代码执行在沙箱里隔离，本地支持 Docker/microsandbox，线上跑在 Vercel 自己的沙箱基础设施上。内置人工审批机制，支持 MCP server，可以对接 Slack、Discord、GitHub 等渠道。[Vercel 在公告里提到](https://vercel.com/blog/introducing-eve)，今年 agent 触发的部署占比从 3% 增长到了 29%，他们预计很快会超过一半。

**IBM + HuggingFace CUGA**：一个轻量级可组合 agent 框架，YAML 声明式配置，最小化依赖，打包了 24 个从 SQL 查询到 PDF 分析的示例 blueprint。定位是让你一天内跑起来一个 production-ready agent。

**Microsoft Agent Framework**：微软在 Build 2026 上发布了 Agent Harness 和 Claw 概念，一个管理 agent 执行上下文、历史持久化、规划和工具调用的标准化 SDK。正在连载技术文章（Part 2 讲安全数据访问，Part 3-4 还没出）。

对于真正在做 agent 系统的人来说，这几个东西里 Vercel eve 的 durable execution 设计是最值得仔细看的——这解决了 agent 实际部署中最痛的问题：session 不能中途崩，崩了要能续。

---

## 欧盟 AI 法案：8月2日是真实日期

很多合规材料在 5 月 7 日 Digital Omnibus 协议之后就过时了。[高风险 AI 系统的核心合规截止日](https://www.complydrive.ai/articles/the-august-2026-deadline-what-needs-to-be-done-by-when)从 8 月 2 日延期到了 2027 年 12 月 2 日。但以下两类义务**没有延期**：

第一，**Article 50 透明度义务**在 8 月 2 日生效。如果你的产品是与用户对话的 AI 系统，必须明确告知用户他们在与 AI 交互。这不只是加一行免责声明，[监管者会看披露是否清晰、可及、有效](https://datamatters.sidley.com/2026/06/24/eu-ai-act-transparency-obligations-preparing-for-compliance-by-2-august-2026/)。

第二，**GPAI 模型的罚款执法**从 8 月 2 日开始。GPAI 义务本身去年就已生效，但欧盟 AI 办公室对 GPAI 提供方实施罚款的权力从 8 月 2 日激活。上限是 1500 万欧元或全球年营业额的 3%，取其高者。

如果你的产品面向欧盟用户，8 月 2 日是一个具体的行动截止点。

---

## 杂项速记

- **GPT-5.6 / Claude Sonnet 5 谣言**：两个都是"下周发布"反复流传，截至 6 月 26 日都未发布。Claude 当前旗舰是 Opus 4.8（5 月 28 日），Fable 5 已下线；GPT-5.6 因政府干预延期。最可靠的判断方式：等官方 anthropic.com/news 或 openai.com 的公告，不要相信 API 日志里的 slug。

- **DeepSeek-V4-Flash 定价**：在行业普遍涨价时，DeepSeek 宣布 V4-Pro 永久降价 7X%，cache hit 价格约合每百万 token ¥0.025——是 GPT-5 同类使用的 1/14,960。

---

*下期预计 7 月 3 日。如有动态遗漏，欢迎补充。*
