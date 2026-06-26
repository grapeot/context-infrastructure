## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Run TypeScript type checking after file edits and immediately flag type errors before moving on. Uses Cursor hooks for automatic enforcement.
- **上游来源**: [auto-type-checking](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/auto-type-checking)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Auto Type Checking

Catch type errors immediately after every edit instead of discovering them at build time.

## Manual Workflow

After editing a TypeScript file, run:

```bash
npx tsc --noEmit 2>&1 | head -30
```

If errors appear, fix them before moving on.

## Automated with Cursor Hooks

Add to `.cursor/hooks.json` to run automatically after every file edit:

```json
{
  "hooks": [
    {
      "event": "afterFileEdit",
      "script": "check-types.sh",
      "pattern": "**/*.{ts,tsx}"
    }
  ]
}
```

Create `.cursor/hooks/check-types.sh`:

```bash
#!/bin/bash
# Quick type check — only reports errors, doesn't block
npx tsc --noEmit --pretty 2>&1 | head -20
exit 0  # Don't block the agent even if there are errors
```

```bash
chmod +x .cursor/hooks/check-types.sh
```

## What to Check

When type errors appear:

1. **Missing imports**: `Cannot find name 'X'` → add the import
2. **Type mismatches**: `Type 'string' is not assignable to type 'number'` → fix the type or the value
3. **Missing properties**: `Property 'x' does not exist on type 'Y'` → add the property to the interface or fix the access
4. **Null safety**: `Object is possibly 'null'` → add null check or optional chaining
5. **Generic constraints**: `Type 'X' does not satisfy the constraint 'Y'` → fix the generic parameter

## Tips

- Use `--noEmit` to type-check without producing output files
- For large projects, `tsc` can be slow — consider `--incremental` or running only on changed files
- If using path aliases, ensure `tsconfig.json` paths are configured correctly
- For monorepos, run `tsc` from the package root, not the workspace root
- Pair with `grinding-until-pass` for a full "fix until clean" loop
