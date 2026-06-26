## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: After making code changes, start the dev server, open the app in Cursor's built-in browser, and verify everything works — check rendering, console errors, and network health. Use proactively after any UI or API change.
- **上游来源**: [verifying-in-browser](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/verifying-in-browser)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Verify in Browser

Use this skill proactively after making code changes to verify the app actually works. Don't just trust that the code is correct — launch it and check.

## Steps

1. **Start the dev server in the background** — check if one is already running by listing terminals. If not:

   ```bash
   npm run dev
   ```

   Set `block_until_ms: 0` to run it in the background. Then poll until you see the "ready" message with the localhost URL.

2. **Open in the side browser** — launch the app beside your code:

   ```
   Tool: browser_navigate
   Arguments: { "url": "http://localhost:3000", "position": "side", "take_screenshot_afterwards": true }
   ```

3. **Quick health check** — run these three checks:

   **Console errors:**
   ```
   Tool: browser_console_messages
   ```
   Flag any errors. Warnings about deprecations can be noted but aren't blockers.

   **Network failures:**
   ```
   Tool: browser_network_requests
   ```
   Flag any 4xx/5xx responses, failed fetches, or CORS errors.

   **Visual check:**
   Review the screenshot. Does the page render? Is the layout correct? Are there any blank screens or loading spinners that never resolve?

4. **Navigate to the changed page** — if your changes are on a specific route, navigate there and repeat the checks.

5. **Test interactions** — if you changed a form, button, or interactive element:
   - Take a `browser_snapshot` to get element refs
   - Click, fill, or hover on the changed elements
   - Take another screenshot to verify the result

6. **Report the verdict** — tell the user:
   - "Verified in browser — page renders correctly, no console errors, all network requests healthy."
   - Or: "Found issues: [list of problems]"

## When to Use This

- After changing any React component, CSS, or layout code
- After modifying API routes or data fetching
- After updating environment variables or configuration
- After installing or removing dependencies
- Before committing — as a final sanity check

## Notes

- Use `position: "side"` to see code and browser at the same time.
- If the dev server is already running, skip step 1 and go straight to navigating.
- For SSR apps, check both the initial server-rendered HTML and the client-hydrated state.
