#!/usr/bin/env python3
"""
L1 Observer Agent (Trigger Script)
Instructs an agentic engine (Cursor or OpenCode) to scan, filter, and write to memory.
"""
from datetime import datetime

from agent_client import WORKSPACE_ROOT, add_engine_args, default_model, get_client

KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts/memory/OBSERVATIONS.md"

PROMPT_TEMPLATE = """
【目标】：执行观测记忆提取并直接持久化到磁盘。
【基准日期】：{target_date}

【幂等性约束】：在执行任何写入前，**必须先**读取 OBSERVATIONS.md，检查是否已存在 `Date: {target_date}` 的条目。若存在，则**不要进行任何文件修改**，直接回复「Entry for {target_date} already exists, skipping」即可。

【SOP 路径】：
{kb_path}

【任务内容】：
1. **获取 Context**：请阅读上述 SOP 以及其中引用的 L3 约束文件。
2. **幂等性检查**：读取 OBSERVATIONS.md，若已有 `Date: {target_date}` 则跳过后续步骤。
3. **扫描与过滤**：自主扫描根目录（{workspace_root}）下的变动。
4. **写入记忆**：将针对 {target_date} 的 🔴 🟡 🟢 观测结果直接写入或追加到 `{observations_path}`。**鼓励使用命令行 append**（如 `echo "..." >> OBSERVATIONS.md` 或 `tee -a`），避免对大文件做全文编辑。
5. **范围约束**：**仅执行 L1 Observer 任务**。不要执行 SOP 中提到的 L2 Reflector 任务（即不要修改 `rules/` 下的任何文件，不要进行规则晋升或垃圾回收）。
6. **格式规范**：
   - 日期 Header 必须严格使用 `Date: YYYY-MM-DD` 格式（Date 首字母大写，冒号后空格，日期为 ISO 格式）。
   - 在结果文件中提到任何文件或目录时，**必须使用相对于根目录的完整路径**（例如：`rules/skills/workflow_deep_research_survey.md`），不要只写文件名。
7. **汇报**：完成后，在此回复一个简短的 Walkthrough。
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description="L1 Observer Agent")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Target date (YYYY-MM-DD)",
    )
    add_engine_args(parser)
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Keep session after completion (OpenCode only; Cursor chats are always kept)",
    )
    args = parser.parse_args()

    target_date = args.date
    model_id = args.model or default_model(args.engine)
    delete_after = not args.no_delete

    if OBSERVATIONS_PATH.exists():
        content = OBSERVATIONS_PATH.read_text(encoding="utf-8")
        if f"Date: {target_date}" in content:
            print(
                f"Idempotent skip: entry for {target_date} already exists in OBSERVATIONS.md"
            )
            return

    print(
        f"Triggering L1 Observer for {target_date} "
        f"(engine={args.engine}, model={model_id})..."
    )
    client = get_client(args.engine)

    session_id = client.create_session(f"Heartbeat L1 - Persistence Mode - {target_date}")
    if not session_id:
        return

    prompt = PROMPT_TEMPLATE.format(
        kb_path=KNOWLEDGE_BASE,
        target_date=target_date,
        workspace_root=WORKSPACE_ROOT,
        observations_path=OBSERVATIONS_PATH,
    )
    client.send_message(session_id, prompt, model_id=model_id)
    print("Waiting for session to complete (sync mode)...")
    client.wait_for_session_complete(session_id)

    if delete_after:
        if client.delete_session(session_id):
            print(f"Task complete (session {session_id} deleted).")
        else:
            print(f"Task complete (Session: {session_id}).")
    else:
        print(f"Task complete (Session: {session_id}).")


if __name__ == "__main__":
    main()
