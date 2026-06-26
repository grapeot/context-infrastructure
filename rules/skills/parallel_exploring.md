## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Explore a large codebase in parallel by launching multiple explore subagents that each investigate a different area simultaneously. Use when onboarding onto a new project, understanding architecture, or investigating a cross-cutting concern.
- **上游来源**: [parallel-exploring](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/parallel-exploring)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Parallel Explore

Use this skill when you need to understand a large or unfamiliar codebase quickly — onboarding onto a new project, investigating how a feature works across layers, or mapping the architecture.

## How It Works

Cursor's `explore` subagent is a fast, read-only agent optimized for searching and reading code. You can launch multiple explore agents in a single message and they run concurrently, each investigating a different area.

## Steps

1. **Identify the areas to explore** — break the codebase into logical zones. For a typical full-stack app:
   - Frontend: components, pages, routing, state management
   - Backend: API routes, database models, middleware, auth
   - Infrastructure: CI/CD, Docker, deployment config
   - Shared: types, utilities, constants

2. **Launch parallel explore agents** — use the Task tool with `subagent_type: "explore"` for each area. Launch them all in one message:

   ```
   Task 1: "Explore the frontend — find the main pages, routing setup, state management approach,
            and UI component library. Check src/app/, src/components/, src/pages/. Report the
            framework, router, styling approach, and key components."

   Task 2: "Explore the backend — find the API routes, database setup, ORM, auth middleware,
            and data models. Check src/server/, src/api/, lib/, prisma/. Report the framework,
            database, auth strategy, and key endpoints."

   Task 3: "Explore the infrastructure — find CI/CD config, Docker setup, deployment targets,
            and environment variable management. Check .github/, docker*, *.config.*, .env*.
            Report the deploy target, CI provider, and any IaC."
   ```

3. **Synthesize the results** — when all agents return, combine their findings into a coherent picture:
   - Tech stack summary (frontend, backend, database, infra)
   - Architecture diagram (describe the data flow)
   - Key files and entry points
   - Potential concerns or tech debt

## Other Use Cases

- **Cross-cutting investigation**: "Where is user authentication checked?" — launch agents to search the frontend (route guards), backend (middleware), and database (session storage) simultaneously.
- **Dependency audit**: launch agents to check different parts of the dependency tree for outdated packages, security issues, and unused imports.
- **Migration planning**: have agents simultaneously assess the frontend, backend, and tests to estimate the scope of a framework migration.

## Notes

- Explore agents are read-only — they can't modify files.
- Use `thoroughness: "very thorough"` in the prompt for comprehensive analysis.
- Each agent has its own context window, so they can each read many files without running out of space.
- For a single focused question, just use Grep or SemanticSearch directly — subagents are for broad exploration.
