#!/usr/bin/env python3
"""
job_guard — cron job 失败通知守护。

用法：
  python job_guard.py <command> [args...]

做的事情很简单：
  1. 运行你给它的命令
  2. 命令成功 → 什么都不做
  3. 命令失败 → 给你发一封邮件，告诉你哪个任务挂了、报了什么错

示例 crontab 配置：
  0 8 * * * cd /your/workspace && .venv/bin/python tools/job_guard.py .venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py

环境变量（从 .env 自动加载）：
  GMAIL_USERNAME      — 发件邮箱
  GMAIL_APP_PASSWORD  — Gmail 应用专用密码
  GMAIL_RECIPIENTS    — 收件人（默认发给自己）
"""
import os
import sys
import subprocess
import socket
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# 邮件发送（复用 send_email_to_myself 的逻辑，但内联以避免循环依赖）
# ---------------------------------------------------------------------------

def _load_dotenv():
    """向上查找 .env 并注入环境变量。"""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip('"\'')
                    if k and k not in os.environ:
                        os.environ[k] = v
            break


def _send_failure_email(subject, body):
    """发送纯文本失败通知邮件。"""
    import smtplib
    from email.mime.text import MIMEText

    _load_dotenv()
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_APP_PASSWORD")
    to_addr = os.getenv("GMAIL_RECIPIENTS")

    if not all([username, password, to_addr]):
        # 邮件配置不全时退化为 stderr 输出，至少 cron 的 MAILTO 还能兜底
        print(f"[job_guard] 邮件配置不全，无法发送通知。Subject: {subject}", file=sys.stderr)
        print(body, file=sys.stderr)
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = username
    msg["To"] = to_addr
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, [to_addr], msg.as_string())
        return True
    except Exception as e:
        print(f"[job_guard] 发送邮件失败: {e}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# 主逻辑
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <command> [args...]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1:]
    job_name = Path(cmd[-1]).stem if cmd else "unknown"
    started_at = datetime.now()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=7200,  # 2 小时超时保护
        )
    except subprocess.TimeoutExpired:
        elapsed = datetime.now() - started_at
        subject = f"[TIMEOUT] {job_name} 超时未完成"
        body = (
            f"任务: {' '.join(cmd)}\n"
            f"机器: {socket.gethostname()}\n"
            f"开始: {started_at:%Y-%m-%d %H:%M:%S}\n"
            f"耗时: {elapsed}\n"
            f"状态: 超过 2 小时未完成，已被强制终止\n"
        )
        _send_failure_email(subject, body)
        sys.exit(124)
    except Exception as e:
        subject = f"[ERROR] {job_name} 启动失败"
        body = f"任务: {' '.join(cmd)}\n异常: {e}\n"
        _send_failure_email(subject, body)
        sys.exit(1)

    # 命令成功 → 透传 stdout 后静默退出
    if result.returncode == 0:
        if result.stdout:
            sys.stdout.write(result.stdout)
        sys.exit(0)

    # 命令失败 → 发通知
    elapsed = datetime.now() - started_at
    subject = f"[FAILED] {job_name} 退出码 {result.returncode}"

    # 截取最后 200 行，避免邮件过长
    stderr_tail = "\n".join(result.stderr.splitlines()[-200:]) if result.stderr else "(无 stderr 输出)"
    stdout_tail = "\n".join(result.stdout.splitlines()[-50:]) if result.stdout else "(无 stdout 输出)"

    body = (
        f"任务: {' '.join(cmd)}\n"
        f"机器: {socket.gethostname()}\n"
        f"开始: {started_at:%Y-%m-%d %H:%M:%S}\n"
        f"耗时: {elapsed}\n"
        f"退出码: {result.returncode}\n"
        f"\n{'='*60}\n"
        f"STDERR (最后 200 行):\n{stderr_tail}\n"
        f"\n{'='*60}\n"
        f"STDOUT (最后 50 行):\n{stdout_tail}\n"
    )

    _send_failure_email(subject, body)

    # 同时输出到 stderr，让 cron 日志也有记录
    print(f"[job_guard] {job_name} failed with exit code {result.returncode}", file=sys.stderr)
    if result.stderr:
        sys.stderr.write(result.stderr)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
