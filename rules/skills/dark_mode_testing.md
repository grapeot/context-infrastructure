## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Toggle between light and dark mode in Cursor's browser, screenshot both states, and flag missing token mappings or contrast issues.
- **上游来源**: [dark-mode-testing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/dark-mode-testing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Dark Mode Testing

Verify that dark mode works correctly by toggling themes and comparing.

## Workflow

### 1. Open the App

Navigate to the target page using `browser_navigate`.

### 2. Screenshot Light Mode

Take a screenshot of the page in its default (light) state using `browser_take_screenshot`.

### 3. Toggle Dark Mode

Toggle dark mode using one of these methods (try in order):

1. **Class toggle**: Execute JS to add `dark` class to `<html>`:
   ```javascript
   document.documentElement.classList.toggle('dark')
   ```
2. **Attribute toggle**: Set `data-theme="dark"`:
   ```javascript
   document.documentElement.setAttribute('data-theme', 'dark')
   ```
3. **Media query**: Use browser to emulate `prefers-color-scheme: dark`
4. **UI toggle**: Find the theme toggle button in `browser_snapshot` and click it

### 4. Screenshot Dark Mode

Take another screenshot after toggling.

### 5. Inspect for Issues

Check the `browser_snapshot` aria tree and screenshots for:

- **White flashes**: Elements with hardcoded `bg-white` instead of `bg-white dark:bg-slate-900`
- **Invisible text**: Text color that matches the dark background (e.g. black text on dark bg)
- **Missing borders**: Borders using light-only colors that disappear on dark backgrounds
- **Contrast violations**: Text that's too low-contrast against the dark background (need 4.5:1)
- **Hardcoded colors**: Any `#ffffff`, `#000000`, `white`, `black` in inline styles
- **Images**: Logos or icons that don't have dark mode variants
- **Shadows**: Box shadows that are invisible on dark backgrounds
- **Form inputs**: Input fields that keep white backgrounds in dark mode

### 6. Report

```
Dark Mode Test:
  Light mode: OK
  Dark mode issues found:
    - Header logo: white logo invisible on dark bg (needs dark variant)
    - Card borders: border-gray-200 invisible on dark bg → add dark:border-gray-700
    - Footer text: hardcoded #333 → use text-gray-900 dark:text-gray-100
```

Fix each issue and re-test.
