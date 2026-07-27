# AI Session Search & Archive

## Objective

Find prior AI sessions across a unified Markdown archive without depending on a
single vendor's history UI. Use lexical search for names and identifiers, then
semantic search when the remembered wording is approximate.

This workflow assumes an archive produced by a multi-source exporter such as
[ai_session_export](https://github.com/grapeot/ai_session_export). Keep the
archive private: session titles, transcripts, project paths, and identifiers
may all contain sensitive information.

## Source Routing

A typical archive has one directory per source:

```text
contexts/ai_sessions/
  opencode/
  claude_code/
  codex/
  antigravity/
  second_mind/
```

- When the user names a source, search only that directory.
- When the source is unknown, search every available source directory.
- Generate client-specific action links only when the result metadata and host
  explicitly support them. Otherwise return an ordinary Markdown file link.

## Retrieval Order

### 1. Lexical search for named entities

Product names, people, projects, titles, dates, and session ids should use
`rg` first. Expand a remembered name into a few plausible variants rather than
assuming the user's wording exactly matches the archived title.

```bash
rg -i -n --glob '*.md' \
  'Claude Teacher|Claude for Teachers|Anthropic for Teachers' \
  contexts/ai_sessions/{opencode,claude_code,codex,antigravity,second_mind}/
```

Glob searches filenames, not file contents. A truncated glob result is not
evidence that no matching session exists.

### 2. Semantic search for approximate memories

Generate the file list from the current source scope at query time. Do not
reuse an old `tmp/*files*.txt`: a semantic-search file list is also a result
allowlist, so an omitted file cannot be returned even if its vectors exist in
the cache.

```bash
FILELIST="$(mktemp)"
trap 'rm -f "$FILELIST"' EXIT
rg --files contexts/ai_sessions/{opencode,claude_code,codex,antigravity,second_mind}/ \
  -g '*.md' > "$FILELIST"

semantic-search query \
  --file-list "$FILELIST" \
  --cache-dir .knowledge_cache \
  --query 'the remembered concept' \
  --top-k 10 \
  --no-refresh
```

Use the installed semantic-search skill's provider and model configuration.
Index refresh is a separate maintenance action; a read-only lookup should not
silently rebuild a large shared cache.

## Freshness Fallback

Check the exporter's state or sync log before reading native stores. If the
target session predates the latest successful source export, search the
archive directly. Only perform a source-specific temporary export when the
session is newer than the archive. Delete temporary exports after lookup.

## Result Contract

- Group chunks by source and session id so one session appears once.
- Show title, date, source, project short name when available, and a verbatim
  excerpt that lets the user verify the match.
- Do not display embedding scores or replace evidence with an AI summary.
- Read action ids from frontmatter; never infer them from filenames or text.
- Do not put credentials, server addresses, local host profiles, absolute
  archive paths, or user queries into action URLs.
- For OpenCode sessions, the deep link is `[Open in OpenCode](opencode://session/<session_id>)`
  with the ID taken verbatim from frontmatter. A legal ID (per the public
  OpenCode iOS Client RFC §4.4, https://github.com/grapeot/opencode_ios_client/blob/main/docs/OpenCode_iOS_Client_RFC.md#L485)
  requires scheme `opencode`, host `session`, a single path segment, and an ID
  starting with `ses_` followed by ASCII letters, digits, underscores, or
  hyphens only. The parser rejects userinfo, port, query, fragment, multi-segment
  paths, control characters, Unicode, double percent encoding, and overlong
  IDs. Antigravity / Claude Code / Codex / Second Mind IDs (UUIDs or non-`ses_`
  prefixes) do not satisfy this contract and cannot produce a deep link.

## Acceptance Criteria

A session lookup is complete when the search covered the correct source scope,
named-entity variants were tried before semantic fallback, semantic queries
used a fresh scoped file list, duplicate chunks were consolidated, and every
navigation action came from validated archive metadata.
