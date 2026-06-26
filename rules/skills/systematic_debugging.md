## 元数据

- **类型**: Workflow
- **分类**: Workflow
- **适用场景**: Structured debugging methodology — reproduce, isolate, hypothesize, verify. Covers git bisect, binary search, logging, and minimal reproduction.
- **上游来源**: [systematic-debugging](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/systematic-debugging)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Systematic Debugging

Debug methodically instead of randomly changing code.

## The Process

### 1. Reproduce

Before anything else, reproduce the bug reliably:
- Get the exact steps to trigger the issue
- Note the expected vs actual behavior
- Confirm it happens consistently (not intermittent)
- Record the environment (OS, Node version, browser, etc.)

If you can't reproduce it, you can't fix it. Ask for more details.

### 2. Isolate

Narrow down where the bug lives:

**Binary search the codebase:**
- Comment out half the system → does the bug persist?
- If yes, the bug is in the remaining half → repeat
- If no, the bug is in the commented-out half → repeat

**Git bisect:**
```bash
git bisect start
git bisect bad          # current commit is broken
git bisect good <sha>   # this commit was working
# Git checks out the midpoint — test it
git bisect good         # or git bisect bad
# Repeat until it finds the first bad commit
git bisect reset        # when done
```

**Isolate by layer:**
- Is it frontend or backend? (Check network tab)
- Is it the database? (Query directly)
- Is it the API? (curl the endpoint)
- Is it the component? (Render it in isolation)

### 3. Hypothesize

Form a specific, testable hypothesis:
- "The bug is caused by X because Y"
- Not "something is wrong with the data"
- Good: "The `userId` is null because the auth middleware doesn't run on this route"

### 4. Test the Hypothesis

Write the smallest possible test that proves/disproves your hypothesis:
- Add a `console.log` or breakpoint at the suspected location
- Check the value of the suspected variable
- If your hypothesis is wrong, go back to step 3 with new information
- If it's right, you've found the bug

### 5. Fix and Verify

- Apply the minimal fix
- Verify the original reproduction steps no longer trigger the bug
- Check for regressions — did the fix break anything else?
- Write a test that would have caught this bug

## Debugging Tools

| Scenario | Tool |
|----------|------|
| "It worked before" | `git bisect` |
| "I don't know where this runs" | Add logging at entry/exit of suspect functions |
| "The data looks wrong" | Inspect at each transformation step |
| "It only fails in production" | Compare env vars, check logs, try to reproduce with prod data locally |
| "It's intermittent" | Look for race conditions, timing issues, or uninitialized state |
| "The error message is useless" | Search the codebase for where that error is thrown |

## Common Bug Patterns

- **Off-by-one**: Array indices, pagination, date ranges
- **Null/undefined**: Missing optional chaining, uninitialized state
- **Race condition**: Async operations completing in unexpected order
- **Stale closure**: React useEffect/useCallback capturing old values
- **Type coercion**: `==` vs `===`, string vs number comparisons
- **Missing await**: Forgetting `await` on async functions
- **Environment mismatch**: Works locally, fails in CI/prod due to different env vars or versions

## Rules

- Never guess — always verify with evidence
- Fix the root cause, not the symptom
- If you've spent 15 minutes without progress, step back and re-isolate
- Document what you tried so you don't repeat failed approaches
