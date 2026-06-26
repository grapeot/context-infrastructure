## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: After navigating and interacting in Cursor's built-in browser, use browser_network_requests to audit every fetch/XHR for failures, slowness, duplicate calls, and suspicious payloads. Use for API-heavy pages and after backend or client networking changes.
- **上游来源**: [network-request-auditing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/network-request-auditing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Network Request Auditing

Deep-dive **network** health using the `cursor-ide-browser` MCP. This skill focuses on `browser_network_requests` — not just “any 500s” but patterns that indicate bugs, waste, or security issues.

## How it works

1. Drive the app in the browser (navigate, click, submit forms) so real requests fire.
2. Call **`browser_network_requests`** after meaningful interactions (and after navigation settles).
3. Classify and report findings using the criteria below.

Follow `cursor-ide-browser` workflow rules: use `browser_snapshot` before structural interactions; after actions that change the page, take a fresh snapshot before the next interaction.

## Audit checklist

### Failures

- **4xx / 5xx** — list method, URL (path + query), status, and whether the UI handled the error.
- **CORS or network errors** — often misconfigured origins or mixed content.

### Performance

- **Slow requests** — flag requests with high latency (e.g. > 500 ms server time if timings are visible; otherwise note unusually large waterfalls).
- **Duplicate calls** — same URL + method fired multiple times in one user action (often a React effect or missing deduplication).
- **Oversized payloads** — responses that look huge for what the UI needs (suggest pagination, field selection, or compression).

### Security and privacy

- **Sensitive data in URLs** — tokens or PII in query strings.
- **Missing auth** — API calls that should send credentials or bearer tokens but do not (compare with adjacent authenticated calls).

### Correctness

- **Unexpected hosts** — calls to third parties not documented for the feature (trackers, accidental leaks).
- **Preflight storms** — excessive OPTIONS requests may indicate wrong CORS caching or too many distinct origins.

## Steps

1. **Start from a clean navigation** — `browser_navigate` to the target URL (or use an existing tab via `browser_tabs`).

2. **Exercise the feature** — interactions that trigger API usage (filters, infinite scroll, form save, modal open).

3. **Fetch network log** — `browser_network_requests` after each logical step if the page does multiple round-trips.

4. **Report** — structured output:
   - Summary counts (failed, slow, duplicate groups).
   - Table or bullet list of issues with **URL pattern** (not necessarily full secrets), **status**, **category** (failure / perf / security / correctness).
   - Recommended next code changes or investigations.

## Notes

- Iframe traffic may not appear in the same log — note if the feature runs inside an iframe.
- Compare against **expected** API design; a 404 might be correct for “optional resource not found” if handled in UI.
- Pair with `browser_console_messages` for errors that do not surface as failed HTTP (e.g. parse errors after 200).
