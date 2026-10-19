# 并行 Subagent 工作流

## 元数据

- **类型**: Workflow
- **适用场景**: 独立 review、并行调研探索与用户明确要求的实现委派
- **创建日期**: 2026-02-20
- **最后更新**: 2026-10-18

---

## 核心判断

Subagent 的主要价值不是模拟人类团队，也不是把一个普通任务包装得更复杂。它解决的是三类具体问题：

1. **上下文窗口隔离**：让不同 agent 各自持有一段可控上下文，避免主线程同时塞入大量文件、网页、日志和中间判断。
2. **并行读与独立探索**：让多个 agent 同时搜索、阅读、定位、复核，减少单一路径依赖。
3. **交叉验证**：让不同 agent 在有意重叠的范围内独立得出结论，用一致和分歧暴露遗漏、误读和假设冲突。

外部经验也指向同一个结论：multi-agent 在 research-heavy、read-heavy、高价值任务上更容易成立；在需要多个 agent 共享大量状态、连续协调写入、实时互相修正的任务上成本高且脆弱。Anthropic 的 multi-agent research system 把它定位为用更多 token 换更强的并行探索和压缩能力，并明确提到 multi-agent 可能消耗约 15 倍于普通 chat 的 token；LangChain 的经验则强调 read-heavy 比 write-heavy 更适合并行，因为写操作会携带隐含决策，合并冲突代价高。

调研依据：Anthropic Engineering《How we built our multi-agent research system》（https://www.anthropic.com/engineering/multi-agent-research-system）、LangChain《How and when to build multi-agent systems》（https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems）、Cemri et al.《Why Do Multi-Agent LLM Systems Fail?》（https://arxiv.org/abs/2503.13657）。

## 委派边界与何时使用并行模式

先决定是否委派，再决定是否并行：实现默认主线程亲自做，仅用户明确要求委派实现时才分派。多文件、模块独立、省上下文或模型便宜均不构成授权。已选写作 workflow 仍可指定 writer，不与代码实现混同。

Code / privacy / design review 通常交独立 subagent 或 Antigravity CLI 获取 fresh context，主线程最终验收；轻微低风险局部变更可按比例自检。单次 review 不受下方多路并行门槛限制。广泛调研探索可按独立维度拆分多个 subagent。

启动多个 subagent 并行时，满足以下条件中的至少 2 条，且没有命中下方反模式：

1. **信息面宽**：需要查多个文件、多个网页、多个数据源、多个时间段，主线程一次性读完会污染上下文。
2. **可拆分为独立读任务**：能分成至少 2 个相对独立的探索方向，每个方向预期需要 ≥5 个 tool call。
3. **需要独立判断**：需要反方审稿、事实核查、竞品对照、代码审查、方案对比，单一路径容易自我确认。
4. **存在高价值不确定性**：任务结果会影响后续决策、公开输出、代码改动或成本较高的行动，多花 token 值得。
5. **主线程需要保留设计/整合能力**：主 agent 应把注意力用在拆分问题、设定标准、整合证据和最终判断，而不是埋在低层搜索或重复读取里。

不满足多路并行条件时，主线程直接执行或按需发起单次独立 review，不为并行凑数。

## 反模式

以下情况默认不拆分为多 subagent；任务价值不能替代实现委派所需的用户明确请求：

1. **单点小任务**：只需读 1-2 个文件或做轻微局部改动，无需机械拆分；单次独立 review 按风险判断，不能仅因文件少跳过隐私或关键设计审阅。
2. **强顺序依赖**：下一步必须依赖上一步输出，拆出去只会制造等待和交接成本。
3. **共享状态写入**：多个 agent 同时改同一批文件、同一张表、同一份文案，冲突和隐含决策难以合并。
4. **上下文必须完整共享**：每个 agent 都必须知道全量背景才能做对，拆分后只会丢条件。
5. **验证标准不清**：没有可核对的输出格式、证据要求或验收条件，多个 agent 只会产出多份模糊总结。

## 任务类型参考

| 任务类型 | 是否适合 | 推荐方式 |
|---|---|---|
| 外部调研、论文/产品/市场 survey | 高 | 3-5 个 agent，按证据功能切分，30-50% overlap |
| 大型代码库理解、文件定位、架构梳理 | 高 | `explore` 并行按模块或问题切分，主线程整合 |
| 代码 / 隐私 / 设计 review、方案审稿、事实核查 | 高 | 通常 1 个独立 reviewer；复杂高风险任务可多视角审阅，主线程验收 |
| Brainstorm、反方观点、thesis 压力测试 | 中高 | 不同 agent 指定不同判断视角，输出必须回答同一组问题 |
| 工程与代码实现（含多文件） | 默认不委派 | 仅用户明确要求委派实现时分派；主线程保留合并与测试验收责任 |
| 单 bug 修复、局部编辑、格式调整 | 低 | 主线程直接做 |
| 多 agent 同时写同一文件或同一状态 | 低 | 避免；先独立读/审阅，再由主线程、获授权实现者或写作 workflow 的单一 writer 写 |

---

## 并行执行流程

### 1. 评估与分割

单次独立 review 不必拆分；确需并行时，识别 2-5 个维度，再确定 overlap：

| 任务类型 | Overlap 范围 | 原因 |
|---------|-------------|------|
| 调研 / 多视角审阅 / 创造性任务 | 30% - 50% | 交叉验证、查漏补缺 |
| 代码库探索 / 用户明确要求委派的实现 | 0% - 20% | 减少重复，保留接口边界重叠 |

不要把 overlap 理解成重复劳动。好的 overlap 是让相邻 agent 在最容易出错的边界区域共同覆盖，例如官方 claim 和独立证据的交界、模块接口、数据口径、反对意见。

### 2. 并行启动

**以运行时 schema 为准。** 核对 `functions.task`、目标 agent 与参数是否可用；缺少工具或指定能力时说明边界，不编造调用或静默切模型。单次 review 直接调用；同批多个就绪任务用 `multi_tool_use.parallel` 同消息启动。

**支持时默认 `background: true`。** 后台完成走自动通知，不轮询、不 sleep 查进度；等待期间可做其他工作或结束本轮。仅不支持异步或确需阻塞取结果时同步执行。异步跨消息仍可能并发；同批就绪任务仍同消息启动。

下例仅用于 schema 支持 `background` 的环境，否则省略该字段。启动回执不是完成结果。新任务不传空 `task_id` / `command`，`task_id` 仅用于续写已有任务。

```json
{
  "tool_uses": [
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "官方叙事",
        "subagent_type": "general",
        "prompt": "读取/搜索官方来源，提取 claim、URL、原文摘录，写入 tmp/<session>/tier1_official.md",
        "background": true
      }
    },
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "独立体验",
        "subagent_type": "general",
        "prompt": "搜索独立用户体验、社区讨论、GitHub issues，写入 tmp/<session>/tier3_independent.md",
        "background": true
      }
    },
    {
      "recipient_name": "functions.task",
      "parameters": {
        "description": "竞品对比",
        "subagent_type": "general",
        "prompt": "做竞品矩阵和 thesis verdict，写入 tmp/<session>/competitive_context.md",
        "background": true
      }
    }
  ]
}
```

工具层调用形式是 `multi_tool_use.parallel`，其中每一项是一个 `functions.task`。`subagent_type` 是 OpenCode 原生 agent 名，不是模型名，也不是旧 `category`。OpenCode 会执行 `agent.get(subagent_type)`；找不到同名 agent 就报 `Unknown agent type`。

内置 agent 与自定义 agent 的来源：

- `general` / `explore` 是 OpenCode 源码内置 agent。
- 其他命名 agent 来自 `~/.config/opencode/opencode.json`、项目 `opencode.json`，或 `.opencode/agent(s)/*.md`。
- `provider/model` 只是底层模型入口，不能代替已注册 agent 名。

能力路由仅在已经决定委派后生效，不授予实现委派权限。用户当前明确指定的模型、agent 或 CLI 优先于默认能力路由，仍须满足运行时能力与数据边界；指定载体不可用时报告阻塞，不自行替换。名称以当前注册配置为准：

| subagent_type | 适用场景 |
|---|---|
| `general` | 通用任务；未配置模型时继承主会话模型。适合普通并行执行，但不要假设它是便宜模型 |
| `explore` | 代码库内部快速搜索、文件定位、架构理解 |
| 已注册专项 agent | 按审阅、推理、编码、初筛或数据边界匹配；不在本文件固定模型映射 |
| Antigravity CLI（非 `functions.task`） | 独立 review 或已选写作 workflow；先读已安装的 `ai-agent-cli` 根 skill 和 Antigravity focused skill，按当前可用模型调用，不与 Gemini subagent 混同 |

每个 subagent 的 prompt 应包含：
- 具体负责的维度/范围
- 预期的 overlap 区域（让 agent 知道其他人也在看这部分）
- 输出格式要求
- 输出落盘路径（例如 `tmp/<session_slug>/tier3_independent.md`）
- 验证标准：哪些证据算有效，哪些情况必须标注不确定
- 总 deadline、日志、失败停止条件与唯一写入范围；独立 reviewer 原则上只写审阅产物，由主线程或获授权实现者修复

独立 review 使用未参与该产物实现或起草的新 agent/task 上下文或新 CLI conversation；不续用原作者的 task/conversation 作为独立 reviewer。原作者自检不计作独立 review；不要求不同模型或供应商。

### 2.2 文件优先的 Agent 交接

主 Agent 与 subagent 之间默认通过 workspace 文件交换实质信息，而不是在 prompt 中复制大段 context，或依赖 subagent 最后一条消息承载完整结果。

具体原则：

1. **Prompt 传目标、边界和路径。** 告诉 subagent 要解决什么、验收标准是什么、应读取哪些文件；已有材料只要已经在 workspace，就传路径，不再粘贴全文。
2. **Subagent 自己读取并迭代文件。** 让 subagent 从 source artifact、scratchpad、claim table 或代码中建立上下文。需要修改时写入自己的 namespaced 输出路径，不让多个 agent 同时覆盖 canonical 文件。
3. **结果先落盘，再返回 manifest。** Subagent 的完整研究、判断、代码或审稿结果写入指定 artifact；最后一条消息只需返回路径、状态、关键结论和未解决问题，不能让聊天摘要成为唯一交付。
4. **Parent 从 artifact 合并。** 主 Agent 读取 child artifacts、验证证据并统一写回 canonical output。Agent 间信息传递以可检查文件为准，不把前一个 agent 的自然语言总结直接当 source of truth。
5. **为失败恢复保留边界。** 长任务按阶段更新 scratchpad、checkpoint 或部分输出。Subagent 中断后，后续 agent 应能从文件继续，而不是只能重跑整段 conversation。

这种 file-first 交接有三个目的：减少 prompt 预处理和 context 复制；让 Agent 能在现有材料上反复读写；让中断、换模型和 parent 接管时仍有可审计的恢复点。结果极短、无 workspace、纯一次性判断，或 agent/运行时没有写权限时，可以直接在返回消息中交付。无写权限的只读探索应返回可核对的文件路径、行号与证据/结论，由 parent 核验并保存必要结果，不为 file-first 提升权限或绕过只读限制。

主线程责任：

1. 设计任务分割和验收标准。
2. 保留最终判断权，不把 subagent 输出直接拼接成最终答案。
3. 处理冲突、补查关键来源、运行最终验证。
4. 控制成本，避免把轻量任务变成多 agent 仪式。

### 2.1 语言继承规则

**subagent 默认继承用户当前对话语言。** 用户用中文，就用中文给 subagent 写 prompt，并要求它用中文输出；用户用英文，就用英文写 prompt，并要求它用英文输出。

不要把语言留给 subagent 自己猜。很多模型会在没有明确约束时回到英文默认值，结果就会出现主线程是中文、后台结果是英文的错位。

推荐做法：在每个 subagent prompt 里显式写一条语言要求，例如：

- `LANGUAGE: 用中文思考与输出，除非引用原文标题或 API 名称`
- `LANGUAGE: Respond in English. Keep source titles in their original language when needed`

如果任务需要双语，必须明确写成双语交付，不要让 subagent 自行决定。

### 3. 等待与整合

`background: true` 返回的仅是启动回执，等运行时自动完成通知后再读结果与落盘文件，不轮询、不调用不存在的 `background_output`，也不用定时巡检绕过。同步 wrapper 才直接返回完成结果；`task_id` 用于续写，不是等待句柄。派发前明确阶段预算、总 deadline、日志与失败停止条件，保留部分产物供恢复。

整合步骤：

1. 有 artifact 时读取文件，返回消息作为 manifest 和状态通知；无写权限的 child 按上述只读交接例外返回证据与内容，由 parent 核验并落盘。
2. 对重叠区域做交叉验证：多 agent 共同发现 → 可信度高；单一来源 → 标注待验证；矛盾信息 → 标注并分析原因。
3. 把整合结果写入 session 目录，例如 `phase3_synthesis.md`、`fact_check.md`、`brainstorm_synthesis.md`。
4. 如果 subagent 只在返回消息里总结，没有落盘，主线程应立即把关键结论落盘，避免证据链丢失。

### 3.1 运行中任务的持续与追加（running continuation）

对运行中的 `functions.task` 复用相同 `task_id` 追加 prompt 时，工具返回的 `context sent` 或 `Background task updated` 只是传输层接收回执，不等于子任务已收到或看到新范围。在那次核查中未见追加范围，不能据此声称子代理已收到；这只是当时没有观察到可观察的投递记录，异步 context 未必落在 timeline，也不构成平台层面的普遍行为。因此不能把工具 accepted 当成送达，真正改变范围需要 timeline 中出现可观察记录，或拿到关联的显式 ack，已取得 ack 的不必再回查 timeline。后台子任务完成仍走内置自动父链，不轮询进度、不做忙等；投递校验只在追加有意义范围或要求 ack 时做一次有界检查，不扩展成监控每次 tool call 的循环。走显式追加兜底时，先核对仍是同一个 current owner、task、attempt、directory，保留子任务当前的 model 与 agent，不猜默认值；结果未知先读取排查，不盲目重试，同一 request id 去重（这是调用侧约定，不代表 legacy API 已实现幂等），已送达的不重复投递。任务完成标记不等于交付物存在，验收除 timeline 外还要关联 ack 与实际产物，task context 工具的 receipt 本身不足以完成验收。具体验收标准见 [Astra Coordinator / PI 工作流](./workflow_astra_coordinator.md)。

---

## 路由决策

仅在决定委派后，按数据边界和当前注册能力分流；用户当前明确指定的模型、agent 或 CLI 优先于默认能力路由，仍须满足运行时能力与隐私约束，指定载体不可用时报告阻塞，不自行替换。不反过来强迫主线程委派编码：

1. 探索用 `explore`，通用调研用 `general`；专项审阅、推理、初筛及用户明确请求委派的实现使用当前注册的对应能力。
2. 隐私数据遵守本地/云端边界，不能因能力不足擅自外发；已选写作 workflow 决定 writer。
3. Antigravity CLI 可提供独立 fresh context 做 code / privacy / design review，不等同于 Gemini subagent。按已安装的 `ai-agent-cli` 根 skill、Antigravity focused skill 与当前可用列表选模型，不固定模型名。

不要沿用旧 `category` 参数或历史 agent 别名；只调用当前运行时已注册的 agent。

不要为了“稳定”默认给 agent 配 `temperature: 0`。默认使用 provider/server 的采样策略，除非目标模型明确要求固定采样。

---

## 示例

### 调研任务（30-50% overlap）

```
调研「某技术框架的采用情况」
├─ Agent 1（general）：官方叙事 + 产品定义
├─ Agent 2（general）：独立使用体验 + 社区反馈
├─ Agent 3（general）：失败边界 + 竞品对比
└─ Overlap：社区和企业案例都有覆盖，可交叉验证
```

### 用户明确要求委派的代码任务（0-20% overlap）

```
前提：用户明确要求委派「用户认证系统」实现；默认主线程亲自做
├─ Task 1：认证核心逻辑 + Token 管理
├─ Task 2：数据库模型 + 迁移脚本
├─ Task 3：API 端点 + 测试用例
└─ Overlap：接口定义处有少量重叠，确保对接正确
```

### 审查任务（单个 reviewer 或多视角 overlap）

通常派 1 个独立 reviewer 或 Antigravity CLI，主线程验收，不受多路并行门槛限制。复杂高风险 PR 可如下拆分：

```
审查「一个 PR 是否可靠」
├─ Agent 1（explore / 审阅向 agent）：代码行为和边界条件
├─ Agent 2（explore）：测试覆盖、缺失 fixture、回归风险
├─ Agent 3（审阅向 agent）：架构一致性和隐含依赖
└─ Overlap：所有 agent 都看核心 diff，但外围文件按职责分开
```

### 不适合并行的任务

```
修复「一个函数里的 off-by-one」
└─ 主线程直接读文件、改代码、跑测试。subagent 的启动和整合成本高于任务本身。
```

---

## 模型路由与指定模型

当前工具 schema 只暴露 `task(subagent_type=...)`，不暴露 `category` 或 `load_skills`。不要把旧环境的 category 路由照搬到当前 OpenCode 工具调用里。

可用 subagent 类型以运行时 schema 为准，不维护固定或历史模型清单；外部 CLI 按其已安装 skill 查询当前模型。

如果未来工具 schema 更新，以运行时 tool schema 为准，不要沿用过期的 `category` / `run_in_background` 写法。

---

## 注意事项

- **不要过度并行**：2-3 个精心设计的 subagent 通常优于 5 个松散的
- **prompt 质量**：subagent 的 prompt 要足够具体，否则结果会很浅
- **成本意识**：并行会消耗更多 token，评估是否值得
- **中间结果**：默认不需要把每个 subagent 的原始输出都落盘；但如果任务属于 research / writing workflow，主线程应把关键中间工件整理到 `tmp/<session_slug>/` 这类 session 目录中

---

## 常见错误

| 错误 | 正确做法 | 说明 |
|------|---------|------|
| 同批就绪任务逐个同步等待 | 同消息 wrapper 启动 | 异步跨消息仍可能并发 |
| 使用 `mcp_task(run_in_background=True)` | 支持时默认 `background: true` | 参数以运行时 schema 为准 |
| 轮询或把启动回执当完成 | 等自动完成通知，再读产物 | 同步 wrapper 才直接返回完成结果 |
| 用并行门槛否决单次 review | 通常交单个独立 reviewer | 轻微低风险局部变更可按比例例外 |
| 编造 `subagent_type` | 只使用运行时 tool schema 中列出的 subagent 类型 | `subagent_type` 必须是已注册 agent 名 |
| 传旧参数 `category` / `load_skills` | 按当前 `functions.task` schema 传 `description`、`prompt`、`subagent_type` | 旧参数不会被当前 task 工具接受 |
| 用户用中文，但 subagent prompt 用英文默认模板 | prompt 里显式声明语言继承规则 | 否则 subagent 往往回落到英文输出 |
