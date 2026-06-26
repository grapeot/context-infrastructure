## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When the same multi-step workflow repeats in Cursor (user corrections or agent redos), capture it as a new SKILL.md under .cursor/skills/ so future sessions load it automatically.
- **上游来源**: [building-skills-from-patterns](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/building-skills-from-patterns)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Building Skills From Patterns

**Skills** are reusable `SKILL.md` files. This meta-skill tells the agent to **promote repeated muscle memory** into a named skill: research once, encode the workflow, reuse forever.

## When to trigger

- The user has asked for the **same sequence** three or more times (e.g. “always run lint then tsc then test before commit”).
- The agent notices it is **re-deriving** the same steps on every task in this repo (e.g. “how we deploy preview branches”).
- A correction sounds like a **policy** (“never use raw SQL here — always the repository layer”) — pair with `suggesting-cursor-rules` if it should be always-on; use a **skill** if it is a procedure with steps.

## Workflow

### 1. Name the pattern

Choose a short **slug** (lowercase, hyphens): `verifying-api-before-merge`, `releasing-mobile-build`, etc.

### 2. Draft `SKILL.md`

Create `.cursor/skills/<slug>/SKILL.md` (or in this repo’s pattern, copy from `resources/<slug>/SKILL.md` when contributing upstream).

Frontmatter:

```yaml
---
name: <slug>
description: One line: what it does and when to use it. Ends with a clear trigger.
user-invocable: true   # optional, if the user should be able to invoke by name
---
```

Body sections (keep lean):

1. **Title** — human-readable.
2. **When to use** — bullets.
3. **Steps** — numbered, imperative, tool names where useful (`npm`, `gh`, MCP tools).
4. **Notes** — edge cases, safety, when **not** to use.

Match the tone of other skills in the repo: concrete commands, no filler.

### 3. Validate

- **Description** is specific enough for Cursor to **match** the skill when the user describes the task.
- Steps are **executable** by an agent without guessing repo layout (or say “detect package manager from lockfile”).
- No secrets or machine-specific paths.

### 4. Point the user to it

Tell the user where the file lives and that the agent will pick it up on the next chat in that workspace.

## Relationship to rules and hooks

| Mechanism | Use for |
|----------|---------|
| **Skill** | On-demand procedure, branching steps, tool usage. |
| **Rule** (`.cursor/rules/`) | Always-on conventions, style, file patterns. |
| **Hook** (`.cursor/hooks.json`) | Automate after file save / stop events. |

If the pattern is “every time I save, run X,” suggest a **hook** instead. If it is “when I ask to ship,” keep it as a **skill**.

## Notes

- Prefer **one skill per workflow** — avoid megaskills that try to cover every situation.
- Update an existing skill instead of adding a duplicate if the workflow evolves.
