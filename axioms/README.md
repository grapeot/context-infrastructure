# 课代表立正（孙煜征）— 认知公理系统

> 从 6M+ 字的真实语料中提炼的 20 条认知与表达公理。

## 这是什么

这是**课代表立正（孙煜征）**的个人认知画像——不是他自己写的"人生信条"，而是由他的 cofounder 鸭哥通过系统性数据分析，从他多年公开与私下表达中**逆向工程**出来的决策原则。

每条公理都经过跨数据源交叉验证，标注了可信度、边界条件和代表性证据，目的是让 AI（或任何协作者）能准确预测他在特定场景下的判断倾向。

## 数据基础

| 数据源 | 规模 | 时间跨度 |
|--------|------|----------|
| YouTube 逐字稿 | 498 期，~3.87M 字 | 2020–2026 |
| 微信群聊/私聊 | 18 个对话，~2.49M 字 | 2023–2026 |
| Circle 社区帖子 | 123 篇，~537K 字 | 2024–2026 |

总计约 **6.9M 字**，经过 20 轮迭代提炼。

## 公理一览

### 观点类（Content）— 14 条

| 编号 | 文件 | 核心主张 | 可信度 |
|------|------|----------|--------|
| K01 | [世界模型](k01_world_model.md) | 人生天花板取决于认知质量，提升世界模型是最高杠杆 | 9 |
| K02 | [SOWH](k02_strong_opinions_weakly_held.md) | 深度积累→强观点→主动 steelman→寻求被打脸 | 8 |
| K03 | [复利](k03_compounding.md) | 减少波动 > 提高均值，赛道聚焦 > 多元 | 8.5 |
| K04 | [反过早简化](k04_anti_premature_closure.md) | 有价值的简化是拆解，有害的简化是判决 | 8.5 |
| K05 | [Users to Builders](k05_users_to_builders.md) | 技能贬值、资产升值，Builder→Architect 是阶梯 | 8.5 |
| K06 | [定义自己的游戏](k06_define_your_game.md) | 痛苦来自玩别人的规则，方向不是终点 | 8.5 |
| K07 | [二层认知](k07_two_layer_cognition.md) | 方向层 = Science + 思考，执行层 = Craft + 行动 | 8 |
| K08 | [分发瓶颈](k08_distribution_bottleneck.md) | Builder 最被低估的瓶颈是销售 | 7.5 |
| K09 | [AI-native](k09_ai_native.md) | 挥霍代码、节约认知。前提是 architect 能力 | 8.5 |
| K10 | [善意独裁者](k10_benevolent_dictator.md) | 社区治理：最终决定权 + 程序公正 | 8.5 |
| K11 | [环境 > 个人努力](k11_environment_over_effort.md) | 环境是最大决定因素，抱怨是最差回应 | 7 |
| K12 | [Coachability](k12_coachability.md) | 职业元技能，核心是"人情估值" | 7 |
| K13 | [Narrative 杠杆](k13_narrative_as_leverage.md) | 定价是讲故事，生态位是 narrative *(私聊独有)* | 7 |
| K14 | [人生即游戏](k14_life_as_game.md) | 把事业当 MMORPG，钱是奖励不是目的 *(私聊独有)* | 7 |

### 风格类（Form）— 6 条

| 编号 | 文件 | 核心主张 | 可信度 |
|------|------|----------|--------|
| KS01 | [具体锚点 + 命名框架](ks01_concrete_anchors_named_frameworks.md) | 数字/故事引入 → 有编号的命名框架收束 | 8.5 |
| KS02 | [自我暴露弱点](ks02_vulnerability_as_pedagogy.md) | 用失败和矛盾当教材，建立信任 | 8 |
| KS03 | [思考过程外化](ks03_thinking_in_public.md) | 展示推导而非断言结论，邀请参与 | 8 |
| KS04 | [反直觉开场](ks04_counter_intuitive_hook.md) | 反常识命题做 hook，排斥 buzzword | 8 |
| KS05 | [高分辨率批评处理](ks05_high_resolution_criticism.md) | 批评分流：信息价值→优化，噪音→忽略 | 8.5 |
| KS06 | [社区是 peer lab](ks06_community_as_peer_lab.md) | 不是课堂，是共同实践者的平行实验 | 8 |

## 每条公理的结构

```
# 标题

## 核心表述        ← 一段话概括
## 展开            ← 完整论述 + 演化过程
## 边界条件        ← 什么时候不成立
## 代表性证据      ← 带出处的原始引用
## 跨源表现        ← YouTube / Circle / 微信中的不同面向
## 可信度          ← 1-10 分 + 评分理由
```

## 关系图

```
                    ┌──── K01 世界模型 ────┐
                    │    (终极目标)        │
                    │                     │
              K02 SOWH ◄──────────── K04 反过早简化
              (更新机制)              (质量保护)
                    │
         ┌──────────┼──────────┐
         │          │          │
    K07 二层认知   K03 复利   K12 Coachability
    (Science/Craft) (时间策略) (学徒制入口)
         │          │
    K09 AI-native  K08 分发瓶颈 ── K13 Narrative(私下版)
    (代码层应用)   (公开版)
         │
    K05 Builder ◄────────── K06 定义自己的游戏
    (how: 建造)              (why: 逃离外部规则)
                                    │
                              K14 人生即游戏(私下版)
                              K11 环境>努力

    治理层: K10 善意独裁者 ◄──► KS06 社区 peer lab

    表达层: KS01 框架化 ◄──► KS03 思考外化
            KS02 自我暴露 ◄──► KS04 反直觉hook
            KS05 批评分流
```

## 怎么用

**给 AI 用**：把这些公理加载到 AI 的 context 中，它就能在帮你做内容创作、社区运营、商业决策时，按照你的真实思维方式来工作——而不是输出"正确的废话"。

**给协作者用**：在不确定"他会怎么想"的时候，查一下对应场景的 axiom。每条都有触发场景和失效场景（见 [INDEX.md](INDEX.md)），帮你判断什么时候该用、什么时候不该用。

**给自己用**：这是一面镜子。看看数据说你是谁，和你以为的自己是不是同一个人。

## 关于

- **画像对象**：孙煜征 / 课代表立正 — [YouTube](https://www.youtube.com/@kedaibiao) · [Superlinear Academy](https://superlinear.academy)
- **提炼者**：鸭哥 ([@grapeot](https://github.com/grapeot)) — cofounder, context infrastructure 作者
- **方法论**：语义搜索 + 跨源交叉验证 + 20 轮迭代，详见 [context infrastructure 博客](https://yage.ai/context-infrastructure.html)

## License

MIT
