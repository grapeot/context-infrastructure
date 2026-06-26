## 元数据

- **类型**: Workflow
- **分类**: Infrastructure & DevOps
- **适用场景**: Set up a GitHub Actions CI/CD pipeline with linting, testing, type-checking, and deployment steps.
- **上游来源**: [setting-up-ci](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/setting-up-ci)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Setup CI (GitHub Actions)

Use this skill when the user asks to set up CI, continuous integration, a build pipeline, or GitHub Actions.

## Steps

1. **Detect the project structure** — check for `package.json` (Node.js), `requirements.txt` / `pyproject.toml` (Python), `go.mod` (Go), or monorepo tools like Turborepo.

2. **Create `.github/workflows/ci.yml`**

   For a Node.js project:

   ```yaml
   name: CI

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: npm
         - run: npm ci
         - run: npm run lint
         - run: npm run typecheck
         - run: npm test
         - run: npm run build
   ```

3. **Add type-checking** — if `typecheck` script doesn't exist in `package.json`, add `"typecheck": "tsc --noEmit"`.

4. **Add caching** — the `actions/setup-node` `cache` option handles `node_modules`. For monorepos with Turborepo, add remote caching or `actions/cache` for `.turbo`.

5. **Add matrix testing (optional)** — if the user needs to test across Node versions or OS:

   ```yaml
   strategy:
     matrix:
       node-version: [18, 20, 22]
   ```

6. **Add deployment step (optional)** — if requested, add a deploy job that runs only on `main` pushes, gated by the build job succeeding:

   ```yaml
   deploy:
     needs: build
     if: github.ref == 'refs/heads/main'
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v4
       - run: npm ci && npm run build
       - run: npx vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
   ```

7. **Add status badge** — add the workflow status badge to the project README:

   ```markdown
   ![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
   ```

## Notes

- Keep CI fast — run lint and typecheck in parallel using separate jobs if the pipeline is slow.
- Use `npm ci` (not `npm install`) for deterministic installs.
- Store secrets (API keys, deploy tokens) in GitHub repository settings, never in the workflow file.
