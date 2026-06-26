# Crucible Notes 查阅指南

## 元数据

- **类型**: Reference
- **适用场景**: 需要深入理解 NVIDIA CUDA 编译器 toolchain、AWS Neuron 编译器/运行时/GPSIMD、Google TPU PJRT 等**二进制内部实现**时，查阅 [crucible-notes](https://gh.evko.io/crucible-notes/) 逆向工程 wiki
- **上游来源**: [GrigoryEvko/crucible-notes](https://github.com/GrigoryEvko/crucible-notes)（MIT License）
- **创建日期**: 2026-06-26

---

## 工作流入口（优先读）

**何时第一个打开本 skill**：用户问题或任务涉及 AI 芯片 / ML 加速器，且触及以下任一层面——

- 编译产物格式（NEFF、fatbin、SASS）
- 编译器 / 运行时内部（IR、pass、symbol、ioctl、firmware）
- 官方文档只给 API/概念、但需要理解「底下怎么跑」

**路由顺序**：

1. **读本 skill** → 按下方「触发词 → 优先 wiki」选 crucible 章节
2. **官方 doc 定边界** → 用户可见行为与 API 以 Tier 1 为准
3. **按需叠加**：
   - 产品层背景 → `contexts/survey_sessions/*_survey_*.md`
   - 全面第三方调研 → `workflow_deep_research_survey.md`
   - 并行读多个 wiki Part → `workflow_parallel_subagents.md`

**不触发本 skill**：纯产品规格对比、无 internals 深度的市场分析、crucible 未覆盖的芯片（MTIA 等）。

---

## 目标与边界

**做什么**：把 crucible-notes 当作「编译器/运行时 internals 的深度参考」，帮助 agent 快速定位正确的 wiki 章节、理解组件关系、提取可验证的技术 claim，并在输出中正确标注可信度层级。

**不做什么**：
- 不把 crucible-notes 当作官方文档或事实标准——站点自身声明为 *best-guess reconstruction*
- 不单独依据该站点做产品决策、性能承诺或法律/合规结论
- 不替代 AWS / NVIDIA / Google 官方文档的用户-facing API 说明
- 不尝试复现或分发逆向得到的专有二进制

---

## 可信度模型（硬约束）

站点首页与每本 wiki 均标明：

> *AI-GENERATED REVERSE-ENGINEERING NOTES — AUTHOR'S PERSONAL REFERENCE ONLY. EVERYTHING HERE IS A BEST-GUESS RECONSTRUCTION, NOT A RELIABLE SOURCE.*

查阅时必须遵守以下分层（与 `workflow_deep_research_survey.md` 的信息源层级对齐）：

| 层级 | 来源 | 如何使用 |
|------|------|----------|
| **Tier 1（官方）** | AWS Neuron docs、CUDA Toolkit docs、Google TPU docs | 用户-facing 行为、API、发布说明——**验证结论的最终依据** |
| **Tier 2（crucible 高置信）** | 页内标注为 symbol/DWARF/`file:line`  grounded 的 claim | 可作为 internals 假设，引用时注明「crucible-notes，binary-derived」 |
| **Tier 3（crucible 推断）** | 页内标注 inferred / pattern-matched | 仅作探索方向，**必须**找官方 doc 或实验验证 |
| **Tier 4（行为证据）** | GitHub issues、NEFF 实测、编译器 flag 实验 | 用于证伪 crucible 推断 |

**输出规则**：从 crucible-notes 引用的任何 claim，正文中必须同时给出：
1. crucible-notes 页面 URL（绝对链接）
2. 该 claim 在 wiki 中的置信度描述（若页面有 confidence model，转述）
3. 是否有官方文档 corroboration；若无，显式写「未独立验证」

---

## 站点路由

**基址**：https://gh.evko.io/crucible-notes/

**URL 模式**：`https://gh.evko.io/crucible-notes/<component>/`  
每本 wiki 是 mdBook 结构，支持 `/` 搜索、`←`/`→` 章节导航。

### CUDA 编译器 toolchain

| 组件 | Wiki | 适用问题 |
|------|------|----------|
| **cicc** | [cicc/](https://gh.evko.io/crucible-notes/cicc/) | CUDA C→PTX；LLVM 20 + EDG 前端 |
| **cudafe++** | [cudafe++/](https://gh.evko.io/crucible-notes/cudafe++/) | CUDA C++ 前端、EDG 语义 |
| **tileiras** | [tileiras/](https://gh.evko.io/crucible-notes/tileiras/) | Cuda Tile IR；MLIR → TileAS → PTX/SASS |
| **ptxas** | [ptxas/](https://gh.evko.io/crucible-notes/ptxas/) | PTX→SASS；159-phase pipeline |
| **nvlink** | [nvlink/](https://gh.evko.io/crucible-notes/nvlink/) | Device linker；embedded ptxas |
| nvcc | — | 计划中 |
| nvptxcompiler | — | 计划中 |

### ML 加速器编译器 / 运行时

| 组件 | Wiki | 适用问题 |
|------|------|----------|
| **neuronx-cc** | [neuronx-cc/](https://gh.evko.io/crucible-notes/neuronx-cc/) | HLO→Penguin→BIR→walrus→**NEFF**；NKI DSL；`hlo-opt` / `hlo2penguin` |
| **neuronx-runtime** | [neuronx-runtime/](https://gh.evko.io/crucible-notes/neuronx-runtime/) | `libnrt.so`、DKMS、`libncfw.so`、collectives、NEFF load/execute |
| **neuronx-gpsimd** | [neuronx-gpsimd/](https://gh.evko.io/crucible-notes/neuronx-gpsimd/) | Vision-Q7 DSP、custom op、firmware 代际（Sunda/Cayman/Mariana/Maverick） |
| **libtpu** | [libtpu/](https://gh.evko.io/crucible-notes/libtpu/) | Google TPU PJRT；LLO VLIW ISA；6 代 silicon |

### 工具

| 工具 | 链接 | 说明 |
|------|------|------|
| **fatbin** | [GitHub fatbin/](https://github.com/GrigoryEvko/crucible-notes/tree/main/fatbin) | Fat binary dump/unpack/repack（ZSTD） |

---

## Neuron 栈：组件关系与阅读顺序

做 AWS Neuron internals 调研时，按数据流选 wiki：

```
Framework (torch-neuronx / PJRT)
        ↓
neuronx-cc wiki     — 编译：HLO/StableHLO → Penguin → BIR → libwalrus → NEFF
        ↓
neuronx-runtime wiki — 加载：nrt_load → execute → collectives → DKMS → device
        ↓
neuronx-gpsimd wiki  — Custom op：GPSIMD/Q7 microcode、firmware、NEFF 内嵌 payload
```

**neuronx-cc 推荐入口**（[Compile Pipeline at a Glance](https://gh.evko.io/crucible-notes/neuronx-cc/)）：
- Part 1 `arch/` — 硬件与六引擎模型、LNC
- Part 4 `hlo-opt/` — HLO 优化与 `hlo2penguin`
- Part 5 `penguin/` — Penguin IR middle-end
- Part 6 `nki/` — NKI tracing/lowering
- Part 7–8 `bir/` + `walrus/` — 后端 codegen 与 linker
- Part 12 `formats/` — **NEFF 容器格式**
- Part 13 `distribution/` — SPMD、collectives 编译期分区

**Companion wikis**（页内交叉链接，查阅时一并打开）：
- neuronx-cc ↔ neuronx-runtime（NEFF 生产者/消费者）
- neuronx-gpsimd ↔ neuronx-runtime Part XI（microcode 加载）
- neuron-jax-stack、neuronx-misc（PJRT 契约、诊断工具）——在 runtime wiki 的 Companion 节列出

与本 workspace 已有调研的衔接：`contexts/survey_sessions/aws_neuron_survey_20260626.md` 覆盖**产品级**硬件/软件；crucible-notes 用于**编译器 IR、NEFF、runtime ioctl、GPSIMD ISA** 等下层细节。

---

## 查阅策略

### 触发词 → 优先 wiki

| 用户/任务关键词 | 优先打开 |
|----------------|----------|
| NEFF 格式、编译产物结构 | neuronx-cc `formats/` + neuronx-runtime NEFF parse 章节 |
| NKI kernel 如何降到硬件 | neuronx-cc `nki/` + `walwalrus/` |
| Penguin IR、HLO 优化 pass | neuronx-cc `hlo-opt/`、`penguin/` |
| Trainium 引擎、Tonga ISA | neuronx-cc `arch/`、`isa/` |
| GPSIMD custom op、Xtensa | neuronx-gpsimd |
| Collective、EFA、multi-node | neuronx-runtime Part IX–XII |
| CUDA PTX/SASS 编译阶段 | ptxas、tileiras、cicc |
| TPU PJRT、LLO ISA | libtpu |
| Fat binary 解包 | GitHub fatbin readme |

### 推荐工作流

1. **先官方 doc 定边界**：例如 [AWS Neuron Compiler](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/compiler/index.html) 确认用户可见概念与 flag 名称。
2. **再 crucible 定 internals**：用 mdBook 搜索（`S` 或 `/`）定位 IR/pass/符号名。
3. **记录 pin 版本**：每本 wiki 页头通常 pin 到特定 wheel/deb 版本（如 `neuronx_cc 2.24.5133.0`）——引用时写清版本，避免与当前 SDK 2.30 混用。
4. **交叉验证**：对关键 claim（IR 名称、pass 顺序、struct layout）查官方 release notes、开源 NKI compiler、或本地 `strings`/`readelf` 抽检；无法验证则降级为「推断」。
5. **成稿标注**：survey / memo 中 crucible 来源单独成节或脚注，不与 Tier 1 官方引用混排为同等可信度。

### 获取页面内容

- 优先 `WebFetch` / 浏览器打开 wiki 章节 URL
- 大部头 topic 可派 subagent 并行读不同 Part（遵循 `workflow_parallel_subagents.md`）
- GitHub repo 含源码化笔记与 `fatbin` 工具：https://github.com/GrigoryEvko/crucible-notes

---

## 验收标准

任务算完成当且仅当：

1. **路由正确**：打开的 wiki 与问题域匹配（未用 ptxas wiki 答 Neuron NEFF 问题）
2. **免责到位**：输出含 crucible-notes 非权威声明；每个 internals claim 有 URL + 验证状态
3. **版本 conscious**：引用了 wiki 内 pin 的 binary/build 版本（若页面提供）
4. **官方对照**：至少一条相关官方 doc URL 用于 corroborate 或划定「仅 crucible 声称」边界
5. **关系清晰**：Neuron 多 wiki 场景下，说清数据流（compile → NEFF → runtime → firmware）

---

## 方法论说明（来源透明）

crucible-notes 方法论（[站点 Methodology](https://gh.evko.io/crucible-notes/)）：对公开分发的 stripped x86-64 ELF 做 IDA Pro 静态分析；**不使用源码或未公开材料**。Neuron runtime 的 DKMS 部分为 GPL 源码，置信度高于纯 symtab 推断。

wiki 内常用置信度标记（neuronx-cc [Methodology & Confidence Model](https://gh.evko.io/crucible-notes/neuronx-cc/)）：
- **Certain** — 符号/DWARF/源码行直接支持
- **Inferred** — 模式匹配或间接证据
- 页内 **CORRECTION** — 早期 scaffold 被后续证据推翻；读旧摘要时注意

---

## 已知陷阱

| 陷阱 | 表现 | 应对 |
|------|------|------|
| 当官方文档用 | 直接写「NEFF 由 X pass 生成」而不验证 | 必须标注来源层级；行为/API 以 AWS docs 为准 |
| 版本漂移 | wiki pin 2.24，用户环境 Neuron 2.30 | 引用时写 pin 版本；差异点查 [What's New](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/whats-new.html) |
| 未完成章节 | 侧边栏无链接 ≠ 不存在，可能是 planned | 见各 wiki「pages land part-by-part」说明；缺失处勿编造 |
| Companion wiki 漏读 | 只读 compiler 不理解 runtime load | Neuron 问题默认检查三 wiki  spine |
| 与 survey 报告混淆 | 把产品规格和 IR pass 名混在一节 | 产品层见 `aws_neuron_survey_*`；internals 单独节 |

---

## 快速链接

- 首页：https://gh.evko.io/crucible-notes/
- GitHub：https://github.com/GrigoryEvko/crucible-notes
- AWS Neuron 官方（对照用）：https://awsdocs-neuron.readthedocs-hosted.com/en/latest/
- 本 workspace Neuron 产品调研：`contexts/survey_sessions/aws_neuron_survey_20260626.md`
