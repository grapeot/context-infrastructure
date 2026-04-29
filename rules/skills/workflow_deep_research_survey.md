# 深度调研工作流

## 元数据

- **类型**: Workflow
- **适用场景**: 需要对某个主题进行深度、全面、可验证的第三方调研
- **输出位置**: `contexts/survey_sessions/`
- **创建日期**: 2026-02-19
- **最后更新**: 2026-03-30

## 核心原则

1. **激励感知验证**: 信息价值取决于来源的激励结构。厂商叙事有用但不能自证。每个主要 claim 都必须追溯到与发布方激励无关的独立证据。
2. **交叉验证**: 多个 sub-agent 覆盖有重叠的主题，用分歧和矛盾暴露盲区。
3. **可追溯性**: 所有引用保留 URL，关键引用保留原文摘录，不依赖总结。
4. **逐步聚焦**: 先扫描全貌，提取 claim，再分维度深入验证。
5. **单一主交付 + 可复用工件**: 最终报告一份，关键中间工件存入 session 目录。
6. **共享 research spine，分叉 reader mode**: 搜索、验证、工件留存共享；成稿前按读者决定 internal / external mode。

## 信息源层级

每次调研中，来源可信度不是对等的。按激励结构分层：

| 层级 | 类型 | 信号特征 | 使用方式 |
|------|------|----------|----------|
| Tier 1 | 厂商官方文档、blog、case study | 告诉你产品想被怎么看 | 提取 claim，不做验证依据 |
| Tier 2 | Press coverage、sponsored review、第三方评测 | 能理解市场定位，但激励仍偏正面 | 辅助理解市场叙事，不作为独立证据 |
| Tier 3 | 独立开发者 blog、HN/Reddit 讨论、Stack Overflow | 信号更强，但采样有偏 | 作为验证信号，注意社区偏差 |
| Tier 4 | GitHub issues、migration stories、production post-mortems、commit history | 行为证据而非态度表达；做迁移的成本远高于发一条好评 | 最高可信度，用于验证 claim 和标注边界 |

证据可信度递增排列：态度表达（"我觉得不错"）< 使用场景描述 < 对比决策记录 < Migration stories < Production post-mortems < 代码/commit 级证据。优先收集后半部分。

## 两种 reader mode

按**读者上下文是否已知且厚重**来区分，不要按渠道理解。

**Mode A：Internal（共享上下文驱动的决策备忘录）** 适用于读者是自己或共享长期上下文的协作者。写作契约：不复述共同常识；重点展开会改变结论的未知点、最可能被反对的点、与既有观点冲突的点；优先交付结论、依据、未决问题和建议动作。

**Mode B：External（零预设上下文的可发布论证）** 适用于读者不是已知对象。写作契约：必须显式回答 why this matters；必须把最有用的判断放在前几段；关键定义、比较框架和限定条件写在页面上，不留在读者脑内补全。

External mode 选定后，还需要回答一个更根本的问题：**这件事对目标读者的 relevance 是现在的、将来的、还是现在大概率不相关？** 很多调研对象的真实答案是第三种——短期和大多数读者没有直接关系，但长期可能重要。如果是这种情况，文章的 thesis 必须正面承认这一点，而不是通过堆叠炫目案例来暗示短期价值比实际更大。承认"现在不相关"不等于"不值得写"；值得写的原因可能恰恰是帮读者区分短期噪音和长期信号。

先问三个问题再选 mode：(1) 这个读者是否已知且共享厚重上下文？(2) 主要价值是帮对方更快判断还是让对方理解并相信？(3) 拿掉私有背景后报告能否独立成立？偏共享上下文和快速判断用 internal；偏自足、传播和说服用 external。

## 工作流程

### Phase 1: 初步扫描 + Claim 提取

**目标**: 了解全貌，区分厂商叙事、市场叙事和独立证据，提取待验证 claim。

**操作**:

1. 用 Tavily 进行 2-3 次搜索，覆盖：
   - 调研对象的基本描述（Tier 1 官方信息）
   - 市场评价和媒体报道（Tier 2 市场叙事）
   - 批评、争议、已知问题（Tier 3-4 信号）
2. 总结 3-5 个需要深入调研的维度。
3. **Claim 提取**：从 Tier 1-2 源中列出产品/对象的关键主张（性能、适用场景、成本、优势等），对每个 claim 标注验证通道：这个 claim 在哪种 Tier 3-4 源中能被证实或证伪？将验证任务编入 Phase 2 的 sub-agent prompt。

**输出**: 写入 `tmp/<session_slug>/scratchpad.md`，包含 claim extraction 表格：

```markdown
## Claim Extraction

| Claim | 来源 (Tier) | 验证通道 | 验证状态 |
|-------|-------------|----------|----------|
| "zero-config，开箱即用" | Tier 1 官方文档 | GitHub issues 搜 setup pain；Reddit 搜迁移故事 | 待验证 |
| "成本低于竞品" | Tier 1 官方 blog | Production post-mortem；独立 benchmark | 待验证 |
```

### Phase 1.5: Prior Work 定位（学术论文调研时必做）

**触发条件**：调研对象是一篇学术论文，或调研主题的核心依据是一篇/一组论文。如果调研对象是产品、公司或纯行业话题，跳过此步。

**为什么需要这一步**：论文的 Related Work 和 Contribution 声明是自利的——作者会把自己放在最有利的位置上。不读 prior work 就无法判断一篇论文到底是在发明一个新问题，还是在用一个好测量证实一个大家已经感觉到的问题。这个区分直接决定文章定位：是写成领域综述、单篇深挖、还是混合。

**操作**：

1. 读论文的 Related Work / Background 章节，提取：
   - 被引用的每一项 prior work
   - 作者如何定位自己相对于 prior work 的优势
   - 作者声称的具体增量贡献

2. 构建被引工作映射表：

```markdown
| Prior Work | 年份/出处 | 做了什么 | 没做什么 | 本文声称的优势 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

3. 对每个被引集群，外部验证 prior work 实际建立了什么（用 Tavily 搜索原始论文/博客/社区讨论，不依赖本文自己的表述）。特别关注：
   - prior work 的实际 scope 是否比本文描述的更宽或更窄
   - prior work 是否已经有独立验证或社区复现
   - 本文声称的"first to do X"是否属实

4. 基于此回答两个问题：

**增量判断**：这篇论文的真正新增是什么？
- 把"领域已知的事实"和"本文新增加的事实"分开列出
- 评估增量大小：概念层面（medium/large）、实证层面（medium/large）、实践层面（meaningful/marginal）

**定位判断**：应该写成什么？
- **A. 领域综述**：如果 prior work 已经很丰富，本文只是其中一环，且目标读者需要全貌
- **B. 单篇深挖**：如果本文的增量足够大且独立，prior work 只需 1-2 段背景
- **C. 混合（推荐默认）**：30-40% 领域背景 + 60-70% 本文聚焦。先解释为什么本文攻击的层面和 prior work 关注的层面不同，再用本文的测量/数据作为主线

**产出**：写入 scratchpad 的 `## Prior Work Positioning` 部分。如果启动了 sub-agent 做此步，结果也存入 `tmp/<session_slug>/prior_work_survey.md`。

**常见错误**：
- 把论文的 Related Work 当作事实接受，不外部验证 prior work 的实际 scope
- 因为论文引用了很多 prior work 就认为"这个领域很成熟"——引用多也可能说明领域碎片化
- 把"本文首次测量了 X"等同于"X 之前不存在"——测量和发现是不同的贡献类型

### Phase 2: 分割与并行调研

**目标**: 多角度深入，同时验证 Phase 1 提取的 claim。

**分割原则**:

维度划分 3-5 个，每个维度同时承担两种功能：覆盖一个主题，并验证特定 claim。维度之间必须有 ≥50% 的 overlap，让不同 agent 有机会发现相同信息的不同解读或互相矛盾的结论。

**按证据功能设计维度**，而不只是按主题：

- 官方叙事（Tier 1-2）：产品自我定义、官方案例、定价逻辑
- 独立使用体验（Tier 3）：开发者实际使用记录、社区讨论、对比决策
- 失败与边界（Tier 3-4）：已知问题、GitHub issues、限制条件、批评声音
- 迁移行为（Tier 4）：用户从竞品迁入/迁出的记录，以及原因

**启动 Sub-agent**:

同时启动 3-5 个 sub-agent，每个负责一个维度。使用以下类型：

- `librarian` — 外部调研首选，查文档、开源代码、官方资料
- `deep` category — 自主深度调研，适合复杂多源任务

```
task(
  subagent_type="librarian",
  load_skills=[],
  description="调研 XX 维度",
  run_in_background=true,
  prompt="[具体调研维度的 prompt]"
)
```

每个 sub-agent 的 prompt 中明确：
1. 具体要调研什么主题
2. 从 Phase 1 claim extraction 中提取的本维度相关 claim（要求在 Tier 3-4 源中寻找支持或反驳证据）
3. 优先返回行为证据（migration、production issue、commit history），而非态度表达（好评/差评）
4. 必须返回 URL 和原文摘录（不是总结）
5. 可以覆盖的其他相关维度（形成 overlap）

主线程把关键结论、来源索引和判断过程整理进 session 目录的 artifact 文件；不必逐字保存原始输出，但不能让关键信息只留在 stdout。

**Tavily 参数偏好**:
- `max_results=6`（覆盖不足可提至 10）
- `search_depth="advanced"`
- `include_answer=false`（直接看结果与原文摘录，不依赖聚合摘要）
- 按需启用 `include_images` / `include_image_descriptions`

### Phase 3: 整合与交叉验证

**目标**: 发现矛盾，对比 claim 在不同层级来源中的表现，形成可信结论。

**操作**:

1. 对比各 sub-agent 结果，重点关注：
   - 多个 agent 都发现的信息 → 可信度高
   - 只有单一来源的信息 → 标注来源，提醒验证
   - 互相矛盾的信息 → 特别标注，分析原因
2. 对 Phase 1 的每个 claim，核查验证状态：
   - 在 Tier 3-4 源中有独立证据 → 标注为已验证，记录来源
   - 仅在 Tier 1-2 源中出现 → 标注为"仅 vendor source，未独立验证"，不当作事实写进报告
   - Tier 3-4 源出现与 Tier 1-2 矛盾的证据 → 以 Tier 3-4 为准，记录矛盾点
3. 如发现重大矛盾，可再启动 sub-agent 针对性验证。

### Phase 4: 写作

调研的 Phase 1-3 完成后，进入写作阶段。根据目标产出类型选择路径：

**如果是 external-facing 分析文章** → 加载 `workflow_analytical_writing.md`，从 Phase A 开始执行。该 skill 包含作者的分析视角目录（Thesis Catalog）、判断合成步骤（视角匹配 → 族谱追溯 → 叙事重构 → thesis 成型）和写作规范。

**如果是 internal memo**（面向自己或共享上下文的协作者）→ 不需要完整的分析写作流程。直接写：先把最影响决策的结论和依据显出来，把仍未确认的点与下一步动作留清楚。动笔前读一遍 `rules/COMMUNICATION.md`。

**共享格式要求**（两种 mode 通用）:
- 中文 Markdown
- 所有引用必须有 URL（Markdown 链接格式），且必须使用**绝对链接**（以 `https://` 开头）。相对链接在 yage.ai 上可工作，但发布到 Circle 等第三方平台时会指向错误地址
- 关键引用保留原文摘录，不只是总结
- 如果最终交付是 external article，重要来源直接进入正文的 inline Markdown links，不只堆在文末

**Survey report 与博客文章的区别**：本 workflow 的产出是 survey report，存放在 `contexts/survey_sessions/`。不是博客文章。不要加博客 frontmatter 或 Kit 订阅 script tag。如果用户要求发布到博客，单独复制到 `contexts/blog/content/` 并加 frontmatter，这是独立步骤。

**交付终点**：写完 `contexts/survey_sessions/` 下的最终 MD 文件即为调研交付的终点。不要自动继续执行发布流程（yage share、博客、Twitter、Circle 等）。只有当用户显式要求发布时，才按对应的 skill 流程执行后续步骤。

**存储位置**: `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md`

**推荐 artifact 目录** `tmp/<session_slug>/`，至少包含：
- `scratchpad.md`（含 claim extraction 表格）
- `search_manifest.md`（含产出文件索引表、subagent 定位方式、数据覆盖评估）
- `search_notes.md`（按需）
- `source_index.md`（按需）

## Search Manifest 必须包含产出文件索引

```markdown
## 产出文件索引

| 文件 | 路径 | 说明 |
|------|------|------|
| Scratchpad | `tmp/<session_slug>/scratchpad.md` | 主线程研究笔记 |
| Search Manifest | `tmp/<session_slug>/search_manifest.md` | 本文件 |
| 最终报告 | `contexts/survey_sessions/<topic>_survey_YYYYMMDD.md` | 最终报告 |

## Subagent 原始产出

| Agent | Session ID | URLs | 状态 |
|-------|-----------|------|------|
| Agent 1 | `ses_xxx` | 50+ | completed |
```

## URL 留存规范

必须保留 URL 的情况：直接引用、数据来源（数字/统计/评分）、评价来源、官方信息。

如果最终交付是 external-facing 文章，默认要求：**重要来源直接进入正文的 inline Markdown links。** 不要把链接只堆在文末参考资料或只留在 scratchpad / manifest。正文中的判断、事实、引语，读者应能就地跳转验证。

```markdown
**来源描述**（URL）
> 原文摘录

或

某平台上有人评价（URL）：
> "原文"
> （👍 X 👎 Y）
```

避免：无 URL 的引用（"有人评价说..."）、只总结不引用原文。

如果后续要把调研写成外部文章，动笔前再做一次检查：最终成稿里是否真的保留了这些 URL，而不是只在 research artifact 里存在。

## 常见调研维度参考

| 调研对象 | 可能的维度 |
|---------|-----------|
| 产品/服务 | 功能评价、价格对比、用户案例、负面反馈、竞品分析 |
| 课程/培训 | 课程内容、讲师背景、学员评价、价格价值、替代方案 |
| 公司/组织 | 业务模式、市场地位、口碑评价、争议事件、财务状况 |
| 技术/工具 | 技术原理、使用体验、适用场景、局限性、替代方案 |
| 观点/框架 | 共识程度、权威背书、反对声音、实际落地、时间线准确性 |

## 常见陷阱

| 陷阱 | 对策 |
|-----|------|
| 只搜到正面信息 | 专门搜索"criticism", "negative review", "scam", "overpriced" |
| 信息来源单一 | 强制要求 sub-agent 找多个独立来源 |
| 过度总结丢失细节 | 要求保留原文摘录，不只是总结 |
| 维度划分太干净没有 overlap | 设计维度时故意让边缘模糊 |
| Sub-agent 返回信息太浅 | prompt 中强调"深度"、"具体"、"原文" |
| 中间文件堆积 | 集中到 `tmp/<session_slug>/`，只保留关键索引和判断 |
| 用错 subagent 类型 | 外部调研用 `librarian` 或 `deep`，`explore` 只用于内部 codebase |
| 调研结果变成 vendor marketing 汇总 | Phase 1 提取 claim，Phase 2 按证据功能分配维度，Phase 3 核查验证状态 |

写作阶段的常见失败模式（Relevance 不着地、Demo 当证据、时间维度模糊、调研汇总而非作者写作等）见 `workflow_analytical_writing.md` 的失败模式表。
