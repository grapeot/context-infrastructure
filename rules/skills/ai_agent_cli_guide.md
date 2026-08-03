# AI CLI Agent 实用指南

## 元数据
- 类型: API Guide
- 适用场景: 用 CLI Agent 构建自动化流水线、AI 调用 AI
- 最后更新: 2026-07-21

---

## 何时用 CLI Agent 而非原始 API

直接调用 LLM API 在处理复杂任务时存在短板。CLI Agent 作为中间层的核心优势：

1. **对抗"模型偷懒"**: 大任务时 API 易输出截断，Agent 天生具备循环执行和自我纠正能力
2. **原生文件上下文**: Agent 自动处理文件读取、编码和写入，将推理与 IO 解耦
3. **继承工具链**: 内置 MCP 插件，可随时调用 Tavily 搜索、执行脚本等
4. **优化上下文管理**: 自动处理 Context Window 消耗和长对话压缩

---

## 工具速查

| 维度 | Claude Code | Codex CLI | OpenCode | Antigravity CLI |
|------|-------------|-----------|----------|-----------------|
| **开源** | ❌ | ❌ | ✅ 100% | ❌ |
| **模型绑定** | 仅 Claude | 仅 OpenAI | Provider-agnostic（xAI, Anthropic, OpenAI, Google 等） | Antigravity 订阅内模型 |
| **CLI 非交互** | `claude --print` | `codex exec` | `opencode serve` + `opencode run --attach`（两步） | `agy --print` |
| **Web API** | ❌ | ❌ | ✅ 完整 | ❌ |
| **推荐场景** | 深度推理 | 自动化 | 多模型对比、自动化 + 可视化 | 用订阅额度调用 Gemini agent |

---

## 文件响应模式（核心设计原则）

**原则**: 在生产环境中，所有输入输出都通过文件，严禁使用管道模式处理核心逻辑。

**为什么**:
- **确定性**: AI 在"编辑文件"时的心理模型是"完成工作并保存"，不容易产生截断
- **可审计**: 任务前后文件系统的变化（git diff）是唯一的真理
- **大容量**: 绕过命令行参数长度限制

**实现要点**:
- **输入**: Prompt 必须先落到本地文件，再由程序读入
- **输出**: CLI 输出必须写入本地文件，再由程序读取解析
- **JSON 输出**: 在 Prompt 中显式要求"只输出 JSON"

**Python 示例**:
```python
import subprocess
from pathlib import Path

# 1. 写 prompt 到文件
Path("prompt.txt").write_text("Your task here...")

# 2. 构造驱动 prompt
driver_prompt = (
    f"Read the full prompt from {Path('prompt.txt').resolve()}\n"
    f"Write ONLY a JSON object to {Path('output.json').resolve()}\n"
    "Do not include Markdown or extra text."
)

# 3. 执行（以 Claude Code 为例）
subprocess.run([
    "claude", "--print", "--output-format", "json",
    "--model", "claude-sonnet-4-6-20260217",
    driver_prompt.replace('\0', '')  # 清理 null byte
])
```

---

## Claude Code 快速参考

**基本命令**: `claude --print "prompt"`

**关键参数**:
- `--model`: `claude-sonnet-4-6-20260217` (推荐) 或 `claude-opus-4-6-20260205` (深度推理)
- `--output-format`: `text` / `json` / `stream-json`
- `--permission-mode`: `acceptEdits` / `bypassPermissions`
- `--json-schema`: 强制输出符合 JSON Schema

**推荐**: Sonnet 4.6 性能接近 Opus，价格仅 1/5

---

## Antigravity CLI 快速参考

Antigravity 自动化使用独立的 `agy` 命令，不使用 `agy-ide chat`。完整安装、认证和执行契约见 [Antigravity CLI 文件式调用](./antigravity_cli.md)。

核心规则：prompt、结果、stdout、stderr、事件日志全部落盘；默认模型为 `gemini-3.6-flash-high`；`--dangerously-skip-permissions` 必须与 `--sandbox` 同时使用；内部 timeout 为 10 分钟，外层约 610 秒。

AGY 1.1.5 的 headless 入口是顶层 `agy --print`，不存在 `agy run`；它没有 `login` 子命令或 JSON event stream。CLI 从系统 keyring 复用 Antigravity App 或 IDE 的 Google 登录，进度检查使用带时间戳的 `--log-file`。它会在 headless mode 继承持久化 `settings.json` policy，运行前必须一并审阅。成功必须同时满足退出码为 0、结果文件非空、硬约束通过且 stderr 无未处理错误。

多阶段写作必须为每个阶段启动 fresh conversation，并使用独立的 prompt、result、stdout、stderr 和 events 文件。

---

## Codex CLI 快速参考

> 基于 Codex CLI 0.144.x 实测校对（2026-07-21）。0.1.x 系列改动很大，旧版的 `--full-auto` 已废弃，sandbox/approval 拆成独立参数，并新增了结构化输出与 last-message 落盘能力。

**基本命令**: `codex exec [options] "prompt"`（`exec` 可简写为 `e`）。prompt 也可用 `-` 从 stdin 读取；stdin 与位置参数同时给出时，stdin 会作为 `<stdin>` block 追加。

**核心参数**:
- `-m, --model`: 指定模型。当前生成为 GPT-5.x Codex 系列；不再是旧文档里的 `gpt-5.2`。
- `-c model_reasoning_effort=<level>`: `low`（翻译/格式转换）/ `medium`（常规）/ `high`（深度重构）。这是通过 `-c` 覆盖 config，不是独立 flag。
- `-s, --sandbox <mode>`: `read-only` / `workspace-write` / `danger-full-access`。**取代了旧的 `--full-auto`**。要让 agent 写文件用 `workspace-write`；只读推理用 `read-only`。
- `-a, --ask-for-approval <policy>`: `untrusted` / `on-request` / `never`。自动化场景配 `never`，让执行失败直接回流给模型而不阻塞。
- `--skip-git-repo-check`: 在非 git 目录运行（在临时目录必备）。
- `--ephemeral`: 不把 session 落盘（一次性调用推荐，避免 rollout 文件堆积）。
- `-C, --cd <dir>`: 指定 agent 工作根目录；`--add-dir <dir>` 追加可写目录。
- `--color never`: 关闭 ANSI，方便解析 stdout。

**自动化关键：结构化输出与结果落盘**

这是相对旧版最大的实用改进，取代"在 prompt 里恳求模型只输出 JSON"的脆弱做法：

- `-o, --output-last-message <file>`: 把 agent 最终一条消息**干净地**写入文件（无事件噪声）。文件响应模式的首选出口。
- `--output-schema <file>`: 传入 JSON Schema 文件，强制最终响应符合该 schema。配合 `-o` 可直接拿到校验过的 JSON。实测有效：

```bash
# schema.json: {"type":"object","properties":{"answer":{"type":"integer"}},"required":["answer"],"additionalProperties":false}
codex exec --skip-git-repo-check --sandbox read-only --color never \
  -c model_reasoning_effort=low \
  --output-schema schema.json \
  -o out.json \
  "What is 17 times 3?"
# out.json => {"answer":51}
```

**JSONL 事件流（`--json`）**

`--json` 输出 JSONL 事件流，schema 已重构。当前事件类型：

```
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"最终答案在这里"}}
{"type":"turn.completed","usage":{"input_tokens":...,"output_tokens":...}}
```

最终答案在 `item.type == "agent_message"` 的 `text` 字段；工具调用则是 `command_execution` / `file_change` 等 item 类型。监控进度按 item 逐条解析即可。注意 stderr 偶发 `failed to renew cache TTL` 警告，不影响结果，解析时忽略。

**其他新增子命令（自动化相关）**:
- `codex exec resume <session_id>` 或 `--last`: 续跑历史 session。
- `codex review [--uncommitted | --base <branch>]`: 非交互代码审查（也有 `codex exec review`）。
- `codex sandbox <command...>`: 直接在 Codex 的 seatbelt sandbox 里跑任意命令。
- `codex doctor`: 诊断安装、auth、runtime 健康（排查 CLI 问题第一步）。

**推荐**: 简单任务用 `low` + `read-only`，需写文件用 `workspace-write`，复杂重构用 `high`。生产自动化统一走 `--output-schema` + `-o` 拿结构化结果，比解析 stdout 稳。

### 使用第三方 model provider（Ollama Cloud 等）

Codex 默认走 ChatGPT 登录调 GPT-5.x，但也支持任意 OpenAI-compatible 的第三方 provider。这在以下场景有用：想用更便宜或更快的 model（如 Ollama Cloud 的 GLM-5.2、DeepSeek-V4-Flash）、想让数据离开 OpenAI 生态、或想用本地模型。

**原理**：在 `~/.codex/config.toml`（或 profile 文件）里定义 `[model_providers.<id>]` 段，指定 `base_url`、鉴权方式和 wire API。然后用 `model_provider = "<id>"` + `model = "<model_id>"` 路由过去。provider id 不能用保留名 `openai` / `ollama` / `lmstudio`。

**Profile 方式（推荐，不影响主配置）**：

```toml
# ~/.codex/ollama-cloud.config.toml
model = "glm-5.2"
model_provider = "ollama_cloud"

[model_providers.ollama_cloud]
name = "Ollama Cloud"
base_url = "https://ollama.com/v1"
env_key = "OLLAMA_API_KEY"
```

调用时加 `--profile ollama-cloud`，codex 会把这份配置 overlay 到主 config 之上：

```bash
OLLAMA_API_KEY=<your_key> codex exec --full-auto --profile ollama-cloud \
  -s danger-full-access -c model_reasoning_effort=low "你的 prompt"
```

**关键点**：

- `env_key` 指向环境变量名，codex 运行时从该变量读 API key。不要把 key 写进 config 文件。
- `base_url` 必须是 OpenAI-compatible endpoint（`/v1` 结尾）。Ollama Cloud 是 `https://ollama.com/v1`。
- `wire_api` 默认 `chat`（Chat Completions）。如果 provider 支持 Responses API，可加 `wire_api = "responses"`。
- 自定义 provider 不能用 `--oss` / `--local-provider`（那两个只给本地 ollama/lmstudio 用）。
- 第三方 model 的 tool calling 能力参差。实测 Ollama Cloud GLM-5.2 能正常用 codex 的 read/bash/write 工具完成文件处理任务，但 reasoning 较长时 token 控制不如 GPT-5.x 精准，简单任务建议 `model_reasoning_effort=low`。
- codex 启动时会刷新 model 列表，部分 provider 返回格式不完全匹配（如 Ollama Cloud 返回 `{"data":[...]}` 而非 `{"models":[...]}`），会打 ERROR 日志但不影响实际推理，可忽略。

**鉴权方式**：
- `env_key = "XXX"`：从环境变量读 API key（最常用）。
- `requires_openai_auth = true`：复用 ChatGPT/API key 登录（适合 OpenAI 代理）。
- 不设任何 auth：无鉴权（适合本地模型）。
- `[model_providers.<id>.auth]` + `command`：从外部命令获取 bearer token（适合需要动态 token 的场景）。

**实测验证清单**（接入新 provider 后建议跑一遍）：
1. 最小连通性：`请只回复 OK` 确认 provider 路由通。
2. 工具调用：`写一个 Python hello world 并运行` 确认 read/bash/write 工具链正常。
3. 文件处理：让 agent 读写一个真实文件，确认 sandbox 内 IO 正常（特别注意 workspace 外路径会被 sandbox 拦截）。

---

## OpenCode 快速参考

OpenCode 有两种非交互调用方式：CLI（`opencode run`）和 Web Server API。

### 方式 A：CLI（serve + run --attach）

`opencode run` 单独执行会因内置 server 启动失败报 "Session not found"。**正确用法**是先起 headless server，再 attach 上去：

```bash
# 1. 启动 headless server（后台常驻，端口可自定义）
opencode serve --port 14097 &

# 2. 发送任务（attach 到已有 server）
opencode run \
  --attach "http://localhost:14097" \
  -m "xai/grok-4.20-experimental-beta-0304-non-reasoning" \
  --dir "/path/to/project" \
  "你的 prompt"
```

**关键参数**:
- `--attach`: 连接到已运行的 server（必须）
- `-m, --model`: `provider/model` 格式（如 `xai/grok-4.20-experimental-beta-0304-non-reasoning`）
- `--dir`: 指定 agent 的工作目录（server 端路径）
- `--format json`: JSON 事件流输出（适合程序解析）
- `--agent`: 指定 agent（默认 build）
- `--variant`: reasoning effort（如 `high`, `max`, `minimal`，provider-specific）

**查看可用模型**: `opencode models | grep xai`

**Server 管理**:
- Server 和工作目录绑定。建议从一个固定目录启动以统一 session 管理
- Server 启动后可处理多个 `run --attach` 请求
- 停止：`kill` 进程或 `Ctrl+C`

### 方式 B：Web Server API（Python 编程调用）

适合需要精细控制 session 生命周期的场景。

**启动 Server**: `opencode web --port 4096`（或 `opencode serve --port 4096`）

**Python 客户端**: `periodic_jobs/ai_heartbeat/src/v0/opencode_client.py` 已实现常用 API 封装
- `create_session()` / `send_message()` / `get_session_messages()` / `wait_for_session_complete()`

**模型格式**: `provider/model` (如 `xai/grok-4.20-experimental-beta-0304-non-reasoning`, `anthropic/claude-sonnet-4-20250514`)

### 方式选择

| 场景 | 推荐方式 |
|------|----------|
| 单次任务、快速实验 | CLI（serve + run --attach） |
| 批量实验、需程序控制 session | Web Server API |
| AI 调用 AI（文件响应模式） | CLI（更简单）或 API（更可控） |

### 常用模型速查

| Provider | Model ID | 特点 |
|----------|----------|------|
| xai | `grok-4.20-experimental-beta-0304-non-reasoning` | Grok 4.20 非推理，快速 |
| xai | `grok-4.20-experimental-beta-0304-reasoning` | Grok 4.20 推理版 |
| xai | `grok-4-1-fast-non-reasoning` | Grok 4.1 非推理，$0.20/1M input |
| anthropic | `claude-opus-4-6` | Claude 深度推理 |
| anthropic | `claude-sonnet-4-6` | Claude 常规，性价比高 |
| openai | `gpt-5.x` | GPT-5.x Codex 当前生成（需 Codex 插件） |

---

## AI 调用 AI 模式

如果你正在编写一个 Agent 来调用这些 CLI，提供如下元指令：

> "当面临大规模文本处理或文件系统操作时，请调用底层的 CLI Agent：
> 1. 优先使用文件响应模式，先将待处理内容存入本地临时文件
> 2. 使用流模式 (`--json`) 并实时解析事件以便监控进度
> 3. 设置合理的推理强度（如翻译设为 `low`）
> 4. 传递 Prompt 前清理空字符 (`.replace('\0', '')`)
> 5. 对于 OpenCode，优先使用 Web Server API"

上面的 JSON 流建议不适用于 Antigravity CLI。AGY 使用 `--log-file` 观察进度，并以指定结果文件作为唯一成品。

---

## 极简主义设计哲学 (pi-mono)

来自 pi-mono 项目的核心原则：**"What's missing matters more than what's included"**

**核心理念**:
- **Context Engineering is Paramount**: 上下文工程比工具数量更重要
- **Full Observability**: 完全可观测，无隐藏状态
- **External State**: 写文件而非维护内部状态
- **Builder's Mindset**: 面向构建者而非消费者设计

**启发**: 在复杂任务中，添加功能往往是逃避问题。真正难的决策是：**什么不该有**。

---

## 模型选择速查

| 任务类型 | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| **翻译/格式转换** | Sonnet 4.6 | GPT-5.x Codex + low | *(你的轻量模型)* |
| **常规开发** | Sonnet 4.6 | GPT-5.x Codex + medium | *(你的标准模型)* |
| **深度推理/重构** | Opus 4.6 | GPT-5.x Codex + high | *(你的推理模型)* |

---

## OpenCode 生产经验（量化交易实验总结）

以下来自在 某量化交易实验项目中用 OpenCode + Grok 4.20 跑 回测实验的实战经验。

### 权限模型：文件必须在项目根目录下

OpenCode agent **无法访问项目根目录之外的路径**（包括 `/tmp/`）。所有 file IO（prompt 输入文件、JSON 输出文件）必须放在 server 启动时的工作目录下。

```python
# ❌ 错误：/tmp 会被 agent 拒绝访问
prompt_path = Path("/tmp/opencode_prompt.txt")

# ✅ 正确：放在 run 目录或项目本地目录
prompt_path = run_dir / "opencode_prompts" / f"{invocation_id}.txt"
# 或 fallback 到项目根目录下
prompt_path = Path(".opencode_tmp") / f"{invocation_id}.txt"
```

### 可靠性：stdout JSON 兜底

即使 prompt 明确要求"写入文件"，agent 有时会直接在 stdout 输出 JSON 而不写文件（或写入空文件）。**生产环境必须实现 stdout JSON 提取作为 fallback**：

```python
import re

def _extract_json_from_text(text: str) -> dict | None:
    """从 stdout 中提取 JSON 对象（兜底方案）"""
    # 优先匹配 ```json 代码块
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # 回退：找最大的 {...} 块
    candidates = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text)
    for c in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    return None
```

### 并发能力

一个 `opencode serve` 进程可以处理多个并发的 `run --attach` 请求。每个请求创建独立的 session。实测 2 并发稳定，更高并发取决于 LLM provider 的 rate limit。

### Grok 4.20 不支持的参数

`xai/grok-4.20-experimental-beta-0304-non-reasoning` 不支持 `presence_penalty`、`frequency_penalty`、`stop` 参数。如果 OpenCode 转发了这些参数，API 会报错。

### 典型调用流程（文件响应模式）

```
1. 写 prompt → run_dir/opencode_prompts/XXXX.txt
2. 构造 driver prompt: "Read from {prompt_path}, write JSON to {response_path}"
3. opencode run --attach http://localhost:14097 -m model "driver_prompt"
4. 读 run_dir/opencode_responses/XXXX.json
5. 如果文件为空 → 从 stdout 提取 JSON（fallback）
6. 如果仍然失败 → retry（最多 3 次）
```

### 关键数据

- Smoke test: 7/7 成功（零 retry），约 3 分钟 wall clock（6 个 30 分钟间隔）
- 每个 decision 平均耗时: ~20-30 秒（Grok 4.20 non-reasoning）
- Server 启动命令: `opencode serve --port 14097`（从 <your-project> 目录启动）

---

## 参考

- [Claude Code 官方文档](https://docs.anthropic.com)
- [OpenAI Codex 文档](https://platform.openai.com/docs)
- [OpenCode 官方文档](https://opencode.ai/docs)
