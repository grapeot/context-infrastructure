## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Check out two branches in separate worktrees, start both dev servers on different ports, screenshot the same pages, and produce a visual diff.
- **上游来源**: [comparing-branches-visually](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/comparing-branches-visually)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Comparing Branches Visually

Create a visual before/after comparison of UI changes between two branches.

## Workflow

### 1. Set Up Two Worktrees

Use `best-of-n-runner` subagents or git worktrees to run both branches simultaneously:

```bash
# Create a worktree for the base branch
git worktree add /tmp/branch-compare-base main

# The current working directory has the feature branch
```

### 2. Start Both Servers

Start the base branch server on a different port:

```bash
# In the base worktree
cd /tmp/branch-compare-base && PORT=3001 npm run dev

# Current branch is already on the default port (3000)
```

### 3. Identify Pages to Compare

Determine which pages are affected by the changes:

```bash
git diff main --name-only | grep -E '\.(tsx?|jsx?|vue|svelte|css)'
```

Map changed files to their routes (e.g. `app/dashboard/page.tsx` → `/dashboard`).

### 4. Screenshot Both Versions

For each affected page:

1. `browser_navigate` to `http://localhost:3001/<page>` (base branch)
2. `browser_take_screenshot` → save as "before"
3. `browser_navigate` to `http://localhost:3000/<page>` (feature branch)
4. `browser_take_screenshot` → save as "after"

### 5. Report

Present the comparison:

```
Visual Diff: feature/redesign-header vs main

/dashboard:
  Before: [screenshot from main]
  After:  [screenshot from feature branch]
  Changes: Header height reduced, nav links repositioned, new avatar dropdown

/settings:
  Before: [screenshot]
  After:  [screenshot]
  Changes: No visual differences detected
```

### 6. Clean Up

```bash
# Stop the base branch server
# Remove the worktree
git worktree remove /tmp/branch-compare-base
```

## Tips

- Test at a consistent viewport size (1280×800 is a good default)
- For mobile-first changes, also compare at 375px width
- If the app requires auth, log in on both ports first
- This pairs well with `screenshotting-changelog` for PR descriptions
