## 元数据

- **类型**: Workflow
- **分类**: Planning & Architecture
- **适用场景**: Design database schemas — tables, relationships, indexes, constraints, and ORM setup. Covers relational design, normalization, and common patterns.
- **上游来源**: [database-design](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/database-design)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Database Design

Design a database schema from requirements.

## Workflow

### 1. Identify Entities

From the requirements, extract the core entities (nouns):
- Users, Teams, Projects, Tasks, Comments, etc.
- Each entity becomes a table

### 2. Define Relationships

| Relationship | Implementation |
|-------------|----------------|
| One-to-one | Foreign key with unique constraint, or embed in same table |
| One-to-many | Foreign key on the "many" side |
| Many-to-many | Junction/join table |
| Self-referential | Foreign key pointing to same table (e.g. `parent_id`) |

### 3. Design the Schema

For each table:

```sql
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  avatar_url  TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE projects (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  owner_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 4. Apply Best Practices

**Primary keys:**
- Use `UUID` for distributed systems or public-facing IDs
- Use `SERIAL`/`BIGSERIAL` for internal-only IDs (faster joins)

**Timestamps:**
- Always add `created_at` and `updated_at`
- Use `TIMESTAMPTZ` (with timezone), never `TIMESTAMP`

**Naming:**
- Tables: plural snake_case (`users`, `project_members`)
- Columns: singular snake_case (`user_id`, `created_at`)
- Indexes: `idx_<table>_<columns>` (`idx_users_email`)

**Constraints:**
- `NOT NULL` on everything unless it's genuinely optional
- `UNIQUE` on natural keys (email, slug, external IDs)
- `REFERENCES` with `ON DELETE` behavior (CASCADE, SET NULL, RESTRICT)
- `CHECK` constraints for enums or value ranges

### 5. Add Indexes

```sql
-- For columns you filter/sort by frequently
CREATE INDEX idx_projects_owner_id ON projects(owner_id);

-- For unique lookups
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Composite for common query patterns
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
```

**When to index:**
- Foreign keys (almost always)
- Columns in WHERE clauses
- Columns in ORDER BY
- Columns in JOIN conditions

**When NOT to index:**
- Small tables (<1000 rows)
- Columns with low cardinality (boolean, status with 3 values)
- Columns that are rarely queried

### 6. ORM Setup

**Prisma:**
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  projects  Project[]
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  @@map("users")
}
```

**Drizzle:**
```typescript
export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});
```

## Common Patterns

**Soft deletes:** Add `deleted_at TIMESTAMPTZ` instead of actually deleting rows
**Audit log:** Separate `audit_events` table with `entity_type`, `entity_id`, `action`, `actor_id`, `payload`
**Tags/labels:** Junction table (`task_tags`) with `task_id` + `tag_id`
**Tree/hierarchy:** `parent_id` self-reference, or materialized path (`/1/4/7/`)
**Polymorphic associations:** Use `entity_type` + `entity_id` columns (avoid if possible, prefer separate FKs)

## Tips

- Start normalized (3NF), denormalize only when you have measured performance problems
- Don't store derived data unless you have a caching/invalidation strategy
- Use database enums or check constraints for status fields, not free-text
- Always think about what happens when you delete a parent record
