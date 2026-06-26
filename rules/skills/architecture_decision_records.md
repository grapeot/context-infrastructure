## 元数据

- **类型**: Workflow
- **分类**: Planning & Architecture
- **适用场景**: Document technical decisions as Architecture Decision Records (ADRs) with context, options considered, and rationale.
- **上游来源**: [architecture-decision-records](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/architecture-decision-records)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Architecture Decision Records

Document significant technical decisions so future you (and your team) understands why choices were made.

## When to Write an ADR

Write one when you're making a decision that:
- Is hard to reverse later
- Affects multiple parts of the system
- Involves tradeoffs between valid options
- Will be questioned by someone in 6 months

Examples: choosing a database, adopting a framework, changing auth strategy, restructuring the API, adding a build tool.

## Template

Create files in `docs/decisions/` (or `adr/`) with sequential numbering:

```markdown
# ADR-001: Use PostgreSQL for primary database

## Status

Accepted | Proposed | Deprecated | Superseded by ADR-XXX

## Date

2026-04-10

## Context

What is the problem or situation that requires a decision?
Include constraints, requirements, and forces at play.

## Options Considered

### Option A: PostgreSQL
- Pros: ACID compliance, JSON support, mature ecosystem, free
- Cons: Requires managing connections, vertical scaling limits

### Option B: MongoDB
- Pros: Flexible schema, horizontal scaling
- Cons: No transactions across collections, eventual consistency issues

### Option C: PlanetScale (MySQL)
- Pros: Serverless, branching, managed
- Cons: Vendor lock-in, no foreign keys in their branching model

## Decision

We chose **PostgreSQL** because:
1. Our data is relational — users, teams, projects with clear relationships
2. We need ACID transactions for billing operations
3. JSON columns give us schema flexibility where needed
4. Prisma/Drizzle have excellent Postgres support

## Consequences

- We need to manage connection pooling (use PgBouncer or Prisma's built-in pool)
- Migrations must be backwards-compatible for zero-downtime deploys
- We accept vertical scaling limits and will shard later if needed
```

## Workflow

1. **Identify** the decision being made
2. **Research** the options (at least 2-3 alternatives)
3. **Write** the ADR using the template
4. **Review** with the team (PR or discussion)
5. **Merge** as accepted
6. **Reference** from code comments when relevant: `// See ADR-001`

## File Naming

```
docs/decisions/
├── 001-use-postgresql.md
├── 002-adopt-trpc-over-rest.md
├── 003-switch-to-pnpm.md
└── template.md
```

## Tips

- Keep ADRs short — 1-2 pages max
- Write them in the present tense ("We choose X" not "We chose X")
- It's OK to write an ADR after the fact if you forgot to write one during the decision
- Superseded ADRs should link to their replacement, not be deleted
- ADRs are not design docs — they capture the decision, not the full design
