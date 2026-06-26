#!/usr/bin/env python3
"""
L2 Reflector Agent (Trigger Script)
Instructs an agentic engine (Cursor or OpenCode) to perform memory garbage collection.
"""
from datetime import datetime

from agent_client import WORKSPACE_ROOT, add_engine_args, default_model, get_client

KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts/memory/OBSERVATIONS.md"

PROMPT_TEMPLATE = """
执行记忆系统的"反思与晋升"任务。

SOP: {kb_path}

Workspace 根目录: {workspace_root}

步骤：
1. 读取 `{observations_path}`，分析 🔴 和高优 🟡 条目
2. 将具有普适性的内容晋升到 rules/，按职责边界分类：
   - SOUL.md: Agent 身份与核心价值观
   - USER.md: 用户画像与人生哲学
   - COMMUNICATION.md: 沟通风格（仅限沟通，不含技术知识）
   - WORKSPACE.md: 目录路由
   - skills/: 技术方法论、工作流、最佳实践
3. GC：重写 OBSERVATIONS.md，删除已晋升及过期 🟢 记录

晋升门槛：跨项目通用 + 多次验证 + 有明确适用场景
完成后回复简短晋升汇报。
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description="L2 Reflector Agent")
    add_engine_args(parser)
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Keep session after completion (OpenCode only; Cursor chats are always kept)",
    )
    args = parser.parse_args()

    model_id = args.model or default_model(args.engine)
    target_date = datetime.now().strftime("%Y-%m-%d")
    delete_after = not args.no_delete

    print(
        f"Triggering L2 Reflector (engine={args.engine}, model={model_id})..."
    )
    client = get_client(args.engine)

    session_id = client.create_session(f"Heartbeat L2 Reflector - {target_date}")
    if not session_id:
        return

    prompt = PROMPT_TEMPLATE.format(
        kb_path=KNOWLEDGE_BASE,
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
