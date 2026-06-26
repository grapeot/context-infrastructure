# Kunlunxin Survey Scratchpad — 20260626

## Claim Extraction

| Claim | 来源 (Tier) | 验证通道 | 验证状态 |
|-------|-------------|----------|----------|
| Gen1 K200 256 INT8 TOPS | Tier 1 产品页 | Hot Chips 2020 PDF | 已验证 |
| Gen2 算力 2-3x Gen1 | Tier 1 官网 | R200 vs K200 规格对比 | 已验证（峰值比 2x） |
| Gen2 国内率先 GDDR6 | Tier 1 官网 | 无独立 Tier 3-4 | 仅 vendor source |
| P800 96GB HBM3 / 345 TFLOPS | Tier 2 行业分析 | 无官方 datasheet | 未独立验证 |
| P800 8卡跑 671B DeepSeek | Tier 1 新闻 | 无第三方 benchmark | 仅 vendor source |
| 万卡集群 96% 线性加速 | Tier 2 雪球/媒体 | 无公开测试报告 | 未独立验证 |
| 飞桨 III 级兼容 R200/R300 | Tier 1 新闻 | Paddle 文档 | 已验证 |

## 调研维度

1. 官方产品规格（K/R/P SKU）
2. Hot Chips 架构 internals（SDNN/Cluster）
3. 软件栈 XRE/XTCL/XDNN + 框架
4. P800 大模型生态（FastDeploy/vLLM）
5. 验证缺口与矛盾点
