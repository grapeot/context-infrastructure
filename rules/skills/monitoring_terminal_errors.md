## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Watch running terminal processes for crashes and stack traces. When an error appears, navigate to the failing file and line, diagnose, and fix it automatically.
- **上游来源**: [monitoring-terminal-errors](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/monitoring-terminal-errors)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Monitoring Terminal Errors

Continuously watch a running process (dev server, test runner, build) for errors and fix them as they appear.

## Workflow

### 1. Identify the Terminal

List terminal files and find the one running the target process:

```bash
head -n 10 <terminals_folder>/*.txt
```

Look for terminals running dev servers (`npm run dev`, `pnpm dev`, `python manage.py runserver`, etc.).

### 2. Read Terminal Output

Read the full terminal file content. Search for error patterns:

- **Stack traces**: `at <function> (<file>:<line>:<col>)`
- **Node.js**: `Error:`, `TypeError:`, `ReferenceError:`, `ENOENT`, `ECONNREFUSED`
- **Python**: `Traceback (most recent call last):` followed by `File "<path>", line <n>`
- **React/Next.js**: `Unhandled Runtime Error`, `Error: ...`, `Module not found`
- **Build errors**: `ERROR in`, `Failed to compile`, `SyntaxError`
- **Vite**: `[vite] Internal server error:`
- **TypeScript**: `error TS\d+:`

### 3. Extract the Source Location

From the stack trace, extract:
- File path
- Line number
- Error message

For Node.js: `at functionName (/path/to/file.ts:42:10)`
For Python: `File "/path/to/file.py", line 42, in function_name`

### 4. Navigate and Fix

1. Read the identified file around the error line
2. Understand the error (missing import, type mismatch, undefined variable, etc.)
3. Apply the fix
4. Re-read the terminal file to confirm the server recovered (hot reload should pick it up)

### 5. Loop

If the server is still showing errors after the fix, repeat from step 2. Stop when:
- The terminal shows a clean "compiled successfully" or equivalent
- No new errors appear in the output
- You've made 5 attempts without resolution (report to user)

## Tips

- Check for `exit_code` in the terminal file footer — if present, the process has crashed entirely and needs a restart
- Some errors cascade — fix the first/root error and the rest often disappear
- For HMR errors, the fix might just be saving the file again to trigger a rebuild
