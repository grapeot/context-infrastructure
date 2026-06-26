## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When the user keeps asking for the same check to run (lint, tests, type-check), suggest a Cursor hook to automate it.
- **上游来源**: [suggesting-cursor-hooks](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/suggesting-cursor-hooks)
- **user-invocable**: false
- **导入日期**: 2026-06-26

---

# Suggesting Cursor Hooks

Watch for repeated manual requests. When the user keeps asking you to run the same command after changes, suggest a hook to automate it.

## Triggers

Suggest a hook when you notice:
- The user asks you to **run the same check 2+ times** (e.g. "run lint", "run tests", "check types")
- The user says "always run X after editing" or "make sure to test after changes"
- You keep forgetting to run a validation step and the user catches it
- A CI failure could have been caught locally with a post-edit check

## How to Suggest

```
You've asked me to run [command] after edits a few times. Want me to 
set up a Cursor hook so it runs automatically?
```

If they say yes, create `.cursor/hooks.json` and the script:

```json
{
  "hooks": [
    {
      "event": "afterFileEdit",
      "script": ".cursor/hooks/<name>.sh",
      "pattern": "<glob>"
    }
  ]
}
```

## Common Hooks to Suggest

| User keeps asking... | Hook |
|---------------------|------|
| "run lint" / "fix formatting" | `afterFileEdit` → `eslint --fix` or `prettier --write` |
| "check types" | `afterFileEdit` → `tsc --noEmit` on `.ts`/`.tsx` |
| "run tests" | `afterFileEdit` → run related test file |
| "don't touch .env" | `beforeShellExecution` → warn on secrets files |
| "make sure it builds" | `stop` → quick build check |

## Rules

- Only suggest after a real repeated pattern, not preemptively
- Hook scripts must be fast (under 5 seconds) or the agent feels slow
- Scripts should exit 0 and report via stdout — don't block the agent unless the user explicitly wants that
- Check for existing `.cursor/hooks.json` first — merge, don't overwrite
- Keep it casual — "want me to automate this?" not a formal proposal
