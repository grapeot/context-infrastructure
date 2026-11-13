#!/usr/bin/env python3
"""
L2 Reflector Agent (Trigger Script)

Two stages, so that no rule changes without a human saying yes:

1. propose (default, safe to run from cron at night):
   the agent reads OBSERVATIONS.md and writes rule *candidates* to contexts/memory/RULE_CANDIDATES.md,
   each with its target file, the exact change, the reason, and the source entries it came from.
   It does not touch rules/ or OBSERVATIONS.md. The script snapshots rules/ before and after and
   exits non-zero if anything under rules/ changed.
2. apply (run by hand after review, `--apply`):
   the human ticks `- [x] 批准` on the candidates they accept; the agent merges only those into rules/,
   moves them to the archive section of the candidates file, and garbage-collects OBSERVATIONS.md.
"""
import hashlib
import os
import sys
from datetime import datetime

from opencode_client import OpenCodeClient

KNOWLEDGE_BASE = "/path/to/your/workspace/periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KNOWLEDGE_BASE))))
RULES_DIR = os.path.join(ROOT_DIR, "rules")
CANDIDATES_PATH = os.path.join(ROOT_DIR, "contexts", "memory", "RULE_CANDIDATES.md")

PROPOSE_TEMPLATE = """
执行记忆系统的"反思"任务（提议阶段，只写候选，不改规则）。

SOP: {kb_path}
基准日期：{target_date}

步骤：
1. 读取 contexts/memory/OBSERVATIONS.md，分析 🔴 和高优 🟡 条目；需要核对时，到历史会话目录或用本地搜索找到当时的原始对话。
2. 找出值得晋升的规律，以及 rules/ 里互相矛盾、需要划清边界的规则。
3. 把每一条建议写成候选，追加到 contexts/memory/RULE_CANDIDATES.md 的「待批阅」部分（文件不存在就新建，先写一行标题「# 规则候选」，再写「## 待批阅」和「## 已处理」两个小节）。每条候选用下面的格式：

### {target_date} · <一句话标题>
- [ ] 批准
- 目标文件：rules/...（写完整相对路径）
- 改动：新增 / 修改 / 删除，附上改动后的原文；修改和删除同时附上原来的那几行
- 理由：为什么要改，适用和不适用的边界
- 来源：支撑这条建议的观测条目日期，或原始对话文件的完整相对路径（至少一条）

硬约束：
- 不要修改 rules/ 下的任何文件，也不要修改 OBSERVATIONS.md。这一阶段只允许写 RULE_CANDIDATES.md。
- 同一条建议已经在「待批阅」里的，不要重复写。
- 晋升门槛：跨项目通用 + 多次验证 + 有明确适用场景；只出现过一次的问题不提议写进全局规则。

完成后回复简短汇报：新增了几条候选，各自的目标文件。
"""

APPLY_TEMPLATE = """
执行记忆系统的"晋升"任务（合入阶段，人已批阅）。

SOP: {kb_path}

步骤：
1. 读取 contexts/memory/RULE_CANDIDATES.md 的「待批阅」部分。
2. 只处理勾选了「- [x] 批准」的候选：按候选里写明的目标文件和改动修改 rules/。没有勾选的候选一律不动。
3. 把已合入的候选整条移到「## 已处理」小节，标题后加上「（已合入 YYYY-MM-DD）」。
4. GC：重写 contexts/memory/OBSERVATIONS.md，删除已经合入规则的内容和过期的 🟢 记录。

完成后回复简短汇报：合入了哪几条，分别改了哪个文件。
"""


def snapshot(path):
    """sha256 of every file under path, keyed by relative path."""
    out = {}
    for base, _, files in os.walk(path):
        for name in files:
            full = os.path.join(base, name)
            with open(full, "rb") as f:
                out[os.path.relpath(full, path)] = hashlib.sha256(f.read()).hexdigest()
    return out


def changed(before, after):
    keys = set(before) | set(after)
    return sorted(k for k in keys if before.get(k) != after.get(k))


def run(client, title, prompt, model_id):
    session_id = client.create_session(title)
    if not session_id:
        return None
    client.send_message(session_id, prompt, model_id=model_id)
    # If send_message timed out, agent may still be running; poll until done
    print("Waiting for session to complete (sync mode)...")
    client.wait_for_session_complete(session_id)
    return session_id


def main():
    import argparse
    parser = argparse.ArgumentParser(description='L2 Reflector Agent')
    parser.add_argument('--model', default='<your-model-id>',
                        choices=['<your-model-id>'],
                        help='Model ID to use')
    parser.add_argument('--apply', action='store_true',
                        help='Merge the candidates a human has ticked into rules/ (default: only propose candidates)')
    args = parser.parse_args()

    model_id = args.model
    target_date = datetime.now().strftime("%Y-%m-%d")
    client = OpenCodeClient()

    if args.apply:
        print(f"Applying approved candidates from {CANDIDATES_PATH} using model: {model_id}...")
        session_id = run(client, f"Heartbeat L2 Reflector Apply - {target_date}",
                         APPLY_TEMPLATE.format(kb_path=KNOWLEDGE_BASE), model_id)
        print(f"Task complete (Session: {session_id}).")
        return

    print(f"Proposing rule candidates using model: {model_id}...")
    before = snapshot(RULES_DIR)
    session_id = run(client, f"Heartbeat L2 Reflector Propose - {target_date}",
                     PROPOSE_TEMPLATE.format(kb_path=KNOWLEDGE_BASE, target_date=target_date), model_id)
    touched = changed(before, snapshot(RULES_DIR))
    if touched:
        print("ERROR: rules/ changed during the propose stage, which is not allowed:", file=sys.stderr)
        for path in touched:
            print(f"  rules/{path}", file=sys.stderr)
        print("Review with `git diff -- rules/` and revert what you did not approve.", file=sys.stderr)
        sys.exit(1)
    print(f"Candidates written to {CANDIDATES_PATH}. Review them, tick `- [x] 批准`, then run with --apply.")
    print(f"Task complete (Session: {session_id}).")


if __name__ == "__main__":
    main()
