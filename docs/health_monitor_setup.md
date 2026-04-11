# Health Monitor Setup Guide

Apple Watch Ultra 3 健康数据 → Mac 自动化采集 → 每日摘要 → Action Advisor 联动。

## 架构概览

```
iPhone (08:00)                    Mac
┌──────────────┐                 ┌──────────────────────┐
│ Apple Health  │                 │ health_data_receiver  │
│ (HealthKit)   │──── HTTP ────→│ (port 9876)           │
│              │   POST JSON    │ → contexts/health/data│
│ Shortcuts    │                 │                      │
│ (08:00 触发)  │                 ├──────────────────────┤
└──────────────┘                 │ health_monitor.py     │
                                 │ (08:01 launchd)       │
                                 │ → contexts/health/    │
                                 │   daily/YYYY-MM-DD.md │
                                 ├──────────────────────┤
                                 │ action_advisor.py     │
                                 │ (09:15 launchd)       │
                                 │ → 读取健康摘要        │
                                 │ → 融合进每日建议邮件   │
                                 └──────────────────────┘
```

## Step 1: Mac 端部署

### 1.1 启动 Health Data Receiver

```bash
cd ~/opencode-context-infrastructure

# 测试运行
python3 tools/health_data_receiver.py --port 9876

# 验证
curl http://localhost:9876/ping
# → {"status": "ok"}
```

### 1.2 注册 launchd 服务

```bash
# Health Data Receiver (常驻服务)
cp .local_runtime/launchd/com.zhouxuanting.opencode.health-receiver.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.zhouxuanting.opencode.health-receiver.plist

# Health Monitor (每日 08:01 定时任务)
cp .local_runtime/launchd/com.zhouxuanting.opencode.health-monitor.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.zhouxuanting.opencode.health-monitor.plist
```

### 1.3 确认 Mac 局域网 IP

```bash
ipconfig getifaddr en0
# 记下这个 IP，Shortcuts 配置时需要用到
# 例如: 192.168.1.100
```

### 1.4 (可选) 配置 Token 认证

在 `.env` 中添加：
```
HEALTH_RECEIVER_TOKEN=your-secret-token-here
```

## Step 2: iPhone Shortcuts 配置

### 2.1 创建 Shortcut

在 iPhone 上打开 Shortcuts app，创建一个新 Shortcut，命名为 **"Health Export"**。

按以下顺序添加 Action：

#### Action 1: Find Health Samples (Sleep Analysis)

```
Find Health Samples where
  Type is Sleep Analysis
  Start Date is in the last 1 day
Sort by Start Date
Limit to 20
```

保存到变量: `SleepSamples`

#### Action 2: Find Health Samples (Resting Heart Rate)

```
Find Health Samples where
  Type is Resting Heart Rate
  Start Date is in the last 1 day
Sort by Start Date
Limit to 1
```

保存到变量: `RestingHR`

#### Action 3: Find Health Samples (Heart Rate Variability)

```
Find Health Samples where
  Type is Heart Rate Variability
  Start Date is in the last 1 day
Sort by Start Date
Limit to 1
```

保存到变量: `HRV`

#### Action 4: Find Health Samples (Step Count)

```
Find Health Samples where
  Type is Step Count
  Start Date is in the last 1 day
Sort by Start Date
```

保存到变量: `Steps`

#### Action 5: Find Health Samples (Active Energy)

```
Find Health Samples where
  Type is Active Energy Burned
  Start Date is in the last 1 day
Sort by Start Date
```

保存到变量: `ActiveEnergy`

#### Action 6: Find Health Samples (Blood Oxygen)

```
Find Health Samples where
  Type is Blood Oxygen Saturation
  Start Date is in the last 1 day
Sort by Start Date
```

保存到变量: `SpO2`

#### Action 7: Build JSON (Text action)

使用 Text action 组装 JSON。由于 Shortcuts 对 HealthKit 数据的处理有限，建议用以下模板，手动插入变量：

```json
{
  "date": "{CurrentDate format:yyyy-MM-dd, adjusted -1 day}",
  "sleep": {
    "total_minutes": {SleepTotal},
    "deep_minutes": {DeepSleep},
    "rem_minutes": {REMSleep},
    "light_minutes": {LightSleep},
    "awake_minutes": {AwakeMins},
    "bedtime": "{Bedtime}",
    "wakeup": "{Wakeup}"
  },
  "heart": {
    "resting_hr": {RestingHR},
    "hrv_avg": {HRV},
    "hr_min": 0,
    "hr_max": 0
  },
  "activity": {
    "steps": {TotalSteps},
    "active_energy_kcal": {TotalActiveEnergy},
    "exercise_minutes": 0,
    "stand_hours": 0
  },
  "blood_oxygen": {
    "avg": {SpO2Avg},
    "min": {SpO2Min}
  }
}
```

> 注意：Shortcuts 中 Sleep Analysis 返回的数据需要按 category 区分 (In Bed / Asleep - Deep / Asleep - REM / Asleep - Core / Awake)，你需要用 Repeat/Filter 来分别统计各阶段时长。

#### Action 8: Get Contents of URL

```
URL: http://<你的Mac IP>:9876/health
Method: POST
Headers:
  Content-Type: application/json
  Authorization: Bearer <你的token>  (如果配置了的话)
Request Body: {上一步的 Text 输出}
```

### 2.2 配置自动化触发

1. 打开 Shortcuts → Automation → + → Time of Day
2. 时间设为 **08:00**
3. 选择 "Run Immediately"
4. Action: Run Shortcut → 选择 "Health Export"

### 2.3 简化方案 (推荐先用这个)

上面的纯 Shortcuts 方案比较复杂（特别是 Sleep 分期的解析）。如果配置困难，可以用 **Health Auto Export** app：

1. App Store 下载 Health Auto Export (Pro 版支持自动化)
2. 配置导出指标：Sleep Analysis, Resting HR, HRV, Steps, Active Energy, SpO2
3. 导出格式：JSON
4. 导出目标：REST API → `http://<Mac IP>:9876/health`
5. 频率：每日 08:00

该 app 会自动处理 HealthKit 数据格式转换，省去手动解析。

## Step 3: 验证

### 手动推送测试数据

```bash
curl -X POST http://localhost:9876/health \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-07",
    "sleep": {
      "total_minutes": 420,
      "deep_minutes": 85,
      "rem_minutes": 110,
      "light_minutes": 195,
      "awake_minutes": 30,
      "bedtime": "23:15",
      "wakeup": "06:15"
    },
    "heart": {
      "resting_hr": 52,
      "hrv_avg": 45,
      "hrv_during_sleep": 52,
      "hr_min": 48,
      "hr_max": 155
    },
    "activity": {
      "steps": 8234,
      "active_energy_kcal": 520,
      "exercise_minutes": 35,
      "stand_hours": 10
    },
    "blood_oxygen": {
      "avg": 97,
      "min": 94
    }
  }'
```

### 运行 health_monitor

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/jobs/health_monitor.py --date 2026-04-07

# 检查生成的摘要
cat contexts/health/daily/2026-04-07.md
```

### 验证 Action Advisor 集成

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/jobs/action_advisor.py --dry-run
# 输出中应该能看到 "health" 在 Signals collected 列表里
```

## 数据格式参考

### 原始 JSON (contexts/health/data/YYYY-MM-DD.json)

```json
{
  "date": "2026-04-07",
  "sleep": {
    "total_minutes": 420,
    "deep_minutes": 85,
    "rem_minutes": 110,
    "light_minutes": 195,
    "awake_minutes": 30,
    "bedtime": "23:15",
    "wakeup": "06:15"
  },
  "heart": {
    "resting_hr": 52,
    "hrv_avg": 45,
    "hrv_during_sleep": 52,
    "hr_min": 48,
    "hr_max": 155
  },
  "activity": {
    "steps": 8234,
    "active_energy_kcal": 520,
    "exercise_minutes": 35,
    "stand_hours": 10
  },
  "blood_oxygen": {
    "avg": 97,
    "min": 94
  }
}
```

## 时间线总览

| 时间 | 组件 | 动作 |
|------|------|------|
| 08:00 | iPhone Shortcuts | 查询昨日 HealthKit 数据 → POST JSON 到 Mac |
| 08:01 | health_monitor.py | 读取 JSON → 生成每日摘要 → 检测异常 → 更新基线 |
| 09:15 | action_advisor.py | 读取健康摘要 → 融合进今日行动建议 → 发邮件 |
| 周日 08:01 | health_monitor.py | 额外生成周报（7 天趋势分析） |

## 故障排查

```bash
# 检查 receiver 是否在运行
curl http://localhost:9876/ping

# 查看 receiver 日志
tail -f .local_runtime/logs/services/health_receiver.log

# 查看 monitor 日志
tail -f .local_runtime/logs/jobs/health_monitor.log

# 手动重启 receiver
launchctl stop com.zhouxuanting.opencode.health-receiver
launchctl start com.zhouxuanting.opencode.health-receiver

# 重建基线
python3 periodic_jobs/ai_heartbeat/src/v0/jobs/health_monitor.py --rebuild-baseline
```
