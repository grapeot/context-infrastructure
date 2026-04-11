# Temu 跟价&限流 — 让每件商品的售价都不比竞品贵

:::metric
3|核心定价公式
6+|对接竞品平台
3|数据看板体系
5|可执行调价动作
:::

## 谁在用这套系统

这套跟价&限流体系服务于 Temu 的**国家线运营团队**和**中台定调价产品团队**。

- **国家线国长/调价业务产品**：负责本国定价策略，决定折扣系数、跟价上下限实验、非跟价品调价方案
- **中台产品**：维护跟价算法和限流规则，监控各站点的价格竞争力和高价率
- **招商/品类运营**：通过比价看板和限流看板，定位具体商品的价格问题，操作同款黑白名单

核心目标只有一个：**确保 Temu 上每件有竞品同款的商品，售价都不比竞品贵**——如果做不到，就限制这件商品的流量，避免用户看到"贵"的商品。

## 跟着一件商品走一遍定价流程

### 第一步：找到竞品同款——谁是"左i"和"右i"

你是一个国家线运营，打开[售价比价看板](tip:全托/半托和本本模式分别有不同的看板入口，均在 OMS 系统中)，看到一件 Temu 上在售的商品——这就是**左i**。

系统会去 Amazon、Shein 等竞品平台抓取商品信息，通过算法匹配找到**同款商品**。这些站外同款就是**右i**。

:::demo
<div class="max-w-md mx-auto">
  <div class="card mb-md">
    <div class="text-xs text-gray mb-sm">左i · Temu 在售商品</div>
    <div class="row" style="align-items:center;gap:12px">
      <div style="width:48px;height:48px;background:#eee;border-radius:6px;display:flex;align-items:center;justify-content:center">
        <span class="text-xs text-gray">图</span>
      </div>
      <div class="col" style="flex:1">
        <div class="text-md text-bold">运动蓝牙耳机</div>
        <div class="text-sm text-gray">当前供价 $10 · 建议价 $12.6</div>
      </div>
      <div class="pill pill-filled">跟价品</div>
    </div>
  </div>
  <div style="text-center;margin:8px 0">
    <div class="text-xs text-gray" style="text-align:center">↕ 算法匹配同款</div>
  </div>
  <div class="card">
    <div class="text-xs text-gray mb-sm">右i · 竞品平台同款</div>
    <div style="display:flex;flex-direction:column;gap:8px">
      <div class="row" style="align-items:center;gap:12px">
        <div class="pill pill-outline" style="min-width:64px;text-align:center">Amazon</div>
        <div class="text-sm" style="flex:1">同款耳机</div>
        <div class="text-bold">$11.5</div>
      </div>
      <div class="divider"></div>
      <div class="row" style="align-items:center;gap:12px">
        <div class="pill pill-outline" style="min-width:64px;text-align:center">Shein</div>
        <div class="text-sm" style="flex:1">同款耳机</div>
        <div class="text-bold">$13.0</div>
      </div>
    </div>
    <div class="text-xs text-gray" style="margin-top:8px">→ 取最低价右i：Amazon $11.5</div>
  </div>
</div>
:::

:::callout
**跟价 vs 限流的同款标准不同：** 跟价范围更广（"相似度较高的同款"即可），限流要求更严格（"严格同款"）。也就是说，一件商品可能有跟价对象但没有限流对象。
:::

> **如果没找到同款：** 这件商品归类为"非跟价品"，不参与自动跟价。但这不代表它真的没有竞品——很多时候是算法漏召。非跟价品的高价风险反而更大。

### 第二步：计算跟价目标价格——打几折跟

找到最低价右i后，系统用一个折扣系数来计算**跟价目标价格**：

> 跟价目标价格 = 最低价右i售价 × 跟价折扣系数

[跟价折扣系数](tip:可在 oms-marketing 折扣配置页面查看，按站点和竞品平台分别配置。折扣来源是按照站点下竞品平台的抽佣率确定的)不是一个固定值——它按**站点×竞品平台**配置，分为 EU、GLO 等区域。比如对 Amazon US 的折扣可能是 0.9，意思是 Temu 的目标售价 = 竞品价格的 90%。

:::callout
**折扣系数的商业含义：** 折扣系数 0.9 意味着"我们要比竞品便宜 10%"。这个 10% 覆盖了竞品平台的抽佣成本差异——竞品平台抽佣高，所以同样售价下，Temu 的实际利润空间更大。
:::

但你不能无限制地跟低价，也不能让定价高于市场认知。所以系统给跟价结果设了上下限：

:::mermaid
graph LR
  A["跟价目标价格<br/>右i × 折扣系数"] --> B{"取 min"}
  C["跟价上限<br/>（通常=市场建议价）"] --> B
  B --> D{"取 max"}
  E["跟价下限<br/>（通常=不亏损成本）"] --> D
  D --> F["最终跟价结果"]
  style F fill:#37352f,color:#fff
:::

核心公式一句话：

> **跟价结果 = max( min( 跟价目标价格, 跟价上限 ), 跟价下限 )**

翻译成人话：先别超过建议价天花板，再保证不低于成本底线。

:::tooltip
**跟价上限**通常等于市场建议价（MSP），由定调价产品团队维护。**跟价下限**通常等于不亏损成本，即供价 ×（1 + 固定成本率）。当有补贴实验时，下限可以下调至不亏损成本的 0.6 倍，即允许亏损换增量。
:::

### 第三步：三种经典跟价场景——看结果怎么算

用一个真实例子走一遍。假设你管理的一件商品：
- 当前供价 = $10，固定成本 5%
- 市场建议价 = $12.6，不亏损成本 = $10.5
- 跟价折扣系数 = 0.9

:::tabs
::tab[场景A：竞品价低，跟到底线]
右i 最低价 = $11.5

跟价目标 = 11.5 × 0.9 = **$10.35**

跟价结果 = max( min(10.35, 12.6), 10.5 ) = **$10.5**

目标价 $10.35 低于不亏损成本 $10.5，所以被兜底到 $10.5。**跟不动了——价格到底了。**

::tab[场景B：竞品价适中，完美跟到]
右i 最低价 = $12

跟价目标 = 12 × 0.9 = **$10.8**

跟价结果 = max( min(10.8, 12.6), 10.5 ) = **$10.8**

目标价在上下限之间，完美跟到。**这是最理想的状态。**

::tab[场景C：竞品价高，顶到天花板]
右i 最低价 = $15

跟价目标 = 15 × 0.9 = **$13.5**

跟价结果 = max( min(13.5, 12.6), 10.5 ) = **$12.6**

目标价 $13.5 超过建议价 $12.6，被压到建议价。**不会继续涨价——有天花板。**
:::

:::demo
<div class="max-w-md mx-auto">
  <div class="text-sm text-bold mb-sm">跟价结果落区示意</div>
  <div style="position:relative;height:60px;margin:16px 0">
    <div style="position:absolute;left:0;right:0;top:28px;height:4px;background:#eee;border-radius:2px"></div>
    <div style="position:absolute;left:15%;top:28px;height:4px;width:55%;background:#37352f;border-radius:2px"></div>
    <div style="position:absolute;left:15%;top:8px;text-align:center">
      <div class="text-xs text-bold">$10.5</div>
      <div style="width:2px;height:12px;background:#37352f;margin:0 auto"></div>
    </div>
    <div style="position:absolute;left:70%;top:8px;text-align:center;transform:translateX(-50%)">
      <div class="text-xs text-bold">$12.6</div>
      <div style="width:2px;height:12px;background:#37352f;margin:0 auto"></div>
    </div>
    <div style="position:absolute;left:5%;top:42px;text-align:center">
      <div style="width:2px;height:8px;background:#aaa;margin:0 auto"></div>
      <div class="text-xs text-gray">下限<br/>不亏损成本</div>
    </div>
    <div style="position:absolute;left:67%;top:42px;text-align:center;transform:translateX(-50%)">
      <div style="width:2px;height:8px;background:#aaa;margin:0 auto"></div>
      <div class="text-xs text-gray">上限<br/>建议价</div>
    </div>
  </div>
  <div class="row" style="justify-content:space-between;margin-top:32px">
    <div class="text-xs text-gray">← 竞品更便宜（被兜底）</div>
    <div class="text-xs text-gray">竞品更贵（被压顶）→</div>
  </div>
</div>
:::

:::impact
触发点: 调整跟价折扣系数（如从 0.9 上调到 0.95）
- 跟价目标价格上升 → 更多商品定价上涨
- 限流折扣同步上浮 → 更多商品脱离限流状态
- 如果竞品有漏召的更低价同款，涨价后测评高价率上升
- 折扣上浮带来的利润空间 = 跟价折扣与核价折扣之间的价差
:::

### 第四步：判断是否限流——贵了就降曝光

跟价完成后，系统还要做一件事：检查你的最终售价是否仍然"太贵"。这就是**限流**。

限流有自己的折扣系数，计算方式类似：

> 限流目标价 = 最低价右i售价 × 限流折扣系数

**判断规则很简单：** 如果跟价后的售价 > 限流目标价 → 高价，需要限流。

:::callout
**限流折扣 ≥ 跟价折扣。** 这意味着限流的标准比跟价更"宽松"——只要你跟价跟到了，通常不会被限流。限流主要抓的是"跟不到价"的商品（比如场景A中被兜底到不亏损成本的品）。
:::

:::callout
**当站点×平台配置了核价折扣时：** 限流折扣 = max(核价折扣 ×(1+支付手续费), 原限流折扣)。核价折扣会拉高限流门槛，让更多品被限流。
:::

限流的惩罚是**重度流量打压**——90% 以上的曝光被砍：

:::demo
<div class="max-w-md mx-auto">
  <div class="text-sm text-bold mb-md">限流对商品曝光的影响</div>
  <div class="card mb-sm" style="border-left:3px solid #37352f">
    <div class="row" style="justify-content:space-between;align-items:center">
      <div>
        <div class="text-sm text-bold">搜索场景</div>
        <div class="text-xs text-gray">同相关性下排到最后</div>
      </div>
      <div class="badge badge-dark">极低曝光</div>
    </div>
  </div>
  <div class="card mb-sm" style="border-left:3px solid #37352f">
    <div class="row" style="justify-content:space-between;align-items:center">
      <div>
        <div class="text-sm text-bold">推荐场景</div>
        <div class="text-xs text-gray">非店铺推荐基本无曝光</div>
      </div>
      <div class="badge badge-dark">几乎不可见</div>
    </div>
  </div>
  <div class="card" style="border-left:3px solid #aaa">
    <div class="row" style="justify-content:space-between;align-items:center">
      <div>
        <div class="text-sm text-bold">店铺内</div>
        <div class="text-xs text-gray">沉到店铺底部，最后展示</div>
      </div>
      <div class="badge badge-gray">低优先级</div>
    </div>
  </div>
</div>
:::

接着前面的例子，场景A中跟价结果 = $10.5，限流目标 = 0.9 × $11.5 = $10.35。**$10.5 > $10.35，高价，限流！** 这件商品虽然已经跟到底线了，但依然比竞品贵——曝光被砍。

> **如果限流折扣调高了（比如 0.99）：** 限流目标变成 0.99 × $11.5 = $11.39，此时 $10.5 < $11.39，不高价，不限流。所以调高限流折扣可以解救一批品。

:::impact
触发点: 上调限流折扣系数
- 限流标准变宽松 → 一批原本被限流的商品恢复曝光
- 如果这些商品实际比竞品贵（算法漏召了更低价同款），解限后用户会看到贵的品
- 测评高价率可能上升——被解限的品如果真的贵，就会被人工测评发现
:::

### 第五步：站内高供品的特殊逻辑——先提 ROI 再跟价

有一类特殊商品叫**站内高供品**：Temu 上同款的多个供应商中，它的供价明显偏高。

:::callout
**判断标准：** 左i 的日常供价 > 站内最低日常供价 × 1.03。也就是说，给了 3% 的缓冲空间，超过这个才算"高供"。
:::

举个例子：你管理的商品A日供 $10——
- 站内同款B日供 $9.7 → A的供价 $10 > 9.7 × 1.03 = $9.99 → **A是站内高供品**
- 站内同款C日供 $9.9 → A的供价 $10 < 9.9 × 1.03 = $10.19 → **A不是高供品**

站内高供品的处理逻辑不同：

:::mermaid
graph TD
  A["判断：左i是站内高供品？"] -->|是| B["跟价：直接定到市场建议价<br/>（不走常规跟价公式）"]
  A -->|否| C["走常规跟价流程"]
  B --> D{"建议价 vs 限流目标价"}
  D -->|"建议价 > 限流目标"| E["高价 → 限流"]
  D -->|"建议价 ≤ 限流目标"| F["不限流"]
  E --> G["降供目标 = min(站内最低日供×1.03, 限流目标倒推供价)"]
  style E fill:#37352f,color:#fff
:::

**为什么这么设计？** 站内高供品的核心问题是供价高，不是售价策略问题。让它先定到建议价（相对高的售价），然后通过限流给供应商降供压力。供应商降供到达标线后，解除高供标签，重新进入常规跟价——这时候才真正跟竞品比价格。

:::tooltip
**降供目标的计算：** min(站内最低日供 × 1.03, 限流目标售价倒推供价)。两个值取更小的——既要求不比站内同款贵太多，也要求售价达到竞品水平。供应商降到这个值后，高供标签解除，商品进入正常跟价&限流流程。
:::

:::impact
触发点: 站内高供品逻辑上线
- 高供品不再跟价降价 → 这些品定在建议价，售价相对更高
- 更多高供品被限流 → 但限流后不计入高价率分子（因为算法找到了真实同款）
- 供应商收到降供信号 → 降供后解除标签，进入正常跟价，最终实现供价和售价双降
:::

### 第六步：国家线的五大调价动作

作为国家线运营，你有以下五个"操纵杆"可以拉：

:::tabs
::tab[1. 下调跟价下限]
**目的：** 让更多品跟到目标价，解限流（代价是亏损）

典型场景：BSR（Best Seller Ranking）跟价品补贴实验，下限从 1 倍不亏损降到 0.6 倍。

例：右i = $10，跟价目标 = $9，正常下限 $10.5 跟不到 → 下调到 $6.3 后跟到 $9，解除限流。

**高价率影响：** 双刃剑。降价可能降低高价率，但解限流后如果有漏召的更低价同款，高价率反而上升。

::tab[2. 上调跟价上限]
**目的：** 提升建议价附近商品的 ROI

例：原上限=建议价 $12，上调到 1.1 倍后=$13.2。竞品价 $20 时，定价从 $12 涨到 $13.2。

**高价率影响：** 风险较大。由于同款漏召问题，涨价后测评找到更低价同款的概率增加。

::tab[3. 调整跟价折扣]
**目的：** 提利润

跟价折扣上浮（如 0.9→0.93），跟价目标价和限流目标价同步上升，实现涨价且不限流。

**高价率影响：** 有天花板兜底（建议价和线上同款价），风险相对可控。

::tab[4. 调整限流折扣]
**目的：** 减少限流（非必要不建议做）

只上浮限流折扣，不动跟价折扣。一般用于站点经营成本比竞品差距过大、降供难度大的场景。

**高价率影响：** 被增量解限流的品如果实际比竞品贵，测评高价率直接上升。

::tab[5. 非跟价品调价]
**目的：** 降高价率 / 提利润

非跟价品没有线上同款做价格天花板，涨价对高价率影响最大。降价则对高价率最友好。

**操作建议：** 对限流率高且测评高价率高的类目，优先测降价；ROI 目标先跟类目平均拉齐。
:::

## 降高价率的完整操作手册

当你的国家测评高价率偏高时，按以下流程操作：

:::sequence
sequenceDiagram
  participant 你 as 国家线运营
  participant 测评 as 测评系统
  participant 看板 as 数据看板
  participant 调价 as 调价系统

  你->>测评: 1. 提测评需求/自测，确定真实高价率
  测评-->>你: 返回高价率水平
  你->>看板: 2. 查 Top GMV 类目的三级类目高价率
  看板-->>你: 定位高价率高的类目
  你->>看板: 3. 查这些类目的限流率
  看板-->>你: 限流率 = 高价限流SKU数/有同款SKU数
  你->>调价: 4. 对高危类目的非跟价品降ROI实验
  调价-->>你: 执行降价
  你->>测评: 5. 对实验类目自测高价率变化
  测评-->>你: 验证效果
:::

:::callout
**限流率高的类目 = 真实高价概率更高的类目。** 逻辑是：如果在算法已找到同款的品里，高价限流比例就很高，那在算法没找到同款的品里（非跟价品），高价的概率只会更大。
:::

> **如果降价效果不明显：** 检查比价规则过滤量级——可能大量同款在 merge 层到 hive1 层之间被过滤掉了，导致本该是跟价品的变成了非跟价品。

## 关键决策点

### 跟价折扣系数

一句话：决定了 Temu 要比竞品便宜多少。

**怎么产生：** 按站点×竞品平台配置，基于竞品平台的抽佣率确定。在 oms-marketing 折扣配置页面维护。

**影响范围：** 折扣上浮 → 所有跟价品目标价上升 → 涨价品增多 + 限流品减少 → 利润提升但高价风险增加。折扣下调 → 反向效果。

### 限流折扣系数

一句话：决定了"贵到什么程度"才会被限流。

**怎么产生：** 默认等于跟价折扣。站点有特殊需求时可独立配置，但必须 ≥ 跟价折扣。有核价折扣时，取 max(核价折扣×(1+支付手续费), 原限流折扣)。

**影响范围：** 限流折扣是跟价和限流之间的"缓冲区"。上调 → 缓冲区变大 → 更多品免于限流但可能实际高价。

### 测评高价率

一句话：人工抽检发现的真实高价比例，是衡量价格竞争力的最终标准。

**怎么产生：** 线下人工测评，或国家线自测。覆盖线上跟价可能漏召的同款。

**影响范围：** 高价率是所有调价动作的"审判官"——线上限流率再低，如果测评高价率高，说明有大量漏召的高价品。所有涨价操作都需要评估对测评高价率的影响。

## 数据看板与排查工具

### 日常监控看板

| 看板 | 用途 | 入口 |
|------|------|------|
| 售价比价看板 | 查看单品的同款匹配和比价结果 | OMS 系统（全托/半托/本本分别有入口） |
| 限流看板 | 查看限流商品列表和限流原因 | OMS 系统（glo/eu/udp 三区独立） |
| 同款黑白名单 | 手动干预同款匹配关系 | OMS 系统（仅 global） |
| 跟价占比大盘 | 跟价品占大盘的比例趋势 | Matrix 报表 |
| 跟价价格变化趋势 | 今日跟价 vs 昨日定价的涨降分布 | Matrix 报表 |

### ROI 下降排查流程

当你发现跟价品 ROI 在下降，按这个思路排查：

:::mermaid
graph TD
  A["ROI 下降"] --> B{"跟价品和非跟价品<br/>都在降？"}
  B -->|"都降"| C["站点大盘在整体降价<br/>检查售价策略是否屏蔽了跟价品"]
  B -->|"只有跟价品降"| D{"有新的补贴实验<br/>上线吗？"}
  D -->|有| E["确认实验影响范围"]
  D -->|没有| F["拆分跟价价格变化<br/>看哪个平台降价品变多"]
  F --> G{"同款覆盖率<br/>有变化？"}
  G -->|"提升了"| H["新增了更多低价同款<br/>（该平台爬到更多品）"]
  G -->|"没变"| I["该平台的右i价格在降<br/>（竞品在降价促销）"]
:::

### 限流目标供价的倒推

当商品被限流时，系统会倒推一个**目标供价**，告诉供应商"降到多少就能解限流"：

:::tabs
::tab[有核价折扣]
目标日常供价 = 核价目标供价

例：竞品 $11，核价折扣 0.9 → 目标供价 = (11 × 0.9 - 运费) / (1 + 增值税) = $9.9

::tab[无核价折扣]
目标日常供价 = 按定价公式倒推

例：竞品 $11，跟价折扣 0.9 → 跟价目标售价 = $9.9

设目标供价 = x → 9.9 = x × (1 + 固定成本 5%) × (1 + 增值税) → 解出 x
:::

## 附录：术语对照表

| 术语 | 含义 |
|------|------|
| 左i | Temu 平台上在售的商品（我方商品） |
| 右i | 竞品平台上的同款商品（竞对商品） |
| 跟价品 | 系统找到了竞品同款、可以自动定价的商品 |
| 非跟价品 | 未找到竞品同款的商品（可能是算法漏召） |
| 跟价折扣系数 | 跟价时乘以右i价格的系数，决定比竞品便宜多少 |
| 限流折扣系数 | 判断是否高价限流的折扣系数，≥ 跟价折扣 |
| 核价折扣 | 平台对供应商的核价标准折扣 |
| 不亏损成本 | 供价 × (1 + 固定成本率)，即不亏损的最低售价 |
| 市场建议价 / MSP | 市场认知的合理售价上限 |
| 站内高供品 | 供价 > 站内最低同款供价 × 1.03 的商品 |
| BSR | Best Seller Ranking，平台畅销品 |
| ROI | 投入产出比，衡量利润水平 |
| 测评高价率 | 人工测评中发现的真实高价商品比例 |
| merge 层 | 算法匹配同款的原始结果层 |
| hive1 / 比价层 | 经过比价规则过滤后的同款结果层 |
| 全托/半托/本本 | 不同的供应商合作模式 |

