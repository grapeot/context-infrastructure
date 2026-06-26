from __future__ import annotations

import os
import subprocess
import uuid
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

module_dir = Path(__file__).resolve().parent
project_env_path = module_dir.parent.parent / ".env"
legacy_env_path = module_dir.parent / ".env"
if load_dotenv:
    if project_env_path.exists():
        load_dotenv(project_env_path)
    else:
        load_dotenv(legacy_env_path)

MESSAGE_TIMEOUT = int(os.getenv("CURSOR_AGENT_TIMEOUT", "3600"))
CREATE_CHAT_TIMEOUT = int(os.getenv("CURSOR_CREATE_CHAT_TIMEOUT", "120"))


class CursorClient:
    """Cursor Agent CLI client with an OpenCodeClient-compatible surface."""

    def __init__(self, workspace: str | None = None, *, resume_chat: bool = False):
        default_workspace = module_dir.parent.parent.parent.parent
        self.workspace = Path(workspace or os.getenv("CURSOR_WORKSPACE", default_workspace))
        self.agent_bin = os.getenv("CURSOR_AGENT_BIN", "agent")
        self.resume_chat = resume_chat or os.getenv("CURSOR_USE_RESUME_CHAT", "").lower() in {
            "1",
            "true",
            "yes",
        }
        self._sessions: dict[str, dict] = {}
        self._prompt_dir = self.workspace / ".cursor_tmp" / "heartbeat"
        self._prompt_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, title: str) -> str | None:
        if not self.resume_chat:
            session_id = str(uuid.uuid4())
            self._sessions[session_id] = {"title": title, "done": False, "chat_id": None}
            return session_id

        try:
            result = subprocess.run(
                [self.agent_bin, "create-chat"],
                capture_output=True,
                text=True,
                timeout=CREATE_CHAT_TIMEOUT,
                check=True,
            )
            chat_id = result.stdout.strip()
            if not chat_id:
                print("Error creating Cursor chat: empty chat id")
                return None
            self._sessions[chat_id] = {"title": title, "done": False, "chat_id": chat_id}
            return chat_id
        except subprocess.TimeoutExpired:
            print(
                f"Error creating Cursor chat: timed out after {CREATE_CHAT_TIMEOUT}s. "
                "One-shot mode does not need create-chat; unset CURSOR_USE_RESUME_CHAT."
            )
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error creating Cursor chat: {e.stderr or e}")
            return None
        except Exception as e:
            print(f"Error creating Cursor chat: {e}")
            return None

    def send_message(
        self,
        session_id: str,
        message: str,
        model_id: str = "composer-2.5",
        provider_id=None,
        agent=None,
    ):
        del provider_id, agent
        prompt_path = self._prompt_dir / f"task_{session_id[:8]}_{uuid.uuid4().hex[:8]}.txt"
        try:
            prompt_path.write_text(message, encoding="utf-8")
            driver_prompt = (
                f"Read and execute the full task prompt from {prompt_path}. "
                "Do not delete the prompt file."
            )
            cmd = [
                self.agent_bin,
                "-p",
                "--force",
                "--approve-mcps",
                "--model",
                model_id,
            ]
            chat_id = (self._sessions.get(session_id) or {}).get("chat_id")
            if chat_id:
                cmd.extend(["--resume", chat_id])
            cmd.append(driver_prompt)

            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                timeout=MESSAGE_TIMEOUT,
            )
            self._sessions.setdefault(session_id, {})["done"] = True
            if result.returncode != 0:
                print(f"Cursor agent exited with code {result.returncode}")
                return None
            return {"status": "ok", "session_id": session_id}
        except subprocess.TimeoutExpired:
            print(f"Cursor agent timed out after {MESSAGE_TIMEOUT}s")
            return None
        except Exception as e:
            print(f"Error running Cursor agent: {e}")
            return None

    def get_session_messages(self, session_id: str):
        del session_id
        return None

    def delete_session(self, session_id: str) -> bool:
        self._sessions.pop(session_id, None)
        return True

    def get_session_info(self, session_id: str):
        session = self._sessions.get(session_id)
        if not session:
            return None
        done = session.get("done", False)
        return {"running": not done, "status": "idle" if done else "running"}

    def wait_for_session_complete(
        self,
        session_id: str,
        poll_interval=15,
        max_wait=7200,
    ) -> bool:
        del poll_interval, max_wait
        session = self._sessions.get(session_id)
        if session and session.get("done"):
            return True
        info = self.get_session_info(session_id)
        return bool(info and not info.get("running"))
