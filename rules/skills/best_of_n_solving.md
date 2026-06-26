## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Solve a hard problem by trying multiple approaches in parallel using isolated git worktrees. Each attempt runs in its own branch, and the best solution is selected. Use for complex refactors, tricky bugs, or architectural decisions where multiple strategies could work.
- **上游来源**: [best-of-n-solving](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/best-of-n-solving)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Best-of-N Problem Solving

Use this skill when facing a hard problem with multiple possible approaches — complex refactors, tricky bugs, performance optimization, or architectural decisions where you're not sure which strategy will work best.

## How It Works

Cursor's `best-of-n-runner` subagent type creates isolated git worktrees — each attempt gets its own branch and working directory. Multiple approaches run in parallel without interfering with each other. You compare the results and pick the winner.

## Steps

1. **Identify the approaches** — before launching, define 2-3 distinct strategies. For example, if optimizing a slow database query:
   - Approach A: Add a composite index and rewrite the query
   - Approach B: Denormalize the schema with a materialized view
   - Approach C: Add application-level caching with Redis

2. **Launch parallel runners** — use the Task tool with `subagent_type: "best-of-n-runner"` for each approach. Launch them all in a single message so they run concurrently:

   ```
   Task 1: { subagent_type: "best-of-n-runner", prompt: "Approach A: ..." }
   Task 2: { subagent_type: "best-of-n-runner", prompt: "Approach B: ..." }
   Task 3: { subagent_type: "best-of-n-runner", prompt: "Approach C: ..." }
   ```

   Each runner gets its own branch and worktree. Include clear success criteria in the prompt (e.g., "run the tests and report if they pass", "measure the query time").

3. **Compare results** — when all runners complete, evaluate:
   - Which approach passes all tests?
   - Which has the cleanest implementation?
   - Which has the best performance characteristics?
   - Which is easiest to maintain long-term?

4. **Merge the winner** — check out the winning branch and merge it, or cherry-pick specific commits. Clean up the other worktree branches.

## When to Use This

- A bug that could have multiple root causes
- A refactor where you're choosing between patterns (e.g., composition vs. inheritance)
- Performance optimization with multiple strategies
- Trying different libraries or approaches for the same feature
- Any situation where "just try it" is faster than analyzing

## Notes

- Each runner is fully isolated — they can't see each other's changes.
- Keep prompts specific: include the file paths, the problem statement, and clear success criteria.
- For simpler problems, this is overkill — just use a single agent.
- The branches are real git branches, so you can inspect them manually if needed.
