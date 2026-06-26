## 元数据

- **类型**: Workflow
- **分类**: Dependencies
- **适用场景**: Safely update an npm package by checking npmjs.com for the latest version, reading release notes, and handling minor vs major upgrades differently. For minor updates, just do it. For major updates, find the upgrade guide, validate breaking changes, and produce a detailed migration report.
- **上游来源**: [updating-npm-package](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/updating-npm-package)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Updating an npm Package

Use this skill when the user asks to update, upgrade, or bump a specific npm dependency.

## Steps

1. **Check the current version** — read `package.json` to find the installed version:

   ```bash
   npm ls <package-name>
   ```

2. **Find the latest version on npm** — fetch the package info:

   ```bash
   npm view <package-name> versions --json
   npm view <package-name> dist-tags --json
   ```

   This gives you the `latest` tag and all published versions.

3. **Determine the update type** — compare current version to latest:
   - **Patch** (1.2.3 → 1.2.4): bug fixes only
   - **Minor** (1.2.3 → 1.3.0): new features, backwards compatible
   - **Major** (1.2.3 → 2.0.0): breaking changes

4. **For patch or minor updates** — just do it:

   ```bash
   npm install <package-name>@latest
   ```

   Run the build and tests to make sure nothing broke:

   ```bash
   npm run build && npm test
   ```

   If everything passes, commit and report what changed.

5. **For major updates** — do a thorough investigation first:

   a. **Fetch the changelog and release notes** — check the package's GitHub repo for `CHANGELOG.md`, `MIGRATION.md`, or release notes. Use the web to find the official upgrade guide:

   ```
   Search: "<package-name> v<major> migration guide" OR "<package-name> v<major> upgrade guide"
   ```

   b. **Read the breaking changes** — identify every breaking change between the current and target version. Common things to check:
   - Removed or renamed APIs
   - Changed function signatures or return types
   - Dropped Node.js version support
   - New peer dependency requirements
   - Changed default behavior
   - Config file format changes

   c. **Scan the codebase for impact** — search for every usage of the package:

   ```bash
   # Find all imports
   grep -r "from ['\"]<package-name>" src/
   grep -r "require(['\"]<package-name>" src/
   ```

   For each usage, check if it's affected by a breaking change.

   d. **Apply the update**:

   ```bash
   npm install <package-name>@latest
   ```

   e. **Fix breaking changes** — update each affected usage based on the migration guide. Apply changes file by file.

   f. **Verify** — run the full suite:

   ```bash
   npm run lint && npx tsc --noEmit && npm test && npm run build
   ```

   g. **Produce a migration report** — summarize:

   ```markdown
   ## Package Update: <package-name> v<old> → v<new> (Major)

   ### Breaking Changes Applied
   - `oldFunction()` renamed to `newFunction()` — updated in 3 files
   - Config format changed from `.js` to `.config.ts` — migrated
   - Dropped support for Node 16 — verified we're on Node 20

   ### Files Modified
   - src/lib/client.ts — updated import and function call
   - src/config/settings.ts — migrated config format
   - package.json — bumped version

   ### Validation
   - ✅ Lint passes
   - ✅ TypeScript compiles
   - ✅ All 47 tests pass
   - ✅ Build succeeds
   ```

## Notes

- Always check peer dependency compatibility before updating — `npm install` will warn about mismatches.
- For monorepos, check if the package is used in multiple workspaces and update them all together.
- If the package has a codemod tool (e.g. `npx @next/codemod`), use it instead of manual migration.
- Lock file (`package-lock.json`) changes are expected — commit them with the update.
