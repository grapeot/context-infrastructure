## 元数据

- **类型**: Workflow
- **分类**: Code Quality & Security
- **适用场景**: Perform a thorough code review focused on correctness, maintainability, performance, and best practices.
- **上游来源**: [reviewing-code](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/reviewing-code)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Code Review

Use this skill when the user asks for a code review, feedback on their code, or to check code quality.

## Steps

1. **Understand the change** — read the files or diff to understand what the code is supposed to do. Identify the scope (new feature, bug fix, refactor).

2. **Check correctness**
   - Does the code handle edge cases (empty input, null, zero, negative numbers)?
   - Are error states handled (try/catch, error boundaries, fallback UI)?
   - Does async code handle race conditions, cancellation, and timeouts?
   - Are there off-by-one errors in loops or array access?

3. **Check maintainability**
   - Are functions focused on a single responsibility?
   - Are variable and function names descriptive?
   - Is there unnecessary duplication that should be extracted?
   - Are magic numbers replaced with named constants?
   - Is the code complexity reasonable (deeply nested conditionals, long functions)?

4. **Check performance**
   - Are there N+1 query patterns in database access?
   - Are expensive computations or API calls happening in render loops?
   - Are large lists missing virtualization or pagination?
   - Are there missing indexes for common database queries?
   - Is memoization used appropriately (not over-applied)?

5. **Check type safety** (TypeScript projects)
   - Are there `any` types that should be narrowed?
   - Are function return types explicit for public APIs?
   - Are union types handled exhaustively?

6. **Check testing**
   - Are there tests for the new/changed code?
   - Do tests cover the happy path AND error cases?
   - Are tests isolated (no shared mutable state)?

7. **Provide feedback** — organize findings by severity:
   - **Must fix**: bugs, security issues, data loss risks
   - **Should fix**: performance issues, maintainability concerns
   - **Nit**: style preferences, minor suggestions

   For each finding, include the file, line, the issue, and a suggested fix.

## Notes

- Be constructive — explain *why* something is a problem, not just that it is.
- Acknowledge what's done well, not just what needs fixing.
- Don't bikeshed on style issues that a linter/formatter should handle.
