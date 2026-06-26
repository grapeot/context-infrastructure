## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Keep iterating on code changes until the tests pass, the build succeeds, or linting is clean. Runs in a tight loop of fix → run → check → repeat. Use when you want the agent to autonomously grind through test failures or build errors.
- **上游来源**: [grinding-until-pass](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/grinding-until-pass)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Grind Until Pass

Use this skill when you want the agent to keep working autonomously until a specific goal is met — all tests pass, the build succeeds, or linting is clean. Instead of stopping after one attempt, the agent loops until done.

## Steps

1. **Define the goal command** — the command whose exit code determines success:

   - Tests: `npm test` or `npx vitest run`
   - Build: `npm run build`
   - Lint: `npm run lint`
   - Type-check: `npx tsc --noEmit`
   - All of the above: `npm run lint && npx tsc --noEmit && npm test && npm run build`

2. **Run the command** — execute it and capture the output.

3. **If it fails — analyze and fix**:
   - Read the error output carefully.
   - Identify the root cause: failing test assertion, type error, lint violation, import error, etc.
   - Make the minimal fix. Don't refactor — just fix the error.
   - Go back to step 2.

4. **If it passes — stop and report**:
   - Report what was fixed and how many iterations it took.
   - Summarize the changes made.

## Rules for the Loop

- **Maximum 10 iterations** — if after 10 attempts the command still fails, stop and report what's blocking progress. Something fundamental is wrong and needs human input.
- **Fix one thing at a time** — don't try to fix all errors at once. Fix the first error, re-run, and see if the fix resolves downstream errors too.
- **Don't delete tests** — if a test is failing, fix the code to make it pass. Don't modify the test unless the test itself is clearly wrong (testing old behavior that was intentionally changed).
- **Don't suppress errors** — don't add `@ts-ignore`, `eslint-disable`, or `any` types to silence errors. Fix the actual problem.
- **Track progress** — if the number of errors is increasing instead of decreasing, stop and reassess the approach.

## When to Use This

- After a large refactor that broke multiple tests
- After upgrading a dependency that introduced type errors
- After merging a branch with conflicts that need resolution
- When you want to "just make it green" and trust the agent to grind through it

## Advanced: Cursor Hooks Integration

You can automate this with a Cursor hook in `.cursor/hooks.json` that triggers after the agent's turn ends, checks if tests pass, and sends a follow-up message if they don't:

```json
{
  "hooks": [
    {
      "event": "stop",
      "command": "bash .cursor/scripts/check-tests.sh",
      "description": "Re-run tests after agent stops and send follow-up if failing"
    }
  ]
}
```

The script checks the exit code and returns a `followup_message` if tests are still failing.

## Notes

- This works best with fast test suites. If your tests take 5+ minutes, the loop will be slow.
- Use `--bail` or `--fail-fast` flags to stop at the first failure for faster iteration.
- The agent will be thorough but not creative — if the fix requires a design change, it'll need human guidance.
