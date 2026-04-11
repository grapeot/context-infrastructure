#!/usr/bin/env python3
"""
Apple Watch 语音备忘录 → whisper-cpp 本地转写 → Markdown 文件

监听 iCloud 同步的语音备忘录目录，检测到新 .m4a 文件后调用 whisper-cli 转写，
转写结果保存到 contexts/voice_notes/ 目录。
"""

import os
import sys
import time
import json
import logging
import hashlib
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("缺少 watchdog: pip3 install watchdog")
    sys.exit(1)

# ---------- 配置 ----------

DEFAULT_WATCH_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/VoiceDropbox"
)

DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "contexts", "voice_notes")

DEFAULT_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "contexts", "voice_notes", ".processed.json")

DEFAULT_WHISPER_CLI = "/opt/homebrew/Cellar/whisper-cpp/1.8.4/bin/whisper-cli"

DEFAULT_MODEL = os.path.expanduser("~/.local/share/whisper-cpp/models/ggml-large-v3-turbo.bin")

# ---------- 日志 ----------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("voice_watcher")

# ---------- 核心逻辑 ----------


class ProcessedTracker:
    """跟踪已处理的文件，避免重复转写。"""

    def __init__(self, state_file: str):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.processed: dict[str, str] = {}
        self._load()

    def _load(self):
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.processed = json.load(f)

    def _save(self):
        with open(self.state_file, "w") as f:
            json.dump(self.processed, f, indent=2, ensure_ascii=False)

    def is_processed(self, filepath: str) -> bool:
        return self._hash(filepath) in self.processed

    def mark_processed(self, filepath: str, output_path: str):
        self.processed[self._hash(filepath)] = {
            "source": filepath,
            "output": output_path,
            "time": datetime.now().isoformat(),
        }
        self._save()

    @staticmethod
    def _hash(filepath: str) -> str:
        stat = os.stat(filepath)
        key = f"{filepath}:{stat.st_size}:{stat.st_mtime}"
        return hashlib.md5(key.encode()).hexdigest()


def transcribe_with_whisper_cpp(audio_path: str, whisper_cli: str, model_path: str) -> dict:
    """调用 whisper-cli 转写音频，返回 JSON 结果。"""
    log.info("开始转写: %s", os.path.basename(audio_path))

    with tempfile.TemporaryDirectory() as tmpdir:
        # whisper-cli 只支持 wav/flac/ogg/mp3，需要先将 m4a 转为 wav
        wav_path = os.path.join(tmpdir, "input.wav")
        ffmpeg_cmd = [
            "/opt/homebrew/bin/ffmpeg", "-i", audio_path,
            "-ar", "16000", "-ac", "1", "-y", wav_path,
        ]
        ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)
        if ffmpeg_result.returncode != 0:
            log.error("ffmpeg 转换失败: %s", ffmpeg_result.stderr)
            raise RuntimeError("ffmpeg 转换失败")
        log.info("已转换为 wav: %s", wav_path)

        output_base = os.path.join(tmpdir, "result")

        cmd = [
            whisper_cli,
            "--model", model_path,
            "--language", "zh",
            "--output-json",
            "--output-file", output_base,
            "--flash-attn",
            "--no-prints",
            "--file", wav_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode != 0:
            log.error("whisper-cli 失败:\nstdout: %s\nstderr: %s", result.stdout, result.stderr)
            raise RuntimeError(f"whisper-cli 退出码: {result.returncode}")

        json_path = output_base + ".json"
        if not os.path.exists(json_path):
            raise RuntimeError(f"未找到输出文件: {json_path}")

        with open(json_path) as f:
            data = json.load(f)

    # 提取文本和分段
    full_text = ""
    segments = []
    for seg in data.get("transcription", []):
        text = seg.get("text", "").strip()
        full_text += text
        timestamps = seg.get("timestamps", {})
        segments.append({
            "start": _ts_to_seconds(timestamps.get("from", "00:00:00,000")),
            "end": _ts_to_seconds(timestamps.get("to", "00:00:00,000")),
            "text": text,
        })

    log.info("转写完成，文本长度: %d 字", len(full_text))
    return {"text": full_text, "segments": segments}


def _ts_to_seconds(ts: str) -> float:
    """将 'HH:MM:SS,mmm' 格式转为秒数。"""
    try:
        parts = ts.replace(",", ".").split(":")
        h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s
    except (ValueError, IndexError):
        return 0.0


def save_transcript(result: dict, audio_path: str, output_dir: str) -> str:
    """将转写结果保存为 Markdown 文件。"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_name = Path(audio_path).stem
    now = datetime.now()
    filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{audio_name}.md"
    output_path = output_dir / filename

    duration = 0
    if result["segments"]:
        duration = result["segments"][-1]["end"]

    lines = [
        f"# 语音转写 — {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**源文件**: `{os.path.basename(audio_path)}`  ",
        f"**转写时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**时长**: {duration:.0f} 秒",
        "",
        "---",
        "",
        "## 原文",
        "",
        result["text"].strip(),
        "",
    ]

    if result["segments"]:
        lines.extend([
            "---",
            "",
            "## 分段（带时间戳）",
            "",
        ])
        for seg in result["segments"]:
            start = _format_time(seg["start"])
            end = _format_time(seg["end"])
            lines.append(f"`[{start} → {end}]` {seg['text'].strip()}")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("已保存: %s", output_path)
    return str(output_path)


def _format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def process_file(audio_path: str, whisper_cli: str, model_path: str,
                 tracker: ProcessedTracker, output_dir: str):
    """处理单个音频文件。"""
    if tracker.is_processed(audio_path):
        log.debug("跳过已处理: %s", audio_path)
        return

    # 等待文件写入完成（iCloud 同步可能还在进行）
    prev_size = -1
    for _ in range(30):
        try:
            curr_size = os.path.getsize(audio_path)
        except OSError:
            return
        if curr_size == prev_size and curr_size > 0:
            break
        prev_size = curr_size
        time.sleep(1)

    # iCloud 文件锁释放需要几秒，最多重试 5 次
    for attempt in range(5):
        try:
            result = transcribe_with_whisper_cpp(audio_path, whisper_cli, model_path)
            output_path = save_transcript(result, audio_path, output_dir)
            tracker.mark_processed(audio_path, output_path)
            return
        except Exception as e:
            if attempt < 4:
                log.warning("转写失败（第%d次），10秒后重试: %s", attempt + 1, e)
                time.sleep(10)
            else:
                log.exception("转写失败，已放弃: %s", audio_path)


class NewFileHandler(FileSystemEventHandler):
    """监听新增/修改的音频文件。"""

    AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".ogg", ".flac"}

    def __init__(self, whisper_cli: str, model_path: str,
                 tracker: ProcessedTracker, output_dir: str):
        self.whisper_cli = whisper_cli
        self.model_path = model_path
        self.tracker = tracker
        self.output_dir = output_dir

    def on_created(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).suffix.lower() in self.AUDIO_EXTENSIONS:
            log.info("检测到新文件: %s", event.src_path)
            process_file(event.src_path, self.whisper_cli, self.model_path,
                         self.tracker, self.output_dir)

    def on_modified(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).suffix.lower() in self.AUDIO_EXTENSIONS:
            process_file(event.src_path, self.whisper_cli, self.model_path,
                         self.tracker, self.output_dir)


def scan_existing(watch_dir: str, whisper_cli: str, model_path: str,
                  tracker: ProcessedTracker, output_dir: str):
    """启动时扫描已有但未处理的文件。"""
    watch_path = Path(watch_dir)
    if not watch_path.exists():
        return
    for ext in NewFileHandler.AUDIO_EXTENSIONS:
        for f in watch_path.glob(f"*{ext}"):
            process_file(str(f), whisper_cli, model_path, tracker, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Apple Watch 语音备忘录自动转写 (whisper-cpp)")
    parser.add_argument("--watch-dir", default=DEFAULT_WATCH_DIR, help="监听目录")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="转写输出目录")
    parser.add_argument("--state-file", default=DEFAULT_STATE_FILE, help="已处理记录文件")
    parser.add_argument("--whisper-cli", default=DEFAULT_WHISPER_CLI, help="whisper-cli 路径")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Whisper 模型文件路径")
    parser.add_argument("--scan", action="store_true", default=True, help="启动时扫描已有文件")
    args = parser.parse_args()

    # 检查 whisper-cli 和模型是否存在
    if not os.path.exists(args.whisper_cli):
        log.error("whisper-cli 不存在: %s\n安装: brew install whisper-cpp", args.whisper_cli)
        sys.exit(1)
    if not os.path.exists(args.model):
        log.error("模型文件不存在: %s", args.model)
        sys.exit(1)

    # 确保监听目录存在
    watch_dir = Path(args.watch_dir)
    if not watch_dir.exists():
        log.warning("监听目录不存在，自动创建: %s", watch_dir)
        watch_dir.mkdir(parents=True, exist_ok=True)

    log.info("=== 语音备忘录转写服务启动 ===")
    log.info("监听目录: %s", args.watch_dir)
    log.info("输出目录: %s", args.output_dir)
    log.info("whisper-cli: %s", args.whisper_cli)
    log.info("模型: %s", args.model)

    tracker = ProcessedTracker(args.state_file)

    if args.scan:
        scan_existing(args.watch_dir, args.whisper_cli, args.model, tracker, args.output_dir)

    handler = NewFileHandler(args.whisper_cli, args.model, tracker, args.output_dir)
    observer = Observer()
    observer.schedule(handler, args.watch_dir, recursive=False)
    observer.start()
    log.info("监听中... (Ctrl+C 停止)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("停止监听")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
