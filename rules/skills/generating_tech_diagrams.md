# Fireworks Tech Graph — 技术架构图生成

## 元数据

- **类型**: Workflow
- **适用场景**: 用自然语言生成出版级 SVG + PNG 技术架构图、流程图、UML、AI/Agent 系统图
- **上游来源**: [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)（MIT）
- **创建日期**: 2026-06-27
- **user-invocable**: true

---

## 何时触发

用户提到以下任一意图时**先读本 skill**：

```
generate diagram / draw diagram / 画架构图 / 生成架构图 / 技术图 / flowchart
architecture diagram / sequence diagram / data flow / 系统架构图
RAG 架构图 / Agent 流程图 / Mem0 / Multi-Agent / UML
```

**路由（与其他 diagram 能力区分）**：

| 需求 | 用哪个 |
|------|--------|
| 暗色 HTML + 浏览器内 Copy/PNG/PDF 导出 | `generating_architecture_html_diagrams.md`（[Cocoon-AI](https://github.com/Cocoon-AI/architecture-diagram-generator)） |
| 出版级多风格 SVG+PNG、UML、AI/Agent 语义形状 | **本 skill**（fireworks-tech-graph） |
| 芯片 survey 可编辑架构图（Excalidraw） | 沿用 `contexts/survey_sessions/assets/*.excalidraw` 惯例 |
| Markdown 内快速示意 | Mermaid（chat 内嵌即可） |
| 代码截图 / 终端输出 PNG | `exporting_to_png.md` |
| 概念艺术 / 营销配图 | `generating_images.md` |

---

## 安装上游 Skill（推荐）

```bash
# Cursor / Claude Code skills CLI
npx skills add yizhiyanhua-ai/fireworks-tech-graph

# 或 clone 到本地 skills 目录
git clone https://github.com/yizhiyanhua-ai/fireworks-tech-graph.git ~/.cursor/skills/fireworks-tech-graph
```

更新：`npx skills add yizhiyanhua-ai/fireworks-tech-graph --force -g -y`

**注意**：`skills add` 用 **GitHub repo 名**，不要用 npm 包名 `@yizhiyanhua-ai/fireworks-tech-graph`。

安装后，生成前读取上游 `SKILL.md` 与 `references/style-*.md`（Style 8 读 `references/style-8-dark-luxury.md`）。

---

## PNG 渲染依赖

默认 **cairosvg**（CSS 支持最好）：

```bash
pip install cairosvg
python3 -c "import cairosvg; print(cairosvg.__version__)"
```

| 渲染器 | 质量 | 何时用 |
|--------|------|--------|
| **cairosvg** | 好 | 默认 |
| rsvg-convert | 一般 | 无 Python；简单 flat 图 |
| puppeteer | 最好 | D3/Mermaid 转 SVG 或像素级 fidelity |

导出宽度：**1920px**（2× retina）。技术图用 PNG，不用 JPEG。

若已安装上游 repo，用其脚本：

```bash
# 在上游 clone 目录内
./scripts/validate-svg.sh path/to/diagram.svg
./scripts/generate-diagram.sh path/to/diagram.svg   # SVG → PNG
```

未安装上游时，手写 SVG 后本地导出：

```python
import cairosvg
cairosvg.svg2png(url="diagram.svg", write_to="diagram.png", output_width=1920)
```

---

## 工作流

```
1. 分类 diagram type + style
2. 列出 nodes / containers / arrows（含 semantic kind）
3. 生成纯 inline SVG（禁止 @import 外链字体）
4. validate-svg（或 xml _wellformed 检查）
5. 导出 1920px PNG
6. 汇报 .svg + .png 路径
```

**本 workspace 默认输出路径**：

- 芯片调研报告：`contexts/survey_sessions/assets/<topic>_chip_architecture.svg` + `.png`
- 临时草稿：`tmp/diagrams/<name>.svg` + `.png`
- 报告内引用：相对路径，如 `assets/nvidia_gpu_chip_architecture.png`

同时更新 survey markdown 的「附：架构图索引」表（若属于 survey 任务）。

---

## 8 种视觉风格

| # | 名称 | 背景 | 适用 |
|---|------|------|------|
| 1 | **Flat Icon**（默认） | #ffffff | 博客、文档、slides |
| 2 | **Dark Terminal** | #0f0f1a | GitHub README、dev 文章 |
| 3 | **Blueprint** | #0a1628 | 工程架构、分层存储 |
| 4 | **Notion Clean** | #ffffff | Wiki、Confluence |
| 5 | **Glassmorphism** | #0d1117 渐变 | 产品 keynote、Multi-Agent |
| 6 | **Claude Official** | #f8f6f3 | Anthropic 风格 |
| 7 | **OpenAI Official** | #ffffff | OpenAI 风格 API 流 |
| 8 | **Dark Luxury**（AI 手作） | #0a0a0a + 香槟金 | 无模板；读 upstream `style-8-dark-luxury.md` |

**选型速查**：

- UML Class/Component → Style 1 或 4
- Sequence/Timing → Style 2
- State/Activity/Deployment → Style 3
- RAG / Agentic Search → Style 2 或 5
- Memory Architecture → Style 3
- 内部文档 → Style 4；GitHub → Style 2

用户指定 `--style glassmorphism` / `style 2` / `暗色终端` 时严格遵循。

Style 1–7 可走 upstream `scripts/generate-from-template.py` + fixtures；Style 8 必须手作 SVG。

---

## 图表类型

| 类型 | 布局规则 |
|------|----------|
| **Architecture** | 水平分层，上→下 |
| **Data Flow** | 每条 arrow 标注数据类型 |
| **Flowchart** | 菱形=决策，上→下 |
| **Agent Architecture** | 5 层：Input / Agent / Memory / Tool / Output |
| **Memory Architecture** | 读写分路、存储 tier |
| **Sequence** | 竖 lifeline + 水平消息 |
| **Comparison** | 列=系统，行=属性 |
| **Mind Map** | 中心节点 + bezier 分支 |

**UML（14 种）**：Class、Component、Deployment、Package、Composite Structure、Object、Use Case、Activity、State Machine、Sequence、Communication、Timing、Interaction Overview、ER — 见 upstream README。

---

## 语义形状词汇（跨风格一致）

| 概念 | 形状 |
|------|------|
| User | 圆 + 身体 |
| LLM / Model | 圆角矩形、双边框、⚡ |
| Agent / Orchestrator | 六边形 |
| 短期 Memory | 虚线圆角矩形 |
| 长期 Memory | 实心圆柱 |
| Vector Store | 带内环圆柱 |
| Graph DB | 三圆簇 |
| Tool / Function | 矩形 + ⚙ |
| API / Gateway | 单边框六边形 |
| Queue / Stream | 水平管道 |
| Decision | 菱形 |
| External Service | 虚线矩形 |

产品图标（OpenAI、Pinecone、Kafka、PostgreSQL 等 40+）见 upstream `references/icons.md` — 用 **inline SVG path**，禁止 CDN URL。

---

## 箭头语义

| 流类型 | 线型 | 含义 |
|--------|------|------|
| Primary data | 2px solid | 主请求/响应 |
| Control | 1.5px solid | 触发 |
| Memory read | 1.5px solid | 读取 |
| Memory write | 1.5px dash 5,3 | 写入 |
| Async / event | 1.5px dash 4,2 | 非阻塞 |
| Feedback / loop | 1.5px curved | 迭代 |

---

## AI/Agent 内置模式

```
RAG Pipeline      → Query → Embed → VectorSearch → Retrieve → LLM → Response
Agentic RAG       → + Agent loop + Tool use
Agentic Search    → Query → Planner → [Search/Calc/Code] → Synthesizer
Mem0 Memory       → Input → Memory Manager → [VectorDB + GraphDB] → Context
Agent Memory Types→ Sensory → Working → Episodic → Semantic → Procedural
Multi-Agent       → Orchestrator → [SubAgent×N] → Aggregator → Output
Tool Call Flow    → LLM → Tool Selector → Execution → Parser → LLM (loop)
```

芯片编译栈（CUDA / NEFF / PJRT）架构图：用 **Architecture + Data Flow**，Style 3 Blueprint 或 Style 1；节点按「Framework → IR → Backend → Container → Runtime」分层。

---

## Stable Prompt 模板

### Style 1 — Mem0 记忆架构

```
Draw a Mem0 memory architecture diagram in style 1 (Flat Icon).
Four horizontal sections: Input Layer, Memory Manager, Storage Layer, Output / Retrieval.
Include User, AI App / Agent, LLM, mem0 Client, Memory Manager, Vector Store, Graph DB,
Key-Value Store, History Store, Context Builder, Ranked Results, Personalized Response.
Use semantic arrows for read, write, control, and data flow.
```

### Style 2 — Tool Call 流

```
Draw a tool call flow diagram in style 2 (Dark Terminal).
Show User query, Retrieve chunks, Generate answer, Knowledge base, Agent, Terminal,
Source documents, and Grounded answer. Terminal chrome, neon accents, monospace typography.
```

### Style 3 — 微服务 / 编译栈

```
Draw a microservices architecture diagram in style 3 (Blueprint).
Numbered sections: 01 // EDGE, 02 // APPLICATION SERVICES, 03 // DATA + EVENT INFRA, 04 // OBSERVABILITY.
Blueprint grid, cyan strokes, bottom-right title block.
```

（Style 4–8 完整 recipe 见 [upstream README](https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/main/README.md#stable-prompt-recipes)）

---

## 高杠杆 JSON 字段（upstream generator）

若走 `generate-from-template.py` / fixtures 路线，优先填：

- `containers[]` — swim lane 分组
- `nodes[].kind` — 语义形状
- `arrows[].flow` — read/write/control/async
- `containers[].header_prefix` — Blueprint `01 // EDGE`
- `containers[].side_label` — Claude Official 左侧层标签
- `blueprint_title_block` — Style 3 工程 title box

fixtures 参考：`fixtures/mem0-style1.json`、`fixtures/tool-call-style2.json`。

---

## 故障排除

| 症状 | 原因 | 修复 |
|------|------|------|
| PNG 空白/全黑 | SVG 内 `@import url()` 外链字体 | 改用 system font stack |
| 边框/文字缺失 | rsvg 不支持 CSS/foreignObject | 换 cairosvg |
| 图底部被裁切 | viewBox 高度不足 | 增大 `viewBox="0 0 960 H"` |
| 文字溢出 | label 过长 | `text-anchor="middle"` + clipPath 或缩短 |
| 图标不显示 | 用了 CDN URL | 改 inline path |

**硬约束**：纯 inline SVG；无外部字体 fetch；无 JS 注入样式（除非走 puppeteer）。

---

## 验收标准

1. 同时交付 `.svg`（可编辑）与 `.png`（1920px 宽）
2. 形状与箭头符合语义词汇表
3. 风格与用户指定或场景默认一致
4. PNG 非空：`file diagram.png && ls -la diagram.png`
5. Survey 任务时更新 markdown 架构图索引表

---

## 参考链接

- 上游 repo：https://github.com/yizhiyanhua-ai/fireworks-tech-graph
- 上游 SKILL.md：https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/main/SKILL.md
- 中文 README：https://github.com/yizhiyanhua-ai/fireworks-tech-graph/blob/main/README.zh.md
- PNG 通用导出：`rules/skills/exporting_to_png.md`
