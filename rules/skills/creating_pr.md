## 元数据

- **类型**: Workflow
- **分类**: Workflow
- **适用场景**: Create a clean, review-ready pull request with a good title, structured description, linked issues, and appropriate reviewers.
- **上游来源**: [creating-pr](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/creating-pr)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Creating a PR

Package work into a pull request that's easy to review and merge.

## Workflow

### 1. Prepare the Branch

Before creating the PR:

```bash
# Ensure branch is up to date with base
git fetch origin
git rebase origin/main  # or merge, depending on project convention

# Check what will be in the PR
git log origin/main..HEAD --oneline
git diff origin/main --stat
```

Squash fixup commits if the project prefers clean history. Keep logical commits separate if the project prefers granular history.

### 2. Write the Title

Format: `<type>: <short description>`

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `chore` | Build, CI, deps, or tooling |
| `perf` | Performance improvement |

Examples:
- `feat: add dark mode toggle to settings page`
- `fix: prevent duplicate form submissions on checkout`
- `refactor: extract auth middleware into shared module`

### 3. Write the Description

Use this structure:

```markdown
## Summary

1-3 sentences explaining what this PR does and why.

Closes #123

## Changes

- Added `ThemeToggle` component with system/light/dark options
- Updated `Layout` to read theme from context
- Added theme persistence to localStorage

## Test Plan

- [ ] Toggle between light/dark/system themes
- [ ] Refresh page — theme persists
- [ ] Check no flash of unstyled content on load
```

### 4. Self-Review

Before requesting review:
- Read every line of the diff yourself
- Remove debug code (`console.log`, `TODO`, commented-out code)
- Verify tests pass: `npm test`
- Verify types: `npx tsc --noEmit`
- Verify lint: `npm run lint`
- Check for files that shouldn't be committed (`.env`, lockfile conflicts)

### 5. Create the PR

```bash
git push -u origin HEAD
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
...

## Changes
...

## Test Plan
...
EOF
)"
```

### 6. Request Review

- Tag the appropriate reviewers (code owners, domain experts)
- If the PR is large (>400 lines), add a comment explaining the best order to review files
- If the PR depends on another PR, note it in the description
- Label the PR appropriately (feature, bug, breaking change, etc.)

## Tips

- Small PRs get reviewed faster — aim for <300 lines changed
- If a PR is too big, split it into stacked PRs
- Screenshots/recordings for UI changes make review much faster
- Draft PRs are useful for early feedback before the work is complete
