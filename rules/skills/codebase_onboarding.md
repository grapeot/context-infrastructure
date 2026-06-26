## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Launch multiple explore subagents in parallel to investigate architecture, data models, auth, APIs, and deployment. Synthesize into an onboarding document.
- **上游来源**: [codebase-onboarding](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/codebase-onboarding)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Codebase Onboarding

Generate a comprehensive onboarding document for a codebase by exploring it in parallel.

## Workflow

### 1. Launch Parallel Explorers

Spawn 5 `explore` subagents, each investigating a different area:

**Agent 1 — Architecture & Structure**
> "Map the top-level directory structure. Identify the framework (Next.js, Express, Django, etc.), monorepo tools (turbo, nx), and key config files. List every app/package and what it does."

**Agent 2 — Data Models & Database**
> "Find all database schemas, ORM models, migrations, and seed files. List every entity, its fields, and relationships. Identify the database (Postgres, MySQL, MongoDB, etc.) and ORM (Prisma, Drizzle, SQLAlchemy, etc.)."

**Agent 3 — API Routes & Endpoints**
> "Find all API route definitions. List every endpoint with its HTTP method, path, auth requirements, and what it does. Identify the API style (REST, GraphQL, tRPC)."

**Agent 4 — Authentication & Authorization**
> "Find how auth works. Identify the auth provider (Auth.js, Clerk, Supabase Auth, custom), session management, protected routes, role/permission checks, and middleware."

**Agent 5 — Deployment & Infrastructure**
> "Find deployment config (Dockerfile, Vercel config, fly.toml, terraform), CI/CD pipelines (GitHub Actions, etc.), environment variables needed, and how to run the app locally."

### 2. Synthesize

Combine the results from all 5 agents into a single onboarding document:

```markdown
# Codebase Onboarding

## Quick Start
1. Clone the repo
2. Install dependencies: `<command>`
3. Set up environment: copy `.env.example` to `.env`
4. Run database migrations: `<command>`
5. Start dev server: `<command>`

## Architecture
<Agent 1 findings>

## Data Models
<Agent 2 findings>

## API Reference
<Agent 3 findings>

## Authentication
<Agent 4 findings>

## Deployment
<Agent 5 findings>

## Key Files to Know
- `<file>` — <why it matters>
```

### 3. Save

Write the document to `ONBOARDING.md` in the project root, or wherever the user specifies.

## Tips

- Each explore agent is read-only and fast — the whole process takes under a minute
- For monorepos, consider one additional agent per app/package
- The document should be opinionated — highlight the "start here" files, not just list everything
- Include gotchas: common setup issues, env vars that are easy to forget, required system dependencies
