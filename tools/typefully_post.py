#!/usr/bin/env python3
"""Typefully v2 posting CLI — draft, schedule, publish tweets and threads.

Authentication uses TYPEFULLY_API_KEY (Bearer token for the v2 API).
Set TYPEFULLY_SOCIAL_SET_ID in .env or pass --social-set-id to choose the target account.

Usage:
    python tools/typefully_post.py post --text "Hello!" --publish-at now
    python tools/typefully_post.py post --thread-file thread.md --publish-at "2026-04-02T09:00:00Z"
    python tools/typefully_post.py draft --text "Save for later"
    python tools/typefully_post.py publish 12345
    python tools/typefully_post.py schedule 12345 --at "2026-04-02T09:00:00Z"
    python tools/typefully_post.py list --status published --limit 10
    python tools/typefully_post.py delete 12345
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.typefully.com/v2"
MAX_WEIGHTED_TWEET_LENGTH = 280
MAX_WEIGHTED_LONG_POST_LENGTH = 25000
TRANSFORMED_URL_LENGTH = 23
WEIGHT_ONE_RANGES: tuple[tuple[int, int], ...] = (
    (0, 4351),
    (8192, 8205),
    (8208, 8223),
    (8242, 8247),
)
URL_RE = re.compile(r"https?://\S+")


def _load_env_file(env_file: Path) -> bool:
    if not env_file.exists():
        return False
    with env_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if key and key not in os.environ:
                os.environ[key] = value
    return True


def load_dotenv(explicit_env_file: str | None = None) -> Path | None:
    candidates: list[Path] = []

    if explicit_env_file:
        candidates.append(Path(explicit_env_file).expanduser().resolve())

    env_from_var = os.getenv("TYPEFULLY_ENV_FILE")
    if env_from_var:
        candidates.append(Path(env_from_var).expanduser().resolve())

    cwd = Path.cwd()
    candidates.extend((parent / ".env") for parent in [cwd] + list(cwd.parents))

    script_dir = Path(__file__).resolve().parent
    candidates.extend((parent / ".env") for parent in [script_dir] + list(script_dir.parents))

    seen: set[Path] = set()
    for env_file in candidates:
        if env_file in seen:
            continue
        seen.add(env_file)
        if _load_env_file(env_file):
            return env_file
    return None


class TypefullyPostClient:
    def __init__(self, social_set_id: str | None = None) -> None:
        self.base_url: str = DEFAULT_BASE_URL
        self.social_set_id: str | None = social_set_id or os.getenv("TYPEFULLY_SOCIAL_SET_ID")
        self.api_key: str | None = os.getenv("TYPEFULLY_API_KEY")

        if not self.api_key:
            raise ValueError(
                "TYPEFULLY_API_KEY is required in .env. Get it from "
                "https://typefully.com/?settings=api"
            )
        if not self.social_set_id:
            raise ValueError(
                "TYPEFULLY_SOCIAL_SET_ID is required in .env or via --social-set-id. "
                "Use your own Typefully social set ID."
            )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url}/social-sets/{self.social_set_id}{path}"

    def create_draft(
        self,
        posts: list[dict[str, str]],
        *,
        publish_at: str | None = None,
        draft_title: str | None = None,
        platform: str = "x",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "platforms": {
                platform: {
                    "enabled": True,
                    "posts": posts,
                }
            }
        }
        if publish_at:
            body["publish_at"] = publish_at
        if draft_title:
            body["draft_title"] = draft_title

        resp = requests.post(
            self._url("/drafts"),
            headers=self._headers(),
            json=body,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def update_draft(
        self,
        draft_id: str | int,
        *,
        publish_at: str | None = None,
        posts: list[dict[str, str]] | None = None,
        draft_title: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if publish_at:
            body["publish_at"] = publish_at
        if posts is not None:
            body["platforms"] = {"x": {"enabled": True, "posts": posts}}
        if draft_title is not None:
            body["draft_title"] = draft_title

        resp = requests.patch(
            self._url(f"/drafts/{draft_id}"),
            headers=self._headers(),
            json=body,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_draft(self, draft_id: str | int) -> dict[str, Any]:
        resp = requests.get(
            self._url(f"/drafts/{draft_id}"),
            headers=self._headers(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def list_drafts(
        self,
        *,
        status: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        params: dict[str, str | int] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        resp = requests.get(
            self._url("/drafts"),
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def delete_draft(self, draft_id: str | int) -> None:
        resp = requests.delete(
            self._url(f"/drafts/{draft_id}"),
            headers=self._headers(),
            timeout=30,
        )
        if resp.status_code not in (204, 200):
            resp.raise_for_status()


SEPARATOR = "---"


def parse_thread_file(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8").strip()
    if SEPARATOR in text:
        tweets = [t.strip() for t in text.split(SEPARATOR) if t.strip()]
    else:
        tweets = [text]
    return tweets


def parse_thread_stdin() -> list[str]:
    text = sys.stdin.read().strip()
    if SEPARATOR in text:
        tweets = [t.strip() for t in text.split(SEPARATOR) if t.strip()]
    else:
        tweets = [text]
    return tweets


def resolve_tweets(*, text: str | None, thread_file: str | None, thread_stdin: bool) -> list[str] | None:
    if thread_file:
        return parse_thread_file(thread_file)
    if thread_stdin:
        return parse_thread_stdin()
    if text:
        return [text]
    return None


def _char_weight(ch: str) -> int:
    cp = ord(ch)
    for start, end in WEIGHT_ONE_RANGES:
        if start <= cp <= end:
            return 1
    return 2


def weighted_tweet_length(text: str) -> int:
    total = 0
    last = 0
    for match in URL_RE.finditer(text):
        prefix = text[last : match.start()]
        total += sum(_char_weight(ch) for ch in prefix)
        total += TRANSFORMED_URL_LENGTH
        last = match.end()
    total += sum(_char_weight(ch) for ch in text[last:])
    return total


def validate_tweets_fit_limit(tweets: list[str]) -> list[tuple[int, int, str]]:
    failures: list[tuple[int, int, str]] = []
    for idx, tweet in enumerate(tweets, start=1):
        length = weighted_tweet_length(tweet)
        if length > MAX_WEIGHTED_TWEET_LENGTH:
            failures.append((idx, length, tweet))
    return failures


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def summarize_draft(data: dict[str, Any]) -> str:
    draft_id = data.get("id", "?")
    status = data.get("status", "?")
    title = data.get("draft_title") or ""
    platforms = data.get("platforms", {})
    x_posts = platforms.get("x", {}).get("posts", [])
    n_posts = len(x_posts)
    first_text = x_posts[0]["text"][:60] + "..." if x_posts else "(empty)"
    scheduled = data.get("scheduled_date") or data.get("publish_at") or ""

    parts = [f"Draft #{draft_id} [{status}]"]
    if title:
        parts.append(f'"{title}"')
    parts.append(f"{n_posts} tweet{'s' if n_posts != 1 else ''}")
    parts.append(f'"{first_text}"')
    if scheduled and scheduled != "now":
        parts.append(f"scheduled: {scheduled}")
    elif scheduled == "now":
        parts.append("publishing now")

    return " | ".join(parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Typefully v2 posting CLI — create, schedule, and publish tweets and threads.",
        epilog=(
            "Thread file format: tweets separated by '---' on its own line.\n"
            "Environment: TYPEFULLY_API_KEY and TYPEFULLY_SOCIAL_SET_ID are required unless overridden by --social-set-id."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--env-file", help="Path to .env file")
    parser.add_argument("--social-set-id", help="Override social set ID from .env")

    sub = parser.add_subparsers(dest="cmd")

    p_post = sub.add_parser("post", help="Create and optionally publish a tweet or thread")
    p_post.add_argument("--text", help="Tweet text (single tweet)")
    p_post.add_argument("--thread-file", help="Path to thread file (tweets separated by ---)")
    p_post.add_argument("--thread-stdin", action="store_true", help="Read thread from stdin")
    p_post.add_argument("--publish-at", help="'now', 'next-free-slot', or ISO datetime")
    p_post.add_argument("--draft-title", help="Internal title for the draft")
    p_post.add_argument(
        "--long-post",
        action="store_true",
        help="Skip 280-char limit (X Premium long post, up to 25k chars)",
    )

    p_draft = sub.add_parser("draft", help="Create a draft without publishing")
    p_draft.add_argument("--text", help="Tweet text")
    p_draft.add_argument("--thread-file", help="Path to thread file")
    p_draft.add_argument("--thread-stdin", action="store_true", help="Read thread from stdin")
    p_draft.add_argument("--draft-title", help="Internal title")
    p_draft.add_argument(
        "--long-post",
        action="store_true",
        help="Skip 280-char limit (X Premium long post, up to 25k chars)",
    )

    p_count = sub.add_parser("count", help="Inspect X weighted length for a tweet or thread")
    p_count.add_argument("--text", help="Tweet text (single tweet)")
    p_count.add_argument("--thread-file", help="Path to thread file")
    p_count.add_argument("--thread-stdin", action="store_true", help="Read thread from stdin")

    p_publish = sub.add_parser("publish", help="Publish an existing draft immediately")
    p_publish.add_argument("draft_id", help="Draft ID to publish")

    p_schedule = sub.add_parser("schedule", help="Schedule an existing draft")
    p_schedule.add_argument("draft_id", help="Draft ID to schedule")
    p_schedule.add_argument("--at", dest="schedule_at", help="ISO datetime to schedule at")
    p_schedule.add_argument(
        "--next-free-slot", action="store_true", help="Use Typefully's next free slot"
    )

    p_list = sub.add_parser("list", help="List drafts")
    p_list.add_argument("--status", help="Filter by status (draft/scheduled/published/error)")
    p_list.add_argument("--limit", type=int, default=10, help="Max results (default 10)")
    p_list.add_argument("--json", action="store_true", help="Output raw JSON")

    p_get = sub.add_parser("get", help="Get a single draft's details")
    p_get.add_argument("draft_id", help="Draft ID")
    p_get.add_argument("--json", action="store_true", help="Output raw JSON")

    p_delete = sub.add_parser("delete", help="Delete a draft")
    p_delete.add_argument("draft_id", help="Draft ID to delete")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return 0

    try:
        if args.cmd == "count":
            tweets = resolve_tweets(
                text=args.text,
                thread_file=args.thread_file,
                thread_stdin=args.thread_stdin,
            )
            if tweets is None:
                print("Error: provide --text, --thread-file, or --thread-stdin", file=sys.stderr)
                return 1

            for i, tweet in enumerate(tweets, start=1):
                length = weighted_tweet_length(tweet)
                status = "OK" if length <= MAX_WEIGHTED_TWEET_LENGTH else "TOO_LONG"
                print(f"Tweet {i}: {length}/{MAX_WEIGHTED_TWEET_LENGTH} [{status}]")
                print(tweet)
                if i != len(tweets):
                    print()
            return 0

        loaded_env = load_dotenv(args.env_file)

        try:
            client = TypefullyPostClient(social_set_id=args.social_set_id)
        except ValueError as exc:
            source_note = f" (loaded from {loaded_env})" if loaded_env else ""
            print(f"Error: {exc}{source_note}", file=sys.stderr)
            return 1

        if args.cmd in ("post", "draft"):
            tweets = resolve_tweets(
                text=args.text,
                thread_file=args.thread_file,
                thread_stdin=args.thread_stdin,
            )
            if tweets is None:
                print("Error: provide --text, --thread-file, or --thread-stdin", file=sys.stderr)
                return 1

            failures = validate_tweets_fit_limit(tweets)
            long_post = getattr(args, "long_post", False)
            if failures and not long_post:
                for idx, length, tweet in failures:
                    print(
                        f"Error: tweet {idx} exceeds X weighted limit ({length}/{MAX_WEIGHTED_TWEET_LENGTH}).",
                        file=sys.stderr,
                    )
                    print(tweet, file=sys.stderr)
                    print(file=sys.stderr)
                return 1
            if long_post:
                for idx, tweet in enumerate(tweets, start=1):
                    length = weighted_tweet_length(tweet)
                    if length > MAX_WEIGHTED_LONG_POST_LENGTH:
                        print(
                            f"Error: tweet {idx} exceeds X Premium long post limit ({length}/{MAX_WEIGHTED_LONG_POST_LENGTH}).",
                            file=sys.stderr,
                        )
                        return 1
                    if length > MAX_WEIGHTED_TWEET_LENGTH:
                        print(
                            f"Note: tweet {idx} is {length} weighted chars (long post mode, OK up to {MAX_WEIGHTED_LONG_POST_LENGTH}).",
                            file=sys.stderr,
                        )

            posts = [{"text": tweet} for tweet in tweets]
            publish_at = getattr(args, "publish_at", None)
            draft_title = getattr(args, "draft_title", None)

            result = client.create_draft(
                posts,
                publish_at=publish_at,
                draft_title=draft_title,
            )
            print(summarize_draft(result))
            return 0

        if args.cmd == "publish":
            result = client.update_draft(args.draft_id, publish_at="now")
            print(summarize_draft(result))
            return 0

        if args.cmd == "schedule":
            if args.next_free_slot:
                result = client.update_draft(args.draft_id, publish_at="next-free-slot")
            elif args.schedule_at:
                result = client.update_draft(args.draft_id, publish_at=args.schedule_at)
            else:
                print("Error: provide --at or --next-free-slot", file=sys.stderr)
                return 1
            print(summarize_draft(result))
            return 0

        if args.cmd == "list":
            result = client.list_drafts(status=args.status, limit=args.limit)
            if args.json:
                print_json(result)
            else:
                drafts = result.get("results", result if isinstance(result, list) else [])
                if not drafts:
                    print("No drafts found.")
                for draft in drafts:
                    draft_id = draft.get("id", "?")
                    status = draft.get("status", "?")
                    preview = (draft.get("preview") or "")[:80]
                    published_url = draft.get("x_published_url") or ""
                    scheduled = draft.get("scheduled_date") or ""
                    line = f"#{draft_id} [{status}] {preview}..."
                    if published_url:
                        line += f" → {published_url}"
                    elif scheduled:
                        line += f" (scheduled: {scheduled})"
                    print(line)
            return 0

        if args.cmd == "get":
            result = client.get_draft(args.draft_id)
            if args.json:
                print_json(result)
            else:
                print(summarize_draft(result))
                x_posts = result.get("platforms", {}).get("x", {}).get("posts", [])
                for i, post in enumerate(x_posts, start=1):
                    print(f"\n--- Tweet {i} ---")
                    print(post.get("text", ""))
            return 0

        if args.cmd == "delete":
            client.delete_draft(args.draft_id)
            print(f"Draft #{args.draft_id} deleted.")
            return 0

        parser.print_help()
        return 1

    except requests.HTTPError as exc:
        response = exc.response
        if response is not None:
            print(f"HTTP {response.status_code}: {response.text}", file=sys.stderr)
        else:
            print(f"HTTP error: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
