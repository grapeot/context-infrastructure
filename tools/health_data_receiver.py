#!/usr/bin/env python3
"""
Health Data Receiver — 接收 iPhone Shortcuts 推送的健康数据。

轻量 HTTP server，监听本地端口，接收 POST JSON 并落盘到 contexts/health/data/。

启动方式：
  python3 tools/health_data_receiver.py                  # 默认 port 9876
  python3 tools/health_data_receiver.py --port 9876

iPhone Shortcuts 调用：
  POST http://<mac-ip>:9876/health
  Content-Type: application/json
  Body: { "date": "2026-04-07", "sleep": {...}, "heart": {...}, ... }

安全说明：
  - 仅监听局域网，不暴露公网
  - 可选 token 认证（通过环境变量 HEALTH_RECEIVER_TOKEN）
"""

import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "contexts" / "health" / "data"
AUTH_TOKEN = os.getenv("HEALTH_RECEIVER_TOKEN", "")


class HealthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/health":
            self._respond(404, {"error": "Not found"})
            return

        # Token auth (optional)
        if AUTH_TOKEN:
            token = self.headers.get("Authorization", "").removeprefix("Bearer ").strip()
            if token != AUTH_TOKEN:
                self._respond(401, {"error": "Unauthorized"})
                return

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._respond(400, {"error": "Empty body"})
            return

        try:
            body = self.rfile.read(content_length)
            data = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self._respond(400, {"error": f"Invalid JSON: {e}"})
            return

        # Determine date
        date_str = data.get("date", datetime.now().date().isoformat())
        # Validate date format
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            self._respond(400, {"error": f"Invalid date format: {date_str}"})
            return

        # Save to disk
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        output_path = DATA_DIR / f"{date_str}.json"
        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        print(f"[{datetime.now().isoformat()}] Saved health data: {output_path}")
        self._respond(200, {"status": "ok", "path": str(output_path)})

    def do_GET(self):
        if self.path == "/ping":
            self._respond(200, {"status": "ok"})
        else:
            self._respond(404, {"error": "Not found"})

    def _respond(self, code: int, body: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode("utf-8"))

    def log_message(self, format, *args):
        # Quieter logging
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Health Data Receiver")
    parser.add_argument("--port", type=int, default=9876)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), HealthHandler)
    print(f"Health Data Receiver listening on {args.host}:{args.port}")
    print(f"POST http://<your-mac-ip>:{args.port}/health")
    if AUTH_TOKEN:
        print("Token auth: ENABLED")
    else:
        print("Token auth: DISABLED (set HEALTH_RECEIVER_TOKEN to enable)")
    print(f"Data dir: {DATA_DIR}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
