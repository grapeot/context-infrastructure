## 元数据

- **类型**: Workflow
- **分类**: Workflow
- **适用场景**: Write clear, conventional commit messages with proper type prefixes, scopes, and body content.
- **上游来源**: [writing-commit-messages](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/writing-commit-messages)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Writing Commit Messages

Write commit messages that are useful for humans and machines.

## Format

```
<type>(<optional scope>): <subject>

<optional body>

<optional footer>
```

### Subject Line Rules

- **50 characters or less** for the subject
- Use imperative mood: "add feature" not "added feature" or "adding feature"
- Don't capitalize the first letter after the type prefix
- No period at the end

### Types

| Type | When to use |
|------|-------------|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `chore` | Build, CI, tooling, deps |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace (not CSS) |
| `ci` | CI/CD pipeline changes |
| `revert` | Reverting a previous commit |

### Scope (Optional)

The area of the codebase affected:
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from payments endpoint`
- `refactor(db): extract query builder into module`

### Body (When Needed)

Explain **why**, not what (the diff shows what):

```
fix(checkout): prevent duplicate order submissions

The submit button was not disabled after the first click,
allowing users to create multiple orders. This caused
duplicate charges in Stripe.
```

### Footer (When Needed)

```
BREAKING CHANGE: rename `getUserById` to `findUser`

Closes #456
Co-authored-by: Name <email>
```

## Examples

Good:
```
feat(dashboard): add real-time notification bell
fix: resolve race condition in WebSocket reconnect
refactor(api): consolidate error handling middleware
test: add integration tests for payment webhook
chore: upgrade TypeScript to 5.4
```

Bad:
```
fixed stuff
WIP
update
changes
asdf
```

## When to Commit

- Each commit should represent one logical change
- Don't mix refactoring with feature work in the same commit
- Don't commit half-working code (use `git stash` instead)
- Commit early and often on feature branches, squash before merge if needed

## Breaking Changes

If the commit introduces a breaking change:
1. Add `!` after the type: `feat(api)!: change auth token format`
2. Add `BREAKING CHANGE:` in the footer with migration instructions
