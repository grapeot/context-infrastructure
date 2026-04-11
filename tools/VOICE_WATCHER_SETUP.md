# 语音备忘录自动转写 — 安装指南

Apple Watch 录音 → iPhone 捷径自动导出到 iCloud Drive → Mac whisper-cpp 本地转写 → Markdown 文件

## 架构

```
Apple Watch (Action Button)
    ↓ 录音
语音备忘录 App
    ↓ iPhone 捷径自动化（App 关闭时触发）
iCloud Drive / VoiceDropbox /
    ↓ iCloud 同步到 Mac
~/Library/Mobile Documents/com~apple~CloudDocs/VoiceDropbox/
    ↓ watchdog 文件监听
voice_watcher.py (ffmpeg 转 wav → whisper-cpp 转写)
    ↓
contexts/voice_transcripts/*.md
```

## 1. iPhone 捷径配置（关键步骤）

macOS 上语音备忘录的音频文件被 CloudKit 托管，无法直接从文件系统访问。
需要用 iPhone 捷径自动将录音导出到 iCloud Drive 的指定文件夹。

### 第一步：创建 iCloud Drive 文件夹

在 iPhone 的「文件」App 中：
1. 打开「文件」→「iCloud Drive」
2. 创建文件夹 `VoiceDropbox`（如果 Mac 上已运行过脚本，这个文件夹已存在）

### 第二步：创建捷径

打开 iPhone「捷径」App → 点右上角 `+` 创建新捷径：

**动作 1：获取最新语音备忘录**
- 搜索添加「查找语音备忘录」
- 排序方式：「录制日期」，排序顺序：「最新在前」
- 限制：勾选「限制」，设为 `1`（只取最新一条）

**动作 2：获取文件名**
- 搜索添加「获取录音的详细信息」
- 获取：「名称」

**动作 3：保存到 iCloud Drive**
- 搜索添加「存储文件」
- 来源：选择动作 1 的输出（语音备忘录）
- 目标路径：`/Shortcuts/VoiceDropbox/`
- 询问存储位置：**关闭**（这样才能全自动）
- 覆盖相同名称：**打开**

给这个捷径命名为「保存语音备忘录」。

### 第三步：创建自动化

捷径 App → 底部「自动化」Tab → 右上角 `+`：

1. 选择「App」
2. App 选择「语音备忘录」
3. 触发条件选「关闭时」
4. 选择「立即运行」（不要选"运行前询问"）
5. 动作选「运行捷径」→ 选刚才创建的「保存语音备忘录」

配置完成后，每次关闭语音备忘录 App，最新录音会自动保存到 iCloud Drive。

> **注意**：捷径保存的文件路径是 `iCloud Drive/Shortcuts/VoiceDropbox/`，
> 对应 Mac 上的 `~/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/VoiceDropbox/`。
> 如果你在「存储文件」步骤里选择直接存到 `iCloud Drive/VoiceDropbox/`，
> 则对应 Mac 上的 `~/Library/Mobile Documents/com~apple~CloudDocs/VoiceDropbox/`。

## 2. Mac 端依赖

```bash
# whisper-cpp（如果还没装）
brew install whisper-cpp ffmpeg

# Python 依赖
pip3 install watchdog

# 下载模型（如果还没有）
# large-v3-turbo 推荐，中文效果好，速度也不慢
whisper-cli --model-path ~/.local/share/whisper-cpp/models/ --download ggml-large-v3-turbo
```

当前环境已确认可用：
- whisper-cpp 1.8.4（`/opt/homebrew/Cellar/whisper-cpp/1.8.4/bin/whisper-cli`）
- ggml-large-v3-turbo.bin（`~/.local/share/whisper-cpp/models/`，1.5G）
- ffmpeg 8.1（`/opt/homebrew/bin/ffmpeg`，用于 m4a → wav 转换）

## 3. 手动运行（测试）

```bash
cd /path/to/context-infrastructure

# 默认监听 iCloud Drive/VoiceDropbox 目录
python3 tools/voice_watcher.py

# 自定义监听目录
python3 tools/voice_watcher.py \
  --watch-dir ~/Library/Mobile\ Documents/com~apple~CloudDocs/VoiceDropbox
```

启动后脚本会：
1. 扫描目录中已有但未处理的音频文件
2. 持续监听新文件
3. 检测到新 .m4a 后：等待文件写入完成 → ffmpeg 转 wav → whisper-cpp 转写 → 保存 Markdown

## 4. 开机自启（launchd）

```bash
REPO_PATH=$(pwd)

# 生成 plist（替换占位符）
sed "s|__REPO_PATH__|$REPO_PATH|g" tools/com.voice-notes.watcher.plist \
  > ~/Library/LaunchAgents/com.voice-notes.watcher.plist

# 创建日志目录
mkdir -p logs

# 加载服务
launchctl load ~/Library/LaunchAgents/com.voice-notes.watcher.plist
```

管理命令：
```bash
# 查看状态
launchctl list | grep voice-notes

# 停止
launchctl unload ~/Library/LaunchAgents/com.voice-notes.watcher.plist

# 查看日志
tail -f logs/voice_watcher.log
```

## 5. 输出

转写结果保存在 `contexts/voice_transcripts/`：

```
contexts/voice_transcripts/
├── 20260406_222958_test_recording.md
├── 20260407_091530_meeting_notes.md
└── .processed.json   # 已处理文件记录，避免重复转写
```

每个 `.md` 文件包含：
- 元信息（源文件、转写时间、时长）
- 完整转写原文
- 带时间戳的分段文本

## 6. 性能参考

在 Apple M4 上实测：
- 20 分钟录音（20MB m4a）→ 约 72 秒完成转写
- 使用 Metal GPU 加速 + flash attention
