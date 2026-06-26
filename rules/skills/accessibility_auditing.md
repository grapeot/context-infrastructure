## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Use Cursor's browser aria snapshots to audit a page for accessibility issues — missing labels, broken tab order, contrast, and ARIA misuse.
- **上游来源**: [accessibility-auditing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/accessibility-auditing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Accessibility Auditing

Audit a web page for accessibility issues using Cursor's built-in browser without external tools.

## Workflow

### 1. Open the Page

Use `browser_navigate` to open the target URL.

### 2. Capture the Accessibility Tree

Use `browser_snapshot` — this returns the aria/accessibility tree of the page. This is the same tree that screen readers use.

### 3. Audit the Tree

Check for these issues:

**Missing Labels**
- `button` elements with no accessible name (no text, no `aria-label`)
- `img` elements with no `alt` text
- `input` elements with no associated `label` or `aria-label`
- `a` (link) elements with no text content
- Icon-only buttons missing `aria-label`

**Semantic HTML**
- Clickable `div` or `span` elements → should be `button` or `a`
- Missing `nav`, `main`, `header`, `footer` landmarks
- Headings that skip levels (h1 → h3)
- Lists that aren't using `ul`/`ol`/`li`

**Keyboard Navigation**
- Interactive elements missing from tab order
- Custom widgets without `role` and keyboard handlers
- Focus traps in modals (should trap focus, but also allow Escape to close)
- Skip-to-content link missing

**ARIA Issues**
- `aria-hidden="true"` on focusable elements
- Invalid `role` values
- `aria-expanded` without corresponding collapsible content
- `aria-controls` pointing to non-existent IDs

**Contrast** (use screenshot for visual check)
- Light gray text on white backgrounds
- Placeholder text that's too faint
- Disabled states that are indistinguishable

### 4. Test Keyboard Navigation

Use `browser_press` to simulate Tab key presses and verify:
- Every interactive element receives focus
- Focus order is logical (top-to-bottom, left-to-right)
- Focus is visible (focus ring or outline)
- Escape closes modals/dropdowns

### 5. Report

```
Accessibility Audit:
  Critical:
    - 3 buttons with no accessible name (header icons)
    - Login form inputs missing labels
  Warnings:
    - Heading levels skip from h1 to h3
    - No skip-to-content link
    - 2 clickable divs should be buttons
  Passed:
    - All images have alt text
    - Landmarks present (nav, main, footer)
    - Focus order is logical
```

### 6. Fix

For each issue, apply the fix in the source code. Common fixes:
- Add `aria-label="Close"` to icon buttons
- Wrap inputs in `<label>` or add `htmlFor`
- Change `<div onClick>` to `<button>`
- Add `alt` text to images
- Fix heading hierarchy
