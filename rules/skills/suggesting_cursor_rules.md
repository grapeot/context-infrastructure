## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When the user repeats the same correction or convention multiple times, suggest a Cursor rule to encode it permanently.
- **上游来源**: [suggesting-cursor-rules](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/suggesting-cursor-rules)
- **user-invocable**: false
- **导入日期**: 2026-06-26

---

# Suggesting Cursor Rules

Watch for repeated corrections and frustration. When the user keeps telling you the same thing, suggest a `.cursor/rules/` file so they never have to say it again.

## Triggers

Suggest a rule when you notice:
- The user corrects the same pattern **2+ times** (e.g. "use named exports", "don't use default exports")
- The user expresses frustration about code style or conventions
- The user says things like "I always want...", "never do...", "every time you..."
- You keep making the same mistake in this project

## How to Suggest

When you detect a trigger, offer it naturally:

```
I notice you've corrected me on [pattern] a couple times. Want me to 
create a Cursor rule so I always follow this convention?
```

If they say yes, create the rule:

```
.cursor/rules/<name>.mdc
```

```
---
description: <what this rule enforces>
globs: <file pattern this applies to>
---

- <the convention, stated clearly>
```

## Examples

**User keeps saying "use relative imports":**
```
---
description: Import conventions
globs: **/*.{ts,tsx}
---

- Use relative imports, not @ aliases
- Import from the same package with relative paths (e.g. "../../queries/..." not "src/queries/...")
```

**User keeps saying "no comments on obvious code":**
```
---
description: Comment style
globs: **/*.{ts,tsx,js,jsx}
---

- Do not add comments that narrate what the code does
- Only comment non-obvious intent, tradeoffs, or constraints
```

**User frustrated about test file locations:**
```
---
description: Test file conventions
globs: **/*.test.{ts,tsx}
---

- Co-locate test files next to the source file they test
- Name test files <source>.test.ts, not __tests__/<source>.ts
```

## Rules

- Don't be annoying — only suggest after a genuine repeated pattern, not on the first correction
- Keep rule files small and focused — one concern per file
- Check `.cursor/rules/` first so you don't duplicate an existing rule
- Frame it as a helpful offer, not a lecture
