#!/usr/bin/env python3
"""
Action Advisor — 从信息到行动的缺失齿轮。

Two-phase architecture:
  Phase 1 (deterministic): 读取今日所有自动采集的信号（builders digest, AI 日报,
           GitHub trending, OBSERVATIONS.md），拼成结构化上下文。
  Phase 2 (agentic): Agent 做三重过滤（相关性 → 可行动性 → 公理校验），
           生成 2-3 个具体 TODO，通过 Email 发送 + 本地存档。

调度时间：每日 9:15 AM（在 observer 之后，确保所有上游数据就绪）

Usage:
  python action_advisor.py              # 正常运行
  python action_advisor.py --dry-run    # 只生成不发邮件
"""

import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys
import glob

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)

from life_record_common import read_latest_work_summary

DEFAULT_MODEL = os.getenv(
    "OPENCODE_NEWS_MODEL",
    os.getenv("OPENCODE_DEFAULT_MODEL", "openai/gpt-5.4"),
)

WORKSPACE = Path(__file__).resolve().parents[5]  # up to workspace root


# ── Phase 1: Deterministic data collection ─────────────────────────────────

def read_latest_file(directory: Path, prefix: str, days_back: int = 2) -> str:
    """Find and read the most recent file matching prefix in directory."""
    if not directory.exists():
        return ""

    # Try today first, then yesterday
    for delta in range(days_back):
        date_str = (datetime.now() - timedelta(days=delta)).strftime("%Y%m%d")
        pattern = str(directory / f"{prefix}*{date_str}*")
        matches = glob.glob(pattern)
        if matches:
            latest = max(matches, key=os.path.getmtime)
            try:
                content = Path(latest).read_text(encoding="utf-8")
                # Truncate if too long
                if len(content) > 8000:
                    content = content[:8000] + "\n\n... [truncated, full file: " + latest + "]"
                return f"**来源**: `{Path(latest).name}`\n\n{content}"
            except Exception as e:
                return f"(读取失败: {e})"

    return ""


def read_observations_tail(n_lines: int = 30) -> str:
    """Read the last N lines of OBSERVATIONS.md."""
    obs_path = WORKSPACE / "contexts" / "memory" / "OBSERVATIONS.md"
    if not obs_path.exists():
        return ""

    try:
        lines = obs_path.read_text(encoding="utf-8").splitlines()
        tail = lines[-n_lines:] if len(lines) > n_lines else lines
        return "\n".join(tail)
    except Exception as e:
        return f"(读取失败: {e})"


def read_latest_github_trending() -> str:
    """Read the most recent GitHub trending report (weekly, so check last 7 days)."""
    directory = WORKSPACE / "contexts" / "survey_sessions" / "github_trending"
    if not directory.exists():
        return ""

    for delta in range(7):
        date_str = (datetime.now() - timedelta(days=delta)).strftime("%Y%m%d")
        pattern = str(directory / f"github_trending*{date_str}*")
        matches = glob.glob(pattern)
        if matches:
            latest = max(matches, key=os.path.getmtime)
            try:
                content = Path(latest).read_text(encoding="utf-8")
                if len(content) > 5000:
                    content = content[:5000] + "\n\n... [truncated]"
                return f"**来源**: `{Path(latest).name}`\n\n{content}"
            except Exception:
                pass

    return ""


def read_latest_health_summary(days_back: int = 2) -> str:
    """Read the most recent health daily summary."""
    health_dir = WORKSPACE / "contexts" / "health" / "daily"
    if not health_dir.exists():
        return ""

    for delta in range(days_back):
        date_str = (datetime.now() - timedelta(days=delta)).strftime("%Y-%m-%d")
        path = health_dir / f"{date_str}.md"
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                return f"**来源**: `{path.name}`\n\n{content}"
            except Exception:
                pass
    return ""


def collect_signals() -> dict:
    """Collect all available signals for today."""
    surveys = WORKSPACE / "contexts" / "survey_sessions"
    life_record_root = WORKSPACE / "contexts" / "life_record" / "data"

    signals = {
        "builders_digest": read_latest_file(
            surveys / "ai_builders_digest", "ai_builders_digest"
        ),
        "ai_newsletter": read_latest_file(
            surveys / "daily_ai_newsletter", "daily_ai_newsletter"
        ),
        "github_trending": read_latest_github_trending(),
        "observations": read_observations_tail(30),
        "life_record": read_latest_work_summary(
            life_record_root, reference_date=datetime.now().strftime("%Y%m%d"), days_back=3
        ),
        "health": read_latest_health_summary(),
    }

    available = {k: v for k, v in signals.items() if v}
    empty = [k for k, v in signals.items() if not v]

    print(f"Signals collected: {list(available.keys())}")
    if empty:
        print(f"Signals empty (normal if not yet generated today): {empty}")

    return signals


def format_signals_for_agent(signals: dict) -> str:
    """Format collected signals into structured text for the Agent prompt."""
    sections = []

    if signals.get("builders_digest"):
        sections.append(f"## 信号 1: AI Builders Digest (今日)\n\n{signals['builders_digest']}")

    if signals.get("ai_newsletter"):
        sections.append(f"## 信号 2: AI 行业日报 (今日)\n\n{signals['ai_newsletter']}")

    if signals.get("github_trending"):
        sections.append(f"## 信号 3: GitHub Trending (本周)\n\n{signals['github_trending']}")

    if signals.get("observations"):
        sections.append(f"## 信号 4: 最近的记忆观察\n\n{signals['observations']}")

    if signals.get("life_record"):
        sections.append(f"## 信号 5: 工作录音摘要\n\n{signals['life_record']}")

    if signals.get("health"):
        sections.append(f"## 信号 6: 健康数据\n\n{signals['health']}")

    if not sections:
        return ""

    return "\n\n---\n\n".join(sections)


# ── Phase 2: Agent analysis ────────────────────────────────────────────────

def run_action_advisor(dry_run: bool = False, model_id: str = DEFAULT_MODEL):
    # Phase 1
    print("Phase 1: Collecting today's signals...")
    signals = collect_signals()
    formatted = format_signals_for_agent(signals)

    if not formatted:
        print("No signals available today. Skipping Action Advisor.")
        return

    signal_chars = len(formatted)
    print(f"Phase 1 complete. {signal_chars} chars of signal data.\n")

    # Phase 2
    client = OpenCodeClient()
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_file = datetime.now().strftime("%Y%m%d")

    report_path = f"contexts/survey_sessions/action_advisor/action_advisor_{date_file}.md"
    archive_dir = WORKSPACE / "contexts" / "survey_sessions" / "action_advisor"
    archive_dir.mkdir(parents=True, exist_ok=True)

    session_title = f"Action Advisor {date_str}"
    session_id = client.create_session(session_title)

    if not session_id:
        print("Failed to create OpenCode session.")
        return

    delivery = ""
    if not dry_run:
        delivery = f"""
### 第四步：发送 Email

使用以下命令发送邮件：
```bash
python3 tools/send_email_to_myself.py "[Action Advisor] {date_str}" "" --file {report_path}
```
"""

    prompt = f"""你是炫汀的 Action Advisor。你的唯一职责是把今天的信息信号转化为具体可执行的动作。

## 今日信号

以下是自动采集系统今天收集到的全部信号：

{formatted}

## 你的任务

### 第一步：读取项目上下文

1. 读取 `AGENTS.md` — 了解 workspace 整体定位
2. 读取 `rules/axioms/INDEX.md` — 浏览公理索引，选 2-3 条最相关的公理

### 第二步：三重过滤

对上面的信号做三层过滤：

**过滤 1 — 相关性**：这条信号跟炫汀的 AI Memory Infrastructure 项目有关吗？具体包括：
- Context engineering / 记忆系统
- Agent 自动化 / 调度 / 编排
- 开发者工具 / AI-native workflow
- 信息架构 / 知识管理
- 当前 workspace 正在活跃开发的模块（从信号 4 的 OBSERVATIONS 判断）

**过滤 2 — 可行动性**：炫汀今天能对这条信号做什么？
- [30min] 可以在 30 分钟内完成的具体动作（试用、配置、对比、阅读）
- [2h] 可以在 2 小时内完成的小型改进（新 skill、新脚本、新公理候选）
- [标记] 需要标记为"下周做"的中型动作

**过滤 3 — 公理校验**：这个动作符合决策原则吗？
- A09（构建者思维）→ 推荐的是"构建"而非"消费"？
- M01（闭环校准）→ 推荐的动作有可验证的结果？
- T05（认知是资产）→ 做完后能沉淀为可复用知识？

### 第三步：写入报告

将结果写入 `{report_path}`，严格按以下模板：

```markdown
# [Action Advisor] {date_str}

## 今日信号

1. [来源名] 一句话描述发现了什么
2. ...
（只列通过相关性过滤的信号，最多 5 条）

## 建议动作

- [ ] [30min] 具体动作描述
  - 为什么：连接到你的什么项目/目标
  - 怎么验证：做完后怎么知道有效
  - 相关公理：Axx 公理名

- [ ] [2h] 具体动作描述
  - 为什么：...
  - 怎么验证：...
  - 相关公理：...

- [ ] [标记] 下周值得做的一件事
  - 为什么：...

## 今日不值得做

- 排除内容 1：原因
- 排除内容 2：原因
（显式列出被过滤的信号及理由，节省筛选时间）

## 反思锚点

今晚写 daily record 时，回顾：
"[一个具体的反思问题，基于今天推荐的动作]"
```

**硬性约束**：
- 最多 3 条建议动作，多了就过滤
- 每条必须有具体的文件路径、命令、或 repo URL，不能只说"关注 X 领域"
- "为什么"必须连接到 workspace 内的具体模块或文件
- "怎么验证"必须是可观察的结果（文件产出、配置变更、测试通过）
- 如果今天没有任何值得做的事，就写："今天的信号都与你的当前方向无关。安心做手头的事。"
- 全文不超过 50 行 Markdown
{delivery}

请开始执行。
"""

    print(f"Phase 2: Triggering Agent analysis (Session: {session_id})...")
    print(f"Using model: {model_id}")

    result = client.send_message(session_id, prompt, model_id=model_id)

    if not result:
        print("No immediate response. Sending continuation ping...")
        result = client.send_message(session_id, "继续", model_id=model_id)

    if result:
        client.wait_for_session_complete(session_id)
        print("Action Advisor complete.")
    else:
        print("Failed to start Action Advisor session.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Action Advisor")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Generate report only, skip email delivery"
    )
    parser.add_argument(
        "--model", "-M", default=DEFAULT_MODEL,
        help=f"Model ID (default: {DEFAULT_MODEL})"
    )
    args = parser.parse_args()

    print(f"Starting Action Advisor (dry_run={args.dry_run})...")
    run_action_advisor(dry_run=args.dry_run, model_id=args.model)
    print("Done.")
