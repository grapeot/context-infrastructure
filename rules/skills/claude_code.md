# Skill: Claude Code

## 元数据
- 类型: API Guide
- 适用场景: 用 Claude Code CLI 做调研、改写、编辑文件、AI 调用 AI
- 最后更新: 2026-06-27

---

## 什么时候用

- 用户明确说用 Claude Code
- 任务强依赖本地文件和 workspace 上下文
- 需要非交互调用（`claude -p`）
- 需要 Claude 自己去读 `AGENTS.md`、rules、skills、报告和目标文件并决定往下钻什么

术语澄清：`Claude Code` = `claude` CLI / Claude Code 工具链。`Claude` = Anthropic 模型家族。**不要把"用 Claude Code"偷换成"用一个 Claude 路由 of subagent"**——后者只是一个底层可能用 Claude 模型的 agent，和 Claude Code CLI 是两回事。

---

## 默认模型

Claude Code 一律用 `--model opus`。不做 Sonnet fallback，不基于 trivial 判断降级。

---

## 启动目录

从工作区根目录启动。Claude Code 会沿着当前目录读取上下文，只有从 workspace 根启动才能稳定继承 `AGENTS.md`、`rules/SOUL.md`、`rules/USER.md`、`rules/WORKSPACE.md`、`rules/COMMUNICATION.md` 和 `rules/skills/INDEX.md`。

- `workdir=$WORKSPACE_ROOT`
- prompt 里尽量用绝对路径
- 需要额外目录时用 `--add-dir`

---

## 非交互调用

最小命令：

```bash
claude -p --model opus "your prompt"
```

拿 JSON 输出：

```bash
claude -p --model opus --output-format json "your prompt"
```

直接改文件（编辑型白名单）：

```bash
claude -p --model opus --permission-mode acceptEdits --tools Read,Edit,Write "your prompt"
```

调研型（Claude 需要自己联网、跑 CLI、调用 Tavily / curl / python 脚本）：

```bash
printf '%s' 'your research prompt' | claude -p --model opus \
  --permission-mode acceptEdits --tools Bash,Read,Write
```

**工具白名单和任务类型必须匹配**：

- `Read,Edit,Write` 适合文件改写
- `Bash,Read,Write` 适合调研 + 落盘
- research task 不要机械套用 `Read,Edit,Write`——没有 `Bash` 就等于没有检索能力

**长 prompt 走 stdin**。如果 prompt 里有长文本和引号/撇号，stdin 比命令行参数更稳，避免 shell quoting 把 prompt 传坏。

---

## 调用层级规则（硬规则）

**主 agent → subagent → `claude` CLI，最多两层。**

- **主 agent 不得直接调用 `claude` CLI**。Claude Code (Opus) 调用耗时通常 2-10 分钟，直接在主线程跑会阻塞所有并行工作，而且会独占主 agent 的 Bash 会话。正确做法：通过后台 subagent 独立执行，让它在内部调用 `claude`。
- **subagent 拿到任务后直接 Bash 执行 `claude -p`，禁止再派一层 agent**。不要调用嵌套派出机制。三层嵌套的失败模式是：外层 subagent 等内层 agent 回调，内层 agent 等 Claude Code 输出，任一层超时或消息丢失都会导致整个任务静默挂起。

**主 agent 派出 subagent 时，prompt 必须包含这几条防递归声明**：

1. "你是 subagent，不要再代理给其他 agent。"
2. "直接用 Bash 调用 `claude -p --model opus`。prompt 走 stdin。"
3. "这是分钟级长任务。Bash 工具的 timeout 设至少 600000ms（10 分钟），长文写作或深度调研给 900000ms（15 分钟）。"
4. "返回可核验痕迹：实际调用命令、关键 stdout 或目标文件变更。不要只说'我改好了'。"

**主 agent 必须做调用核验**。不能只看 subagent 的自述。通过可见证据确认它真的调用了 `claude` CLI（Bash 命令本身、stdout 结果、目标文件实际变更）。没看到证据就视为没有真正调用，必须回攻修正。

分工逻辑是：便宜 of agent 做编排，Claude Code 做思考。

---

## 长任务 timeout

Claude Code 调研、长文起草、重写、深度修订常见耗时 5-10 分钟，不能沿用 Bash 默认 120s timeout：

- **长文起草 / 深度改写 / 复杂综合**：600000ms（10 分钟）起步
- **重度调研 + 写作合并任务**：900000ms（15 分钟）
- **subagent 内部调 `claude -p`**：交接 prompt 里显式写"长任务，超时预算至少 600-900 秒"

按分钟级预算，不要按逆向小 shell 命令预算。

---

## Session continuity / resume

Claude Code CLI 原生支持 session 持久化，不是把旧 prompt 再喂一遍。先区分三层概念：

- **Dispatcher/Orchestrator 的 `session_id`**：外层 agent 的会话 ID，只延续其自身的上下文
- **Claude Code CLI 的 session**：`claude` 自己持久化的对话历史，支持真正的 resume
- **伪 continuity**：把 scratchpad、旧输出重新塞进 prompt。有用，但不等于 Claude Code 自己记住了对话

**硬规则：不要把外层框架的 session_id 误当成 Claude Code 的 session，它们是两套独立系统。**

CLI 支持 of 参数（来自 `claude --help`）：

- `-c, --continue`：继续当前目录最近一次对话
- `-r, --resume [value]`：按 session ID / 名称恢复
- `--fork-session`：恢复时分叉成新 session ID
- `--session-id <uuid>`：指定会话 ID
- `--no-session-persistence`：禁止持久化（仅 `--print` 模式；用了之后不能 resume）

常用用法：

```bash
# 继续当前目录最近一次对话
claude -c

# 恢复指定 session
claude -r <session-id> -p "continue the previous analysis"

# 恢复但分叉，保留原 session 不被覆盖
claude -r <session-id> --fork-session -p "take a different direction"
```

适合用 resume 的场景：同一任务分多轮继续、上一轮被中断但需要保留对话历史、多轮修订明确依赖上一轮上下文。

不适合的场景：单轮 `claude -p` 就能完成、要换方向而旧上下文会造成污染、外层 scratchpad 已经够用且保留旧历史徒增 token 成本。

---

## 调研模式：先给目标，不先给答案

如果任务是调研，默认给 Claude Code 目标、边界、起点，**让它自己决定搜什么**：

**要给的**：调研目标、成功标准、边界条件、起始文件或目录、可用工具（必须包含 `Bash`）

**不要做的**：
- 先替它搜一轮再把结果当成唯一语料塞进 prompt
- 把大量预处理好的上下文直接塞进 prompt
- 把 research task 偷换成 summary task
- 把 Claude Code 降级成 writer-only 或 final drafting only

只有两种情况适合先准备材料：数据源昂贵、受限或 Claude 无法直接访问；或你要的不是 full research 而是对一批已知材料做二次判断、筛选、写作。

**如果 Claude Code 在分析或写作过程中发现论证盲点、证据缺口、概念边界不清，默认允许它做补充调研**。目标是 targeted gap-filling，不是重新发散做完整 research pass。

**深度调研 / 观点碰撞 / 长文论证，默认让 Claude Code 做 lead thinker + final writer**，不是让它在主线程想完之后只负责措辞。

原则：**能放文件里的知识不要塞进 prompt；能让 Claude 自己找到的信息不要先替它找**。

---

## 写作任务：用户反馈必须原样落盘

如果任务涉及写作、重写、风格校准、标题修改、结构改写，包装层可以补充执行说明，但**必须把用户原始反馈 as-is 落到本地 handoff / scratchpad 文件里，再让 Claude Code 自己去读**。

- **不要只把用户意思"转述"给 Claude Code**。原话必须作为独立文件保留。
- 包装层只管执行约束（目标文件、边界、工具、超时、核验），不管写作风格。
- 显式告诉 Claude Code：**按用户 handoff + `rules/COMMUNICATION.md` 写，不要被 prompt 文风带偏**。

推荐流程：

1. 从工作区根目录启动
2. 把用户原始反馈原样写入 handoff 文件
3. prompt 只写目标、边界、目标文件、语言继承、风格约束
4. 让 Claude Code 自己读 `AGENTS.md`、rules、已有报告、handoff 和目标文档
5. 直接编辑目标文件或输出到指定路径

**语言继承是硬规则**。用户用中文，包装层 prompt 和 Claude Code 输出都用中文；用户用英文，全链路英文。不要依赖 Claude 自己判断语言——默认情况下模型经常会回落到英文。

---

## Final report protocol

如果任务属于 research + writing workflow，目标是产出最终可复用报告，Claude Code 在执笔前必须完成一轮标准预读：

1. `AGENTS.md`
2. `rules/SOUL.md`
3. `rules/USER.md`
4. `rules/WORKSPACE.md`
5. `rules/COMMUNICATION.md`
6. `rules/skills/INDEX.md`
7. 当前 session 的 scratchpad、manifest、search notes、目标报告文件

---

## 临时上下文文件

如果确实要补充一次性上下文，先写入文件再让 Claude Code 去读：

- 为每个 workflow/session 建独立子目录：`tmp/<session_slug>/`
- 把 scratchpad、source manifest、search notes、claude brief、gap list 放同一目录
- 关键中间产物默认落盘，不依赖 stdout
- 文件名写清楚职责：`scratchpad.md`、`search_manifest.md`、`claude_brief.md`
- 只有长期有复用价值才转正到 `contexts/` 或 `docs/`

---

## 参考实现

生产脚本里的 canonical 模式：

```python
import os
import subprocess

result = subprocess.run(
    ["claude", "-p", "--model", "opus", "--permission-mode", "acceptEdits"],
    cwd=WORKSPACE_ROOT,
    input=driver_prompt,
    text=True,
    capture_output=True,
    check=False,
)
```

---

## 实战 caveats

1. `claude -p` 必须真收到 prompt，命令行参数或 stdin 都行，长 prompt 走 stdin 更稳
2. 改文件时显式给 `--permission-mode acceptEdits`
3. 用绝对路径减少路径歧义
4. 包装层要处理 `FileNotFoundError`，给出 `claude` 不在 PATH 的清晰报错
5. 对外部站点搜索要有超时意识：5-7 分钟为一个检查点，没产出就用已有证据推进
6. Search manifest 要写清楚产出文件路径和 subagent 原始产出的回溯方式，否则后续只能看到判断看不到载体
7. 任务如果不必同步等待结果，默认走后台 subagent，不要在主线程直接跑 `claude`

---

## 关键参数速查

| 参数 | 默认 | 说明 |
|---|---|---|
| `--model` | `opus` | 一律用 Opus，不降级 |
| `--output-format` | `text` | 可选 `json` / `stream-json` |
| `--permission-mode` | — | 编辑任务用 `acceptEdits` |
| `--tools` | — | 编辑用 `Read,Edit,Write`；调研用 `Bash,Read,Write` |
| `--json-schema` | — | 强制结构化 JSON 输出 |
| `-c` / `--continue` | — | 继续当前目录最近一次对话 |
| `-r` / `--resume` | — | 按 session ID 恢复 |
| `--fork-session` | — | resume 时分叉成新 session |
