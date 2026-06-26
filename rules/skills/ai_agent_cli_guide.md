# AI CLI Agent 实用指南

## 元数据
- 类型: API Guide
- 适用场景: 用 CLI Agent 构建自动化流水线、AI 调用 AI
- 最后更新: 2026-06-27

---

## 何时用 CLI Agent 而非原始 API

直接调用 LLM API 在处理复杂任务时存在短板。CLI Agent 作为中间层的核心优势：

1. **对抗"模型偷懒"**: 大任务时 API 易输出截断，Agent 天生具备循环执行和自我纠正能力
2. **原生文件上下文**: Agent 自动处理文件读取、编码和写入，将推理与 IO 解耦
3. **继承工具链**: 内置 MCP 插件，可随时调用 Tavily 搜索、执行脚本等
4. **优化上下文管理**: 自动处理 Context Window 消耗和长对话压缩

---

## 工具速查

| 维度 | Claude Code | Codex CLI | Cursor Agent | OpenCode |
|------|-------------|-----------|--------------|----------|
| **开源** | ❌ | ❌ | ❌ | ✅ 100% |
| **模型绑定** | 仅 Claude | 仅 OpenAI | Cursor 模型族 | Provider-agnostic（xAI, Anthropic, OpenAI, Google 等） |
| **CLI 非交互** | `claude --print` | `codex exec` | `agent -p`（prompt 落盘文件） | `opencode serve` + `opencode run --attach`（两步） |
| **Web API** | ❌ | ❌ | ❌ | ✅ 完整 |
| **推荐场景** | 深度推理 | 自动化 | Cursor IDE 工作区自动化、Heartbeat | 多模型对比、自动化 + 可视化 |

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

## Codex CLI 快速参考

**基本命令**: `codex exec [options] "prompt"`

**关键参数**:
- `-m, --model`: `gpt-5.2` (推荐)
- `-c model_reasoning_effort`: `low` (翻译) / `medium` (常规) / `high` (深度重构)
- `--full-auto`: 自动接受所有操作
- `--json`: JSON 输出格式

**推荐**: 简单任务用 `low`，复杂任务用 `high`

---

## Cursor Agent CLI 快速参考

本 workspace 的 AI Heartbeat（observer/reflector）默认经 Cursor Agent CLI 驱动；与 OpenCode 共用 `agent_client.py` 抽象。

**基本模式**: prompt 落盘 → `agent -p --workspace <dir> [--resume <chat_id>] "<read prompt file>"`

**关键环境变量**（见根目录 `.env.example`）:
- `HEARTBEAT_ENGINE=cursor`（默认）或 `opencode`
- `CURSOR_AGENT_MODEL`：如 `composer-2.5`
- `CURSOR_AGENT_TIMEOUT`：单次任务超时（秒）
- `CURSOR_USE_RESUME_CHAT`：设为 `true` 时用 `agent create-chat` 复用会话

**Python 客户端**: `periodic_jobs/ai_heartbeat/src/v0/cursor_client.py`（`OpenCodeClient` 兼容接口）
- prompt 目录：`<workspace>/.cursor_tmp/heartbeat/`
- 统一入口：`agent_client.get_client(engine)`，`add_engine_args()` 供 CLI 脚本复用

**与 OpenCode 选型**:

| 场景 | 推荐引擎 |
|------|----------|
| 已在 Cursor IDE 工作、需 MCP/内置工具 | `cursor` |
| 需切换多 provider 模型、Web API 编排 | `opencode` |
| AI 调用 AI（文件响应模式） | 两者均适用；Cursor 默认零配置 |

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

**Python 客户端**: `periodic_jobs/ai_heartbeat/src/v0/opencode_client.py` 已实现常用 API 封装；双引擎入口见同目录 `agent_client.py`
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
| openai | `gpt-5.4` | GPT-5.4（需 Codex 插件） |

---

## AI 调用 AI 模式

如果你正在编写一个 Agent 来调用这些 CLI，提供如下元指令：

> "当面临大规模文本处理或文件系统操作时，请调用底层的 CLI Agent：
> 1. 优先使用文件响应模式，先将待处理内容存入本地临时文件
> 2. 使用流模式 (`--json`) 并实时解析事件以便监控进度
> 3. 设置合理的推理强度（如翻译设为 `low`）
> 4. 传递 Prompt 前清理空字符 (`.replace('\0', '')`)
> 5. 对于 OpenCode，优先使用 Web Server API"

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
| **翻译/格式转换** | Sonnet 4.6 | gpt-5.2 + low | *(你的轻量模型)* |
| **常规开发** | Sonnet 4.6 | gpt-5.2 + medium | *(你的标准模型)* |
| **深度推理/重构** | Opus 4.6 | gpt-5.2 + high | *(你的推理模型)* |

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
