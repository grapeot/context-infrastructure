## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When multiple tests fail, assign each failing test file to a separate subagent that fixes it independently in parallel.
- **上游来源**: [parallel-test-fixing](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/parallel-test-fixing)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Parallel Test Fixing

Speed up fixing a broken test suite by distributing failing tests across parallel subagents.

## Workflow

### 1. Run the Full Test Suite

```bash
npm test -- --no-coverage 2>&1 || true
```

Capture the output and extract all failing test files.

### 2. Group Failures

Parse the test output for failing files:
- Jest: `FAIL src/components/Button.test.tsx`
- Vitest: `FAIL src/utils/format.test.ts`
- Pytest: `FAILED tests/test_api.py::test_create_user`

Group by file — each file becomes one task.

### 3. Launch Parallel Subagents

For each failing test file, launch a `generalPurpose` subagent:

```
Task: Fix the failing tests in <file>

The test file is: <path>
The test command is: <command to run just this file>
The error output was:
<paste the relevant failure output>

Steps:
1. Read the test file and the source file it tests
2. Understand why each test is failing
3. Fix the source code (preferred) or update the test if the test is wrong
4. Run the single test file to confirm it passes
5. Report what you changed and why
```

Launch all subagents simultaneously — they work in parallel since each touches different files.

### 4. Collect Results

As each subagent completes, collect:
- Which tests were fixed
- What files were changed
- Whether the fix might conflict with another subagent's changes

### 5. Verify

Run the full test suite one more time to confirm everything passes:

```bash
npm test
```

If there are new failures (from conflicting fixes), resolve them sequentially.

## Tips

- If two failing tests share the same source file, assign them to the same subagent to avoid edit conflicts
- Set a timeout — if a subagent is stuck for 5+ minutes, check its progress
- For large test suites (50+ failures), batch into groups of 5-10 per subagent rather than one-per-file
- Use `best-of-n-runner` subagents if you want isolated worktrees for each fix attempt
