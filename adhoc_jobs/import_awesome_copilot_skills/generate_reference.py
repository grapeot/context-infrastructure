#!/usr/bin/env python3
"""Generate rules/skills/reference_awesome_copilot_skills.md from upstream README."""

import argparse
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = "github/awesome-copilot"
README_URL = f"https://raw.githubusercontent.com/{REPO}/main/docs/README.skills.md"
OUT = Path(__file__).resolve().parents[2] / "rules" / "skills" / "reference_awesome_copilot_skills.md"
DATE = "2026-06-27"

ROW_RE = re.compile(
    r"^\| \[([^\]]+)\]\(\.\./skills/([^/]+)/SKILL\.md\)(?:<br\s*/>)?\s*"
    r"`gh skills install github/awesome-copilot ([^`]+)` "
    r"\| ([^|]+) \| ([^|]+) \|$"
)


def fetch_readme() -> str:
    req = urllib.request.Request(README_URL, headers={"User-Agent": "context-infrastructure-import"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_rows(text: str) -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        title, slug_dir, slug_cmd, desc, assets = m.groups()
        slug = slug_cmd.strip()
        skills.append(
            {
                "title": title.strip(),
                "slug": slug,
                "description": clean_cell(desc),
                "assets": clean_assets(assets),
            }
        )
    return skills


def clean_cell(text: str) -> str:
    text = re.sub(r"<br\s*/>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_assets(text: str) -> str:
    text = re.sub(r"<br\s*/>", ", ", text)
    return re.sub(r"\s+", " ", text).strip(" ,")


def first_letter(slug: str) -> str:
    c = slug[0].upper() if slug else "#"
    return c if c.isalpha() else "#"


def render(skills: list[dict[str, str]]) -> str:
    by_letter: dict[str, list[dict[str, str]]] = defaultdict(list)
    for s in skills:
        by_letter[first_letter(s["slug"])].append(s)

    lines: list[str] = [
        "# Awesome Copilot Skills 查阅与安装",
        "",
        "## 元数据",
        "",
        "- **类型**: Reference",
        f"- **适用场景**: 从 [{REPO}/skills](https://github.com/{REPO}/tree/main/skills) 发现、安装 {len(skills)} 个社区 Agent Skills",
        f"- **上游来源**: [{REPO}](https://github.com/{REPO})（MIT）",
        f"- **生成日期**: {DATE}（`adhoc_jobs/import_awesome_copilot_skills/generate_reference.py`）",
        "- **user-invocable**: true",
        "",
        "---",
        "",
        "## 何时触发",
        "",
        "本地 `INDEX.md` 无覆盖；需要 bundled scripts/assets；Azure/AWS/ADR/spec/agent 安全等 Copilot 生态能力。",
        "",
        "## 发现与安装",
        "",
        "- 浏览：[awesome-copilot.github.com/skills](https://awesome-copilot.github.com/skills)",
        "- 索引源：[docs/README.skills.md](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)",
        "",
        "```bash",
        "gh skills install github/awesome-copilot <skill-name>",
        "# 或",
        "cp -r /tmp/awesome-copilot/skills/<name> ~/.cursor/skills/<name>",
        "```",
        "",
        "**不要** bulk import 进 `rules/skills/`；按需 vendor + 本地 overlay 私有配置。",
        "",
        "上游更新后重新生成本文件：",
        "",
        "```bash",
        "python adhoc_jobs/import_awesome_copilot_skills/generate_reference.py",
        "```",
        "",
        "---",
        "",
        f"## Skill 目录（{len(skills)}）",
        "",
    ]

    for letter in sorted(by_letter.keys()):
        lines.append(f"### {letter}")
        lines.append("")
        for s in sorted(by_letter[letter], key=lambda x: x["slug"].lower()):
            assets = s["assets"]
            asset_note = ""
            if assets and assets.lower() != "none":
                asset_note = f"\n  - **资产**: {assets}"
            lines.append(
                f"- **`{s['slug']}`** — {s['description']}{asset_note}\n"
                f"  - 安装：`gh skills install github/awesome-copilot {s['slug']}`\n"
                f"  - 上游：[skills/{s['slug']}/SKILL.md](https://github.com/{REPO}/tree/main/skills/{s['slug']}/SKILL.md)"
            )
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 参考",
            "",
            f"- https://github.com/{REPO}/tree/main/skills",
            "- 本 workspace 工具型 repo：[`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=Path, help="Local README.skills.md path")
    args = parser.parse_args()
    if args.local:
        text = args.local.read_text(encoding="utf-8")
    else:
        text = fetch_readme()
    skills = parse_rows(text)
    if not skills:
        raise SystemExit("No skills parsed from README.skills.md")
    OUT.write_text(render(skills), encoding="utf-8")
    print(f"Wrote {len(skills)} skills to {OUT}")


if __name__ == "__main__":
    main()
