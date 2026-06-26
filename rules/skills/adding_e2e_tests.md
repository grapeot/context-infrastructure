## 元数据

- **类型**: Workflow
- **分类**: Testing
- **适用场景**: Set up Playwright end-to-end testing in a project, including test configuration, example tests, and CI integration.
- **上游来源**: [adding-e2e-tests](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-e2e-tests)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add E2E Tests (Playwright)

Use this skill when the user asks to add end-to-end tests, browser tests, integration tests, or set up Playwright.

## Steps

1. **Install Playwright**

   ```bash
   npm init playwright@latest
   ```

   This creates `playwright.config.ts`, a `tests/` directory, and installs browsers. If the project already has a test runner, install manually:

   ```bash
   npm install -D @playwright/test
   npx playwright install
   ```

2. **Configure `playwright.config.ts`**

   - Set `baseURL` to the local dev server URL (e.g. `http://localhost:3000`).
   - Configure `webServer` to start the dev server automatically:

     ```ts
     webServer: {
       command: "npm run dev",
       url: "http://localhost:3000",
       reuseExistingServer: !process.env.CI,
     },
     ```

   - Enable only chromium for local dev speed; enable all browsers in CI.

3. **Create a smoke test** — write a basic test that verifies the app loads:

   ```ts
   import { test, expect } from "@playwright/test";

   test("homepage loads", async ({ page }) => {
     await page.goto("/");
     await expect(page).toHaveTitle(/.+/);
   });
   ```

4. **Add page object pattern (optional)** — for larger apps, create a `tests/pages/` directory with page objects that encapsulate selectors and actions.

5. **Add npm scripts**

   ```json
   {
     "test:e2e": "playwright test",
     "test:e2e:ui": "playwright test --ui"
   }
   ```

6. **Add to `.gitignore`**

   ```
   test-results/
   playwright-report/
   blob-report/
   ```

7. **CI integration** — add a GitHub Actions step that runs `npx playwright install --with-deps` then `npm run test:e2e`. Use the official `actions/upload-artifact` to save the HTML report on failure.

## Notes

- Use `data-testid` attributes for selectors instead of CSS classes.
- Use `test.describe` to group related tests.
- Run `npx playwright codegen` to record tests interactively.
