## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Profile a running web application's CPU performance using Cursor's built-in browser profiler. Captures call stacks, identifies slow functions, and suggests optimizations. Use when a page feels slow or janky.
- **上游来源**: [profiling-performance](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/profiling-performance)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Performance Profile

Use this skill when a web application feels slow, janky, or unresponsive. Cursor's built-in browser has CPU profiling tools that capture real call stacks and timing data.

## How It Works

The `cursor-ide-browser` MCP provides `browser_profile_start` and `browser_profile_stop` tools that capture Chrome DevTools-format CPU profiles. Profile data is written to `~/.cursor/browser-logs/` as both raw JSON and a human-readable summary.

## Steps

1. **Ensure the app is running** — start the dev server if it isn't already running.

2. **Navigate to the slow page**:

   ```
   Tool: browser_navigate
   Arguments: { "url": "http://localhost:3000/slow-page" }
   ```

3. **Start profiling**:

   ```
   Tool: browser_profile_start
   ```

4. **Reproduce the slow interaction** — use browser tools to trigger the slow behavior:
   - Click buttons, scroll, type in inputs, navigate between pages
   - Use `browser_click`, `browser_scroll`, `browser_fill` to interact
   - Wait a few seconds for the interaction to complete

5. **Stop profiling**:

   ```
   Tool: browser_profile_stop
   ```

   This writes two files to `~/.cursor/browser-logs/`:
   - `cpu-profile-{timestamp}.json` — raw Chrome DevTools profile
   - `cpu-profile-{timestamp}-summary.md` — human-readable summary

6. **Analyze the results** — read both files. Key things to look for in the raw JSON:
   - `profile.nodes[].hitCount` — how many samples hit each function
   - `profile.nodes[].callFrame.functionName` — the function names
   - `profile.samples.length` — total number of samples collected

   Cross-reference with the summary to identify:
   - Functions consuming the most CPU time
   - Unexpected re-renders or layout thrashing
   - Expensive third-party library calls
   - Synchronous operations blocking the main thread

7. **Suggest fixes** — based on the profile data, recommend specific optimizations:
   - Memoize expensive computations
   - Debounce rapid event handlers
   - Move heavy work to a Web Worker
   - Lazy-load components or routes
   - Virtualize long lists

## Notes

- Always read the raw `.json` profile to verify the summary — the summary can miss nuances.
- Profile in development mode first, but be aware that React dev mode adds overhead. For accurate measurements, profile a production build.
- Short profiles (2-5 seconds of interaction) are usually more useful than long ones.
- Compare before/after profiles to verify your optimization actually helped.
