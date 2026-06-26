## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When GitHub Actions fails, fetch failing job logs and assign each failing job to a separate subagent that fixes its slice of the problem in parallel. Use for multi-job CI failures where jobs are independent.
- **上游来源**: [parallel-ci-triage](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/parallel-ci-triage)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Parallel CI Triage

Speed up fixing broken CI by splitting failing **jobs** (or independent failure clusters) across parallel subagents. Each subagent owns one vertical slice: logs, root cause, code fix, and local verification for that slice.

## Prerequisites

- **GitHub CLI** (`gh`) installed and authenticated (`gh auth login`), or use the GitHub web UI / API to copy logs manually.
- Push access to the repo so fixes can be pushed and CI re-run.

## Workflow

### 1. Identify the failing run

From the repo root:

```bash
gh run list --limit 5
gh run view <RUN_ID> --log-failed
```

Or open the Actions tab, open the failed workflow run, and note which **jobs** failed (not just which step — group by job name).

If `gh` is unavailable, download logs from the GitHub UI and paste them into the conversation.

### 2. Split by job (or by failure cluster)

- **One subagent per failed job** when jobs test different things (e.g. `lint`, `test-node-18`, `e2e`).
- **One subagent per independent failure cluster** when a single job logs multiple unrelated errors — but prefer one job per agent to avoid conflicting edits in the same files.

If two failures share the same root cause in the same file, assign **one** subagent to fix both.

### 3. Launch parallel subagents

For each failing job, launch a `generalPurpose` subagent in a **single message** so they run concurrently:

```
Task: Fix CI failure for job "<JOB_NAME>"

Context:
- Workflow run: <RUN_URL or RUN_ID>
- Branch: <branch>
- Relevant log excerpt (failed steps only):
<paste gh run view --job <JOB_ID> --log or the failed section>

Instructions:
1. Infer the root cause from the log (command, stack trace, file:line).
2. Open and edit only what this job requires.
3. Run the same commands locally that failed in CI (or the narrowest equivalent, e.g. `npm run lint`, `pytest tests/foo`, `pnpm test --filter pkg`).
4. Report: what failed, what you changed, and confirmation that the local command passes.
```

Include the **exact** failing command and error lines so the subagent does not guess.

### 4. Merge and verify

- Collect each subagent’s changed files. Resolve overlaps manually if two agents touched the same file.
- Run the full CI-equivalent locally when possible:

  ```bash
  # Example: match your repo
  npm run lint && npm test
  ```

- Commit with a conventional message, push, and re-check the workflow:

  ```bash
  gh run watch
  ```

## When to use

- Multiple GitHub Actions jobs failed and the failures look independent.
- A long workflow log is easier to split by job than to fix sequentially.

## When not to use

- A single job with one clear error — fix it in the main agent.
- Failures that are purely flaky infrastructure — retry or fix workflow config first.

## Notes

- Redact secrets if pasting logs into chat.
- If agents conflict on shared files, merge sequentially after the parallel pass.
