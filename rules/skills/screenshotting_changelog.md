## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Generate a visual changelog or PR description by taking before/after screenshots of UI changes using Cursor's built-in browser. Use when preparing a PR with visual changes.
- **上游来源**: [screenshotting-changelog](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/screenshotting-changelog)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Screenshot Changelog

Use this skill when preparing a pull request that includes visual/UI changes. Capture before and after screenshots to create a visual changelog that reviewers can quickly scan.

## Steps

1. **Capture the "before" state** — before making changes (or on the base branch), start the dev server and screenshot the affected pages:

   ```bash
   git stash  # or checkout the base branch
   ```

   Start the dev server, then:

   ```
   Tool: browser_navigate
   Arguments: { "url": "http://localhost:3000/affected-page", "take_screenshot_afterwards": true }
   ```

   ```
   Tool: browser_take_screenshot
   Arguments: { "fullPage": true, "filename": "before-homepage.png" }
   ```

   Repeat for each affected page or component state.

2. **Switch to the feature branch** — apply your changes:

   ```bash
   git stash pop  # or checkout the feature branch
   ```

   Wait for the dev server to hot-reload (or restart it).

3. **Capture the "after" state** — screenshot the same pages:

   ```
   Tool: browser_take_screenshot
   Arguments: { "fullPage": true, "filename": "after-homepage.png" }
   ```

4. **Generate the changelog** — create a summary describing what changed visually:

   ```markdown
   ## Visual Changes

   ### Homepage
   **Before:**
   ![before](before-homepage.png)

   **After:**
   ![after](after-homepage.png)

   Changes: Updated hero section layout, new CTA button color, added testimonials section.
   ```

5. **Include in the PR description** — paste the visual changelog into the PR body so reviewers can see the changes at a glance without running the app locally.

## Variations

- **Responsive comparison**: use `browser_resize` to capture screenshots at mobile (375px), tablet (768px), and desktop (1280px) widths.
- **Dark mode comparison**: if the app has a dark mode toggle, capture both themes.
- **Interactive states**: capture hover states, open modals, filled forms, and error states.

## Notes

- Screenshots are saved to the workspace. You can reference them in markdown or upload them to the PR.
- For component-level screenshots, navigate to a Storybook URL or a specific component route.
- This is most valuable for design-heavy PRs — skip it for backend-only changes.
