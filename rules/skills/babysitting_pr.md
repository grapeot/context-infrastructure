## 元数据

- **类型**: Workflow
- **分类**: Workflow
- **适用场景**: Monitor a pull request for CI failures, review comments, and merge conflicts — then fix them automatically. Use when a PR is open and you want the agent to keep it merge-ready.
- **上游来源**: [babysitting-pr](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/babysitting-pr)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Babysitting a PR

Use this skill when the user has an open pull request and wants the agent to monitor it, fix CI failures, resolve review comments, and keep it merge-ready.

## Steps

1. **Get the PR status** — fetch the current state of the PR:

   ```bash
   gh pr view --json number,title,state,mergeable,reviewDecision,statusCheckRollup,comments,reviews
   ```

   Also check for merge conflicts:

   ```bash
   gh pr view --json mergeStateStatus
   ```

2. **Check CI status** — look at the `statusCheckRollup` field. For each failing check:

   ```bash
   gh pr checks
   ```

   This lists all CI checks and their status (pass/fail/pending).

3. **Fix CI failures** — for each failing check, get the logs:

   ```bash
   gh run view <run-id> --log-failed
   ```

   Analyze the failure and fix it:

   - **Lint failures**: run the linter locally (`npm run lint -- --fix`), fix remaining issues manually, commit.
   - **Type errors**: run `npx tsc --noEmit`, read the errors, fix the types, commit.
   - **Test failures**: run the failing test suite locally, read the assertion errors, fix the code or update the test expectations, commit.
   - **Build failures**: run `npm run build`, read the error output, fix imports/configs/missing deps, commit.

   After fixing, push the changes:

   ```bash
   git add -A && git commit -m "fix: resolve CI failures" && git push
   ```

4. **Handle review comments** — fetch PR review comments:

   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/comments
   ```

   For each unresolved comment:
   - Read the comment and the code it references.
   - If the fix is clear (typo, naming, missing null check, style issue), apply it.
   - If the comment requires a design decision or clarification, skip it and report to the user.

   Commit fixes for resolved comments:

   ```bash
   git add -A && git commit -m "fix: address review feedback" && git push
   ```

5. **Resolve merge conflicts** — if the PR has conflicts:

   ```bash
   git fetch origin main
   git merge origin/main
   ```

   Resolve conflicts by reading both sides and choosing the correct resolution. For ambiguous conflicts, ask the user. After resolving:

   ```bash
   git add -A && git commit -m "fix: resolve merge conflicts" && git push
   ```

6. **Re-check status** — after pushing fixes, wait for CI to run and check again:

   ```bash
   gh pr checks --watch
   ```

   If new failures appear, go back to step 3. Limit to 3 rounds to avoid infinite loops.

7. **Report** — summarize what was done:
   - Which CI checks were failing and how they were fixed
   - Which review comments were addressed
   - Whether merge conflicts were resolved
   - Current PR status (ready to merge, or what's still blocking)

## Loop Behavior

This skill is designed to run in a loop:

```
Check PR → Find issues → Fix issues → Push → Re-check → Repeat
```

Stop when:
- All checks pass, no unresolved comments, no conflicts → PR is merge-ready
- 3 fix-push-check cycles have been attempted without full resolution → report what's still failing
- A fix requires a design decision → ask the user

## Notes

- Never force-push to a shared PR branch.
- Don't modify test assertions to make tests pass unless the behavior change was intentional.
- Don't resolve review comments you're unsure about — skip them and let the user know.
- If CI is queued/pending, wait for it to complete before analyzing failures.
- Use `gh pr ready` to mark the PR as ready for review once everything is green.
