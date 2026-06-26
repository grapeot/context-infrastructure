## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Automatically persist useful context — research, decisions, learnings, templates — to workspace files so knowledge survives across conversations.
- **上游来源**: [saving-workspace-context](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/saving-workspace-context)
- **user-invocable**: false
- **导入日期**: 2026-06-26

---

# Saving Workspace Context

You are an agent that builds institutional memory. As you work, watch for information that should outlast this conversation and save it to the workspace so future sessions start smarter.

## At the Start of Every Conversation

Load existing context before doing anything else:

1. Check for a `context/` directory — read any files relevant to the current task
2. Check for a product/project context file (e.g. `.agents/product-marketing-context.md`, `PROJECT.md`, or similar) for positioning, goals, and constraints
3. Check for any domain-specific directories the project uses (e.g. `companies/`, `docs/`, `research/`)
4. Check for templates or reusable assets that might apply

If the project doesn't have a `context/` directory yet, that's fine — create one when you first have something worth saving.

## During a Conversation

Watch for information that should be persisted. Save it as soon as you recognize it — don't wait until the end.

| Signal | Where to Save |
|---|---|
| Product details, positioning, ICP changes | Project context file (e.g. `.agents/product-marketing-context.md`) |
| Research on a company, person, or topic | `context/{topic-slug}.md` or a domain-specific directory |
| Strategy decisions or learnings | `context/{topic}.md` with dated entries |
| Reusable templates or boilerplate | `templates/` or a project-appropriate location |
| A repeatable multi-step workflow | New skill in `.cursor/skills/` or `.agents/skills/` |
| A persistent constraint or convention | New rule in `.cursor/rules/` |

### How to Save

- **Don't ask permission** for small context saves — just do it and mention what you saved
- **Do ask permission** before creating new skills or rules (they affect all future conversations)
- **Append, don't overwrite** when adding to existing context files — use dated entries
- **Use clear file names** — future you (or a future agent) needs to find this by scanning a directory listing

## At the End of a Conversation

Before finishing, ask yourself:

- Did I learn anything about this project that isn't captured in workspace files?
- Did I do research that would be painful to redo?
- Did I discover a pattern that should become a skill or rule?
- Did I create content that could be templated for reuse?

If yes to any, save it before the conversation ends.

## File Formats

### Context Files (`context/{slug}.md`)

```markdown
# {Topic}

## {Date} — {Brief title}

{What was learned, decided, or discovered}

## {Earlier date} — {Earlier entry}

{Previous context}
```

Keep entries reverse-chronological (newest first). Date your entries so they age gracefully.

### Project Context File

A single file capturing the current state of the project's identity:

```markdown
# {Project Name} — Context

- **What it is:** {one line}
- **Who it's for:** {target audience}
- **Key differentiator:** {why this vs alternatives}
- **Current stage:** {pre-launch / beta / growth / etc.}
- **Current goals:** {what matters right now}

## Positioning

{How we talk about the product}

## Constraints

{Things to always keep in mind}
```

## When to Create a New Skill

Create a skill when you find yourself doing the same multi-step workflow more than once:

- Researching a topic (check multiple sources, synthesize, save findings)
- Preparing for a meeting or call (pull context, recent history, prep talking points)
- Running a campaign or process (select targets, personalize, track progress)

## When to Create a New Rule

Create a rule when a persistent constraint should apply across all conversations:

- Voice/tone guidelines that get refined through feedback
- Naming conventions or file organization patterns
- Domain-specific constraints ("never mention X", "always check Y first")

## Rules

- Be proactive — save context without being asked, but mention what you saved
- Keep files scannable — future agents will skim directory listings to find context
- Don't save trivial information — if it's easily re-derived, skip it
- Date everything that accumulates over time
- Check for existing files before creating new ones to avoid duplicates
