## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Execute a user flow step-by-step in Cursor's built-in browser while documenting each action, then emit a Playwright test that replays the same flow using stable selectors derived from the accessibility tree.
- **上游来源**: [recording-browser-flow-as-test](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/recording-browser-flow-as-test)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Recording Browser Flow as Playwright Test

Use the **browser** MCP as a **recorder**: every navigation, click, fill, and keypress becomes a row in a script. The agent then translates that trace into a **Playwright** test file in the repo (or a snippet to paste into an existing spec).

This is Cursor-native because it combines `browser_snapshot` (refs + roles + names) with structured actions — not a separate recorder extension.

## Prerequisites

- Target app reachable (e.g. dev server running); use `finding-dev-server-url` if needed.
- Repo has or will have Playwright installed (`@playwright/test`). If not, add it with `adding-e2e-tests` or the project’s standard setup.

## Recording workflow

### 1. Define the flow

One sentence scope, e.g. “Log in, open Settings, toggle dark mode, save.”

### 2. For each step, in order

1. **`browser_snapshot`** — get the accessibility tree and element refs.
2. Choose the **smallest** interaction:
   - `browser_click` with ref from snapshot (not coordinate clicks unless required).
   - `browser_fill` or `browser_type` for inputs.
   - `browser_select_option` for selects.
   - `browser_navigate` for full URL changes.
3. **Log the step** in a structured list the main agent keeps:

   - Step number
   - Action verb (`navigate`, `click`, `fill`, `press`, `select`)
   - **Locator strategy for Playwright** — prefer:
     - `getByRole('button', { name: '...' })`
     - `getByLabel('...')`
     - `getByPlaceholder('...')`
     - `getByTestId('...')` if the app uses test IDs
   - Value (for fills), URL (for navigates)
   - Optional: short assertion (“expect URL to contain `/settings`”)

4. After actions that change the DOM or navigate, take a **new** `browser_snapshot` before the next interaction.

5. If the flow must wait for async content, use `browser_wait_for` or short incremental waits per `cursor-ide-browser` guidance — then snapshot again.

### 3. Add assertions

From the final snapshot and URL, add **at least**:

- `expect(page).toHaveURL(...)` or URL fragment check
- One **visible** outcome: text, role, or test id

### 4. Generate Playwright output

Emit a test file, e.g. `tests/recorded/<flow-name>.spec.ts`, containing:

- `test.describe` and `test('...', async ({ page }) => { ... })`
- Steps as `await page.goto(...)`, `await page.getByRole(...).click()`, etc.
- **No** raw snapshot refs in the final file — they are session-specific.

### 5. Run and harden

```bash
npx playwright test tests/recorded/<flow-name>.spec.ts
```

Fix flakiness: prefer `expect(locator).toBeVisible()` before clicks, use `toPass()` retries for async lists, avoid arbitrary `waitForTimeout` except as last resort.

## Tips

- **Stable selectors**: roles and accessible names beat CSS from devtools. Add `data-testid` in app code if names are ambiguous.
- **Auth**: if the flow needs login, use env vars for test credentials or Playwright `storageState` — never commit secrets.
- **Parallel runs**: ensure test data does not collide with other tests.

## When not to use

- Flows that require manual 2FA, captchas, or email links — stop and ask the user for a test bypass or mock.
