#!/usr/bin/env python3
"""
Health Monitor — Apple Watch 健康数据处理与每日摘要生成。

纯确定性处理，无需 LLM：
  1. 读取 contexts/health/data/YYYY-MM-DD.json（由 iPhone Shortcuts 推送）
  2. 与个人基线对比，检测异常
  3. 生成每日摘要 Markdown → contexts/health/daily/YYYY-MM-DD.md
  4. 每周日生成周报 → contexts/health/weekly/YYYY-Wxx.md

调度时间：每日 08:01（在 iPhone Shortcuts 08:00 推送之后）

Usage:
  python health_monitor.py                    # 处理今天的数据
  python health_monitor.py --date 2026-04-07  # 处理指定日期
  python health_monitor.py --rebuild-baseline # 重建基线
"""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[5]
HEALTH_ROOT = ROOT_DIR / "contexts" / "health"
DATA_DIR = HEALTH_ROOT / "data"
DAILY_DIR = HEALTH_ROOT / "daily"
WEEKLY_DIR = HEALTH_ROOT / "weekly"
BASELINE_PATH = HEALTH_ROOT / "baseline.json"

# 指标定义：(显示名, JSON路径, 单位, 方向, 告警阈值倍数)
# 方向: "lower_better" 表示低于基线是好事, "higher_better" 反之
METRIC_DEFS = {
    "resting_hr": {
        "name": "静息心率",
        "path": ("heart", "resting_hr"),
        "unit": "bpm",
        "direction": "lower_better",
        "warn_pct": 0.10,  # 偏离基线 10% 告警
    },
    "hrv_avg": {
        "name": "HRV",
        "path": ("heart", "hrv_avg"),
        "unit": "ms",
        "direction": "higher_better",
        "warn_pct": 0.15,
    },
    "sleep_total": {
        "name": "总睡眠",
        "path": ("sleep", "total_minutes"),
        "unit": "min",
        "direction": "higher_better",
        "warn_pct": 0.20,
    },
    "sleep_deep": {
        "name": "深睡",
        "path": ("sleep", "deep_minutes"),
        "unit": "min",
        "direction": "higher_better",
        "warn_pct": 0.25,
    },
    "sleep_rem": {
        "name": "REM",
        "path": ("sleep", "rem_minutes"),
        "unit": "min",
        "direction": "higher_better",
        "warn_pct": 0.25,
    },
    "steps": {
        "name": "步数",
        "path": ("activity", "steps"),
        "unit": "步",
        "direction": "higher_better",
        "warn_pct": 0.30,
    },
    "active_energy": {
        "name": "活动消耗",
        "path": ("activity", "active_energy_kcal"),
        "unit": "kcal",
        "direction": "higher_better",
        "warn_pct": 0.30,
    },
    "blood_oxygen_avg": {
        "name": "血氧均值",
        "path": ("blood_oxygen", "avg"),
        "unit": "%",
        "direction": "higher_better",
        "warn_pct": 0.03,  # 血氧波动很小，3% 就算异常
    },
}


def _get_nested(data: dict, path: tuple):
    """Safely traverse nested dict by key path."""
    current = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def load_day_data(date_str: str) -> dict | None:
    """Load raw JSON for a given date (YYYY-MM-DD format)."""
    path = DATA_DIR / f"{date_str}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {path}: {e}")
        return None


def load_baseline() -> dict:
    """Load personal baseline values."""
    if not BASELINE_PATH.exists():
        return {}
    try:
        return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_baseline(baseline: dict):
    """Save baseline to disk."""
    BASELINE_PATH.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def rebuild_baseline(days_back: int = 14) -> dict:
    """Build baseline from the last N days of data."""
    today = datetime.now().date()
    metric_values: dict[str, list] = {k: [] for k in METRIC_DEFS}

    for delta in range(days_back):
        date_str = (today - timedelta(days=delta)).isoformat()
        data = load_day_data(date_str)
        if not data:
            continue
        for key, mdef in METRIC_DEFS.items():
            val = _get_nested(data, mdef["path"])
            if val is not None and isinstance(val, (int, float)):
                metric_values[key].append(val)

    baseline = {"updated": today.isoformat(), "days_used": 0, "metrics": {}}
    for key, values in metric_values.items():
        if len(values) >= 3:  # 至少 3 天数据才建基线
            baseline["metrics"][key] = {
                "mean": round(statistics.mean(values), 1),
                "stdev": round(statistics.stdev(values), 1) if len(values) > 1 else 0,
            }
            baseline["days_used"] = max(baseline["days_used"], len(values))

    save_baseline(baseline)
    print(f"Baseline rebuilt from {baseline['days_used']} days of data.")
    return baseline


def analyze_day(data: dict, baseline: dict) -> dict:
    """Analyze a day's data against baseline. Returns structured analysis."""
    analysis = {"metrics": {}, "warnings": [], "highlights": []}

    for key, mdef in METRIC_DEFS.items():
        val = _get_nested(data, mdef["path"])
        if val is None:
            continue

        entry = {"value": val, "unit": mdef["unit"], "name": mdef["name"]}

        # Compare against baseline
        bl = baseline.get("metrics", {}).get(key)
        if bl and bl.get("mean"):
            mean = bl["mean"]
            diff_pct = (val - mean) / mean if mean != 0 else 0
            entry["baseline_mean"] = mean
            entry["diff_pct"] = round(diff_pct * 100, 1)

            # Determine status
            is_good_direction = (
                (mdef["direction"] == "lower_better" and diff_pct < 0)
                or (mdef["direction"] == "higher_better" and diff_pct > 0)
            )

            if abs(diff_pct) <= mdef["warn_pct"]:
                entry["status"] = "normal"
            elif is_good_direction:
                entry["status"] = "good"
                analysis["highlights"].append(
                    f"{mdef['name']} {val}{mdef['unit']}（较基线 {entry['diff_pct']:+.1f}%）"
                )
            else:
                entry["status"] = "warning"
                analysis["warnings"].append(
                    f"{mdef['name']} {val}{mdef['unit']}（较基线 {entry['diff_pct']:+.1f}%）"
                )
        else:
            entry["status"] = "no_baseline"

        analysis["metrics"][key] = entry

    return analysis


def _status_icon(status: str) -> str:
    if status == "good":
        return "+"
    if status == "warning":
        return "!"
    return " "


def format_sleep_time(minutes: int) -> str:
    """Format minutes as Xh Ym."""
    h, m = divmod(minutes, 60)
    return f"{h}h{m:02d}m"


def generate_daily_summary(date_str: str, data: dict, analysis: dict) -> str:
    """Generate daily health summary markdown."""
    lines = [f"# Health Summary {date_str}", ""]

    # Sleep section
    sleep = data.get("sleep", {})
    if sleep:
        total = sleep.get("total_minutes", 0)
        deep = sleep.get("deep_minutes", 0)
        rem = sleep.get("rem_minutes", 0)
        light = sleep.get("light_minutes", 0)
        awake = sleep.get("awake_minutes", 0)
        bedtime = sleep.get("bedtime", "?")
        wakeup = sleep.get("wakeup", "?")

        m = analysis["metrics"]
        deep_s = f" {_status_icon(m.get('sleep_deep', {}).get('status', ''))}" if "sleep_deep" in m else ""
        rem_s = f" {_status_icon(m.get('sleep_rem', {}).get('status', ''))}" if "sleep_rem" in m else ""

        lines.extend([
            "## Sleep",
            f"- Total: {format_sleep_time(total)} ({bedtime} - {wakeup})",
            f"- Deep: {deep}min{deep_s} | REM: {rem}min{rem_s} | Light: {light}min | Awake: {awake}min",
            "",
        ])

    # Heart section
    heart = data.get("heart", {})
    if heart:
        rhr = heart.get("resting_hr")
        hrv = heart.get("hrv_avg")
        hr_min = heart.get("hr_min")
        hr_max = heart.get("hr_max")

        m = analysis["metrics"]
        rhr_info = ""
        if rhr and "resting_hr" in m:
            e = m["resting_hr"]
            if "diff_pct" in e:
                rhr_info = f" (baseline {e['baseline_mean']}, {e['diff_pct']:+.1f}%)"

        hrv_info = ""
        if hrv and "hrv_avg" in m:
            e = m["hrv_avg"]
            if "diff_pct" in e:
                hrv_info = f" (baseline {e['baseline_mean']}, {e['diff_pct']:+.1f}%)"

        lines.extend([
            "## Heart",
            f"- Resting HR: {rhr} bpm{rhr_info}" if rhr else "",
            f"- HRV: {hrv} ms{hrv_info}" if hrv else "",
            f"- Range: {hr_min}-{hr_max} bpm" if hr_min and hr_max else "",
            "",
        ])
        lines = [ln for ln in lines if ln != ""]  # remove empty
        lines.append("")

    # Activity section
    activity = data.get("activity", {})
    if activity:
        steps = activity.get("steps", 0)
        energy = activity.get("active_energy_kcal", 0)
        exercise = activity.get("exercise_minutes", 0)
        stand = activity.get("stand_hours", 0)

        lines.extend([
            "## Activity",
            f"- Steps: {steps:,}",
            f"- Active energy: {energy} kcal | Exercise: {exercise} min | Stand: {stand} hours",
            "",
        ])

    # Blood oxygen
    spo2 = data.get("blood_oxygen", {})
    if spo2:
        avg = spo2.get("avg")
        low = spo2.get("min")
        if avg:
            lines.extend([
                "## Blood Oxygen",
                f"- Avg: {avg}% | Min: {low}%",
                "",
            ])

    # Warnings & highlights
    if analysis["warnings"]:
        lines.append("## Warnings")
        for w in analysis["warnings"]:
            lines.append(f"- {w}")
        lines.append("")

    if analysis["highlights"]:
        lines.append("## Highlights")
        for h in analysis["highlights"]:
            lines.append(f"- {h}")
        lines.append("")

    # Action hint (for action_advisor to pick up)
    if analysis["warnings"]:
        lines.append("## Suggested adjustments")
        for w in analysis["warnings"]:
            if "HRV" in w:
                lines.append("- HRV 偏低，建议今天避免高强度运动，优先恢复性活动")
            if "深睡" in w:
                lines.append("- 深睡不足，建议今晚减少屏幕时间、提前入睡")
            if "步数" in w:
                lines.append("- 活动量偏低，建议增加日间步行")
            if "静息心率" in w:
                lines.append("- 静息心率偏高，关注是否有过度疲劳或感冒前兆")
            if "血氧" in w:
                lines.append("- 血氧偏低，如持续请关注呼吸健康")
        lines.append("")

    return "\n".join(lines)


def generate_weekly_report(end_date: str) -> str | None:
    """Generate weekly report from last 7 days of daily summaries."""
    end = datetime.fromisoformat(end_date).date()
    week_data = []

    for delta in range(7):
        d = end - timedelta(days=delta)
        data = load_day_data(d.isoformat())
        if data:
            week_data.append((d.isoformat(), data))

    if len(week_data) < 3:
        print(f"Only {len(week_data)} days of data, skipping weekly report (need >= 3)")
        return None

    # Compute weekly averages
    metric_values: dict[str, list] = {k: [] for k in METRIC_DEFS}
    for _, data in week_data:
        for key, mdef in METRIC_DEFS.items():
            val = _get_nested(data, mdef["path"])
            if val is not None and isinstance(val, (int, float)):
                metric_values[key].append(val)

    iso_year, iso_week, _ = end.isocalendar()
    lines = [f"# Weekly Health Report {iso_year}-W{iso_week:02d}", ""]
    lines.append(f"Period: {week_data[-1][0]} to {week_data[0][0]} ({len(week_data)} days)")
    lines.append("")

    baseline = load_baseline()

    lines.append("## Weekly Averages")
    lines.append("")
    lines.append("| Metric | Weekly Avg | Baseline | Trend |")
    lines.append("|--------|-----------|----------|-------|")

    for key, mdef in METRIC_DEFS.items():
        values = metric_values[key]
        if not values:
            continue
        avg = round(statistics.mean(values), 1)
        bl = baseline.get("metrics", {}).get(key, {})
        bl_mean = bl.get("mean", "—")
        if isinstance(bl_mean, (int, float)) and bl_mean != 0:
            diff = round((avg - bl_mean) / bl_mean * 100, 1)
            trend = f"{diff:+.1f}%"
        else:
            trend = "—"
        lines.append(f"| {mdef['name']} | {avg} {mdef['unit']} | {bl_mean} | {trend} |")

    lines.append("")

    # Daily sparkline (simple text trend)
    lines.append("## Daily Trend")
    lines.append("")
    sorted_days = sorted(week_data, key=lambda x: x[0])
    for key in ["sleep_total", "resting_hr", "hrv_avg", "steps"]:
        mdef = METRIC_DEFS[key]
        daily_vals = []
        for date, data in sorted_days:
            val = _get_nested(data, mdef["path"])
            daily_vals.append(str(val) if val is not None else "—")
        lines.append(f"- {mdef['name']}: {' → '.join(daily_vals)} {mdef['unit']}")

    lines.append("")
    return "\n".join(lines)


def process_day(date_str: str, force: bool = False):
    """Main entry: process a single day's health data."""
    data = load_day_data(date_str)
    if not data:
        print(f"No data found for {date_str}")
        return False

    daily_path = DAILY_DIR / f"{date_str}.md"
    if daily_path.exists() and not force:
        print(f"Daily summary already exists: {daily_path}")
        return True

    baseline = load_baseline()
    if not baseline.get("metrics"):
        print("No baseline yet. Will generate summary without baseline comparison.")

    analysis = analyze_day(data, baseline)
    summary = generate_daily_summary(date_str, data, analysis)

    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(summary + "\n", encoding="utf-8")
    print(f"Daily summary written: {daily_path}")

    # Auto-rebuild baseline if we have enough data and it's stale
    bl_updated = baseline.get("updated", "")
    if bl_updated:
        days_since = (datetime.now().date() - datetime.fromisoformat(bl_updated).date()).days
        if days_since >= 7:
            print("Baseline is stale (>7 days), rebuilding...")
            rebuild_baseline()
    else:
        # Check if we have enough data to build initial baseline
        count = len(list(DATA_DIR.glob("*.json")))
        if count >= 7:
            print(f"Found {count} days of data, building initial baseline...")
            rebuild_baseline()

    # Generate weekly report on Sundays
    date_obj = datetime.fromisoformat(date_str).date()
    if date_obj.weekday() == 6:  # Sunday
        weekly = generate_weekly_report(date_str)
        if weekly:
            iso_year, iso_week, _ = date_obj.isocalendar()
            weekly_path = WEEKLY_DIR / f"{iso_year}-W{iso_week:02d}.md"
            WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
            weekly_path.write_text(weekly + "\n", encoding="utf-8")
            print(f"Weekly report written: {weekly_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Health Monitor — daily summary generator")
    parser.add_argument(
        "--date", default=datetime.now().date().isoformat(),
        help="Date to process (YYYY-MM-DD, default: today)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing daily summary",
    )
    parser.add_argument(
        "--rebuild-baseline", action="store_true",
        help="Rebuild personal baseline from last 14 days",
    )
    args = parser.parse_args()

    if args.rebuild_baseline:
        rebuild_baseline()
        return

    process_day(args.date, force=args.force)


if __name__ == "__main__":
    main()
