from __future__ import annotations

import os
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = MODULE_DIR.parent.parent.parent.parent


def get_client(engine: str, workspace: Path | None = None):
    root = workspace or WORKSPACE_ROOT
    if engine == "cursor":
        from cursor_client import CursorClient

        return CursorClient(workspace=str(root))
    if engine == "opencode":
        from opencode_client import OpenCodeClient

        return OpenCodeClient()
    raise ValueError(f"Unknown engine: {engine}. Use 'cursor' or 'opencode'.")


def default_model(engine: str) -> str:
    if engine == "cursor":
        return os.getenv("CURSOR_AGENT_MODEL", "composer-2.5")
    return os.getenv("OPENCODE_MODEL", "antigravity-gemini-3-flash")


def add_engine_args(parser) -> None:
    parser.add_argument(
        "--engine",
        default=os.getenv("HEARTBEAT_ENGINE", "cursor"),
        choices=["cursor", "opencode"],
        help="Agent engine (default: HEARTBEAT_ENGINE or cursor)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model ID (defaults to CURSOR_AGENT_MODEL or OPENCODE_MODEL)",
    )
