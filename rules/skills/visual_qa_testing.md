## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Visually QA a web application by launching it in Cursor's built-in browser, taking screenshots, checking console errors, and auditing network requests. Use after making UI changes to verify they look correct.
- **上游来源**: [visual-qa-testing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/visual-qa-testing)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Visual QA

Use this skill after making UI changes to visually verify the result, catch console errors, and audit network requests — all without leaving Cursor.

## How It Works

Cursor has a built-in browser (`cursor-ide-browser` MCP) that can navigate to URLs, take screenshots, read console messages, inspect network requests, and interact with page elements. This skill uses those tools to do a quick visual QA pass.

## Steps

1. **Ensure the dev server is running** — check if there's already a terminal running the dev server. If not, start one in the background:

   ```bash
   npm run dev
   ```

   Wait for the server to be ready (watch for the "ready" or localhost URL in the output).

2. **Navigate to the page** — use `browser_navigate` to open the relevant page:

   ```
   Tool: browser_navigate
   Arguments: { "url": "http://localhost:3000", "take_screenshot_afterwards": true }
   ```

   If the change is on a specific route, navigate directly to it (e.g., `/settings`, `/dashboard`).

3. **Take a screenshot** — capture the current state:

   ```
   Tool: browser_take_screenshot
   Arguments: { "fullPage": true }
   ```

   Review the screenshot for visual issues: layout breaks, missing content, wrong colors, misaligned elements.

4. **Check console for errors** — look for JavaScript errors or warnings:

   ```
   Tool: browser_console_messages
   ```

   Report any errors, especially `TypeError`, `ReferenceError`, failed imports, or React hydration mismatches.

5. **Audit network requests** — check for failed API calls or unexpected requests:

   ```
   Tool: browser_network_requests
   ```

   Look for: 4xx/5xx status codes, CORS errors, excessively large responses, unnecessary duplicate requests.

6. **Interact if needed** — if the change involves interactive elements (buttons, forms, modals), use `browser_click`, `browser_fill`, or `browser_hover` to test the interaction, then take another screenshot to verify.

7. **Report findings** — summarize:
   - Screenshot shows the UI looks correct (or what's wrong)
   - Console is clean (or list errors found)
   - Network requests are healthy (or list failures)

## Notes

- Always use `browser_snapshot` before clicking elements to get the correct element refs.
- For responsive testing, use `browser_resize` to check different viewport sizes.
- Use `browser_navigate` with `position: "side"` to open the browser beside your code.
