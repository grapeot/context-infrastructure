## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Open the app in Cursor's browser at multiple viewport sizes, screenshot each, and report any layout breakage.
- **上游来源**: [responsive-testing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/responsive-testing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Responsive Testing

After a UI change, verify the app looks correct at all standard breakpoints.

## Viewports to Test

| Name | Width | Tailwind |
|------|-------|----------|
| Mobile (small) | 375px | default |
| Mobile (large) | 428px | default |
| Tablet | 768px | `md:` |
| Desktop | 1280px | `xl:` |
| Ultrawide | 1536px | `2xl:` |

## Workflow

### 1. Navigate to the Page

Use `browser_navigate` to open the target URL (usually `http://localhost:3000` or whatever the dev server is running on).

### 2. Test Each Viewport

For each viewport size:

1. Resize the viewport using `browser_navigate` with viewport parameters, or use `browser_snapshot` to inspect the layout
2. Take a screenshot with `browser_take_screenshot`
3. Check `browser_snapshot` for the aria tree — look for:
   - Content overflowing or hidden behind other elements
   - Navigation that should collapse into a hamburger menu
   - Text that's too small to read
   - Buttons/links too close together (touch target issues)
   - Horizontal scrollbars that shouldn't exist

### 3. Check for Common Breakage

- **Overflow**: Elements wider than the viewport causing horizontal scroll
- **Collapsed layout**: Flex/grid items that should stack on mobile but don't
- **Hidden content**: Elements that disappear at certain sizes without a menu toggle
- **Font scaling**: Text that's readable on desktop but tiny on mobile
- **Fixed positioning**: Modals, toasts, or sticky headers that break on small screens
- **Images**: Oversized images that don't scale down

### 4. Report

```
Responsive Test Results:
  375px (mobile):  PASS — layout stacks correctly
  428px (mobile):  PASS
  768px (tablet):  WARN — nav items overlap, need hamburger menu
  1280px (desktop): PASS
  1536px (ultrawide): WARN — content not centered, stretched too wide
```

Fix any issues found, then re-test the affected viewports.
