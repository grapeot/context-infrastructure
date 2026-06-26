#!/usr/bin/env python3
"""Import awesome-cursor-skills resources into rules/skills/."""

import argparse
import json
import re
import urllib.request
from pathlib import Path
from typing import Optional

REPO = "spencerpauly/awesome-cursor-skills"
BASE = f"https://raw.githubusercontent.com/{REPO}/main/resources"
API = f"https://api.github.com/repos/{REPO}/contents/resources?ref=main"
SKILLS_DIR = Path(__file__).resolve().parents[2] / "rules" / "skills"
DATE = "2026-06-26"

CATEGORIES: dict[str, list[str]] = {
    "Cursor-Native": [
        "suggesting-cursor-rules",
        "suggesting-cursor-hooks",
        "switching-projects",
        "saving-workspace-context",
        "visual-qa-testing",
        "verifying-in-browser",
        "profiling-performance",
        "screenshotting-changelog",
        "best-of-n-solving",
        "parallel-exploring",
        "grinding-until-pass",
        "finding-dev-server-url",
        "monitoring-terminal-errors",
        "detecting-port-conflicts",
        "tailing-build-output",
        "responsive-testing",
        "dark-mode-testing",
        "accessibility-auditing",
        "form-testing",
        "parallel-test-fixing",
        "codebase-onboarding",
        "comparing-branches-visually",
        "auto-type-checking",
        "suggesting-skills",
        "parallel-ci-triage",
        "parallel-code-review",
        "network-request-auditing",
        "recording-browser-flow-as-test",
        "building-skills-from-patterns",
    ],
    "Analytics & Tracking": ["adding-analytics", "adding-feature-flags"],
    "Error Tracking": ["adding-error-tracking"],
    "Auth & Payments": ["adding-auth", "adding-stripe"],
    "Testing": [
        "adding-e2e-tests",
        "writing-tests",
        "python-tdd-with-uv",
        "api-smoke-testing",
    ],
    "Workflow": [
        "babysitting-pr",
        "creating-pr",
        "writing-commit-messages",
        "incident-response",
        "systematic-debugging",
    ],
    "Infrastructure & DevOps": [
        "adding-docker",
        "setting-up-ci",
        "setting-up-terraform",
        "kubernetes-deploying",
    ],
    "Code Quality & Security": [
        "reviewing-code",
        "auditing-security",
        "auditing-performance",
        "verifying-markdown-formatting",
        "fixing-broken-links",
    ],
    "Dependencies": ["updating-npm-package"],
    "Frontend & UI": [
        "using-ui-stack",
        "converting-css-to-tailwind",
        "converting-css-modules-to-tailwind",
        "react-native-patterns",
    ],
    "Planning & Architecture": [
        "architecture-decision-records",
        "database-design",
    ],
    "Documentation": ["adding-api-docs"],
    "Utilities": [
        "exporting-to-png",
        "generating-images",
        "prompt-engineering",
        "seo-auditing",
        "writing-copy",
    ],
}

SLUG_TO_CATEGORY: dict[str, str] = {}
for cat, slugs in CATEGORIES.items():
    for slug in slugs:
        SLUG_TO_CATEGORY[slug] = cat


def kebab_to_snake(name: str) -> str:
    return name.replace("-", "_")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return meta, parts[2].lstrip("\n")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "context-infrastructure-import"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def convert(slug: str, raw: str) -> str:
    meta, body = parse_frontmatter(raw)
    name = meta.get("name", slug)
    description = meta.get("description", "")
    invocable = meta.get("user-invocable", "")
    category = SLUG_TO_CATEGORY.get(slug, "Utilities")
    upstream = f"https://github.com/{REPO}/tree/main/resources/{slug}"

    header = f"""## 元数据

- **类型**: Workflow
- **分类**: {category}
- **适用场景**: {description}
- **上游来源**: [{slug}]({upstream})
- **user-invocable**: {invocable if invocable else "—"}
- **导入日期**: {DATE}

---

"""
    # Replace first H1 if body starts with # Title matching name pattern
    return header + body


def list_slugs_local(resources_dir: Path) -> list[str]:
    return sorted(
        p.name for p in resources_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    )


def list_slugs_remote() -> list[str]:
    with urllib.request.urlopen(
        urllib.request.Request(API, headers={"User-Agent": "context-infrastructure-import"}),
        timeout=30,
    ) as resp:
        data = json.load(resp)
    return sorted(x["name"] for x in data if x["type"] == "dir")


def read_skill(slug: str, resources_dir: Optional[Path]) -> str:
    if resources_dir is not None:
        return (resources_dir / slug / "SKILL.md").read_text(encoding="utf-8")
    return fetch(f"{BASE}/{slug}/SKILL.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import awesome-cursor-skills into rules/skills/")
    parser.add_argument(
        "--local",
        type=Path,
        help="Local clone path (e.g. /tmp/awesome-cursor-skills); reads resources/ from disk",
    )
    args = parser.parse_args()

    resources_dir = None
    if args.local:
        resources_dir = args.local / "resources"
        if not resources_dir.is_dir():
            raise SystemExit(f"Not found: {resources_dir}")
        slugs = list_slugs_local(resources_dir)
    else:
        slugs = list_slugs_remote()
    expected = {s for slugs_list in CATEGORIES.values() for s in slugs_list}
    missing = expected - set(slugs)
    extra = set(slugs) - expected
    if missing:
        print("WARN missing from upstream:", missing)
    if extra:
        print("WARN new upstream dirs not in CATEGORIES:", extra)

    index_lines: list[str] = []
    index_lines.append("### Cursor Skills（awesome-cursor-skills）")
    index_lines.append("")
    index_lines.append(
        "来自 [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources)，"
        "kebab-case 目录名 → snake_case 文件名。上游更新时可重新运行 `adhoc_jobs/import_awesome_cursor_skills/import_skills.py`。"
    )
    index_lines.append("")

    for cat, cat_slugs in CATEGORIES.items():
        index_lines.append(f"#### {cat}")
        index_lines.append("")
        for slug in cat_slugs:
            if slug not in slugs:
                continue
            fname = kebab_to_snake(slug) + ".md"
            try:
                raw = read_skill(slug, resources_dir)
            except Exception as e:
                print(f"FAIL {slug}: {e}")
                continue
            out = SKILLS_DIR / fname
            content = convert(slug, raw)
            out.write_text(content, encoding="utf-8")
            meta, _ = parse_frontmatter(raw)
            desc = meta.get("description", slug)
            # Extract title from body first H1
            title_match = re.search(r"^# (.+)$", content.split("---", 1)[-1], re.MULTILINE)
            title = title_match.group(1) if title_match else slug
            index_lines.append(f"- [{title}](./{fname}) — {desc}")
            print(f"OK {fname}")
        index_lines.append("")

    index_path = SKILLS_DIR / "INDEX.md"
    text = index_path.read_text(encoding="utf-8")
    marker = "### BestPractice（最佳实践）"
    block = "\n".join(index_lines).rstrip() + "\n\n"
    if "### Cursor Skills（awesome-cursor-skills）" in text:
        # Replace existing block
        start = text.index("### Cursor Skills（awesome-cursor-skills）")
        end = text.index(marker)
        text = text[:start] + block + text[end:]
    else:
        text = text.replace(marker, block + marker)
    index_path.write_text(text, encoding="utf-8")
    print("Updated INDEX.md")


if __name__ == "__main__":
    main()
