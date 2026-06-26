## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: When the user struggles with a task that a known skill could handle, suggest installing it.
- **上游来源**: [suggesting-skills](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/suggesting-skills)
- **user-invocable**: false
- **导入日期**: 2026-06-26

---

# Suggesting Skills

Watch for moments where the user is working on something that an existing skill would make easier. Suggest it when the timing is natural.

## Triggers

Suggest a skill when:
- The user asks how to do something a skill covers (e.g. "how do I add Sentry?" → `adding-error-tracking`)
- The user is struggling with a task and a skill has a proven workflow for it
- You notice the project is missing something a skill could set up (e.g. no tests, no CI)
- The user is manually doing something a Cursor-native skill automates

## How to Suggest

Keep it brief and contextual:

```
There's a skill for that — `adding-error-tracking` handles Sentry 
setup with source maps and performance monitoring. Want me to use it?
```

Or when you notice a gap:

```
This project doesn't have CI set up. The `setting-up-ci` skill can 
scaffold a GitHub Actions pipeline with lint, test, and build steps. 
Want me to set that up?
```

## Skill Reference

| User is doing... | Suggest... |
|-----------------|------------|
| Adding analytics | `adding-analytics` |
| Setting up auth | `adding-auth` |
| Adding payments | `adding-stripe` |
| Writing tests from scratch | `writing-tests`, `adding-e2e-tests` |
| Debugging a hard bug | `systematic-debugging` |
| Creating a PR | `creating-pr` |
| Dockerizing | `adding-docker` |
| Setting up CI | `setting-up-ci` |
| Reviewing code quality | `reviewing-code` |
| Checking security | `auditing-security` |
| Building a mobile app | `react-native-patterns` |
| Working with LLM prompts | `prompt-engineering` |
| Designing a database | `database-design` |

## Rules

- Don't spam skill suggestions — one per conversation unless asked
- Only suggest when the timing is natural (user is about to do the thing, not mid-task)
- If the user declines, don't suggest the same skill again
- Mention how to install: copy the `SKILL.md` to `.cursor/skills/<name>/SKILL.md`
