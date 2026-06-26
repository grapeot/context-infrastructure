## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Run four parallel read-only subagents that each review the same diff from a different lens — security, performance, correctness, and readability — then merge findings into one report. Use before merging large or risky PRs.
- **上游来源**: [parallel-code-review](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/parallel-code-review)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Parallel Code Review

Use Cursor’s **Task** tool to run **four** `explore` (read-only) subagents at once. Each subagent only reads code and produces findings for one dimension. The main agent merges results into a single prioritized review — something only a multi-agent setup does efficiently.

## When to use

- Large diffs or refactors where a single pass misses categories.
- Security-sensitive changes (auth, payments, parsing untrusted input).
- Performance-sensitive paths (hot loops, N+1 queries, bundle entry points).

## Workflow

### 1. Scope the change set

Prefer a concrete list of files for reviewers:

```bash
git diff --name-only origin/main...HEAD
```

Or paste the PR link and let the main agent list changed files from the branch.

### 2. Launch four parallel subagents

Send **one message** with **four** Task invocations, each `subagent_type: "explore"` and **readonly: true**, with prompts like:

**Security**

```
Read-only review: SECURITY

Changed files:
<list>

Focus: injection (SQL, shell, XSS), authZ/authN gaps, secrets in code, unsafe deserialization, path traversal, SSRF, IDOR, dependency CVEs mentioned in diff.

Output:
- Critical / High / Medium / Low findings
- File:line and short fix recommendation
- "No issues" if nothing material
```

**Performance**

```
Read-only review: PERFORMANCE

Changed files:
<list>

Focus: N+1 queries, missing indexes, accidental O(n²) loops, bundle size impact, unnecessary re-renders, sync I/O on hot paths, unbounded caches.

Output: same severity + location format as above.
```

**Correctness**

```
Read-only review: CORRECTNESS

Changed files:
<list>

Focus: logic bugs, off-by-one, wrong edge cases, race conditions, error handling gaps, breaking API changes, test gaps for new behavior.

Output: same format.
```

**Readability / maintainability**

```
Read-only review: READABILITY

Changed files:
<list>

Focus: naming, duplication, abstraction boundaries, file size, unclear control flow, missing types/docs where they would prevent bugs.

Output: same format; prefer suggestions over nitpicks.
```

### 3. Synthesize

The main agent should:

1. De-duplicate findings that appear in multiple dimensions (count once, worst severity).
2. Order by severity, then by fix cost.
3. Produce a short executive summary (5 bullets max) and a table or list of actionable items.

### 4. Optional — address findings

Fix in the main agent or spawn targeted **non-readonly** follow-up tasks only for approved items.

## Notes

- Keep prompts **read-only** so parallel runs never fight over writes.
- If the diff is huge, split by directory and run four reviewers **per directory** in a second wave — do not cram unrelated megadiffs into one pass.
- This complements human review; it does not replace compliance or security sign-off for regulated environments.
