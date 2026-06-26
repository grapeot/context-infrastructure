## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Monitor a build process (webpack, turbo, docker) for warnings and errors as they stream. Summarize issues and fix them before the build finishes.
- **上游来源**: [tailing-build-output](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/tailing-build-output)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Tailing Build Output

Watch a build process in real time via terminal files and fix issues as they appear.

## Workflow

### 1. Start or Find the Build

Either start the build yourself or find the terminal running it:

```bash
head -n 10 <terminals_folder>/*.txt
```

Look for commands like `npm run build`, `pnpm build`, `turbo build`, `docker build`, `tsc`, `vite build`.

### 2. Poll for Output

Read the terminal file periodically. Look for:

**Errors (fix immediately):**
- `ERROR` / `Error:` / `error TS`
- `Module not found` / `Cannot find module`
- `SyntaxError` / `TypeError`
- `Failed to compile`

**Warnings (collect for summary):**
- `WARNING` / `Warning:` / `warn`
- `Deprecation` / `deprecated`
- Unused imports/variables
- Large bundle size warnings (`asset size limit`)

**Progress indicators:**
- Webpack: `[XX%]`, `modules`, `chunks`
- Turbo: task completion logs
- Docker: `Step X/Y`
- TypeScript: file count

### 3. Fix Errors in Flight

When an error appears:
1. Extract the file path and line number from the error
2. Read and fix the source file
3. If the build supports watch mode, it will re-trigger automatically
4. If not, note the fix and let the build continue — it may reveal more errors

### 4. Summary Report

After the build completes (check for `exit_code` in terminal footer):

```
Build Summary:
  Status: Failed (exit code 1) / Succeeded
  Duration: ~45s
  Errors fixed: 3
  Remaining warnings: 2
    - Large bundle: src/pages/Dashboard.tsx (450kb)
    - Deprecated API: useRouter from 'next/router'
```

## Tips

- Don't fix warnings during the build — collect them and address after
- For `turbo build`, errors may appear in parallel task output — check all task logs
- Docker builds cache layers — if you fix a file early in the Dockerfile, later layers rerun
- TypeScript's `--noEmit` is useful for type-checking without a full build
