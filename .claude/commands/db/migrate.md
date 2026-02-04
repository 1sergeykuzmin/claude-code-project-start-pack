# Database Migration Command

Manage database schema changes safely.

## Process

### Step 1: Plan Migration

Before making changes:
- Review current schema
- Identify required changes
- Consider data preservation
- Plan rollback strategy

### Step 2: Create Migration

#### Prisma
```bash
# Create migration
npx prisma migrate dev --name descriptive_name

# Examples:
npx prisma migrate dev --name add_user_roles
npx prisma migrate dev --name create_posts_table
npx prisma migrate dev --name add_index_on_email
```

#### Drizzle
```bash
# Generate migration
npx drizzle-kit generate:pg --name add_user_roles

# Apply migration
npx drizzle-kit push:pg
```

#### Raw SQL
```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### Step 3: Review Migration

Check generated SQL:
```bash
# Prisma
cat prisma/migrations/[timestamp]_[name]/migration.sql

# Drizzle
cat drizzle/[timestamp]_[name].sql
```

Verify:
- [ ] No data loss
- [ ] Indexes created where needed
- [ ] Constraints are correct
- [ ] Default values set appropriately

### Step 4: Test Migration

```bash
# On development database
npx prisma migrate dev

# Verify schema
npx prisma db pull
npx prisma studio
```

### Step 5: Deploy Migration

```bash
# Production deployment
npx prisma migrate deploy
```

## Common Migration Patterns

### Add Column
```prisma
// schema.prisma
model User {
  id    String @id @default(uuid())
  email String @unique
  name  String
  role  String @default("user") // New column
}
```

### Add Table
```prisma
model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
}
```

### Add Index
```prisma
model User {
  id    String @id @default(uuid())
  email String @unique
  name  String

  @@index([name]) // New index
}
```

### Add Relation
```prisma
model User {
  id    String @id @default(uuid())
  posts Post[] // New relation
}

model Post {
  id       String @id @default(uuid())
  authorId String
  author   User   @relation(fields: [authorId], references: [id])
}
```

### Rename Column (Careful!)
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Step 2: Copy data
UPDATE users SET full_name = name;

-- Step 3: Make new column required
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;

-- Step 4: Drop old column (after app updated)
ALTER TABLE users DROP COLUMN name;
```

### Remove Column (Careful!)
```sql
-- Ensure no code references this column first!
ALTER TABLE users DROP COLUMN deprecated_field;
```

## Safety Checklist

### Before Migration
- [ ] Backup database
- [ ] Test migration on copy of production data
- [ ] Review generated SQL
- [ ] Verify no data loss
- [ ] Plan rollback

### During Migration
- [ ] Monitor for errors
- [ ] Check for long-running queries
- [ ] Verify data integrity

### After Migration
- [ ] Verify schema is correct
- [ ] Test application functionality
- [ ] Check performance

## Rollback Strategy

### Prisma
```bash
# Reset to previous migration
npx prisma migrate reset

# Or manually:
# 1. Restore from backup
# 2. Remove failed migration folder
# 3. Run prisma migrate dev
```

### Manual Rollback
```sql
-- Create rollback script alongside migration
-- migrations/001_add_role_rollback.sql
ALTER TABLE users DROP COLUMN role;
```

## Environment-Specific Commands

```bash
# Development
DATABASE_URL="postgresql://localhost/dev" npx prisma migrate dev

# Staging
DATABASE_URL="postgresql://staging-host/db" npx prisma migrate deploy

# Production
DATABASE_URL="postgresql://prod-host/db" npx prisma migrate deploy
```

## Best Practices

1. **Never modify existing migrations** - Create new ones
2. **Use descriptive names** - `add_user_email_index` not `update`
3. **One logical change per migration** - Easier to rollback
4. **Test on production data copy** - Catch issues early
5. **Have rollback ready** - Before deploying
6. **Coordinate with deployments** - Migration then code, or vice versa

## Troubleshooting

### Migration Drift
```bash
# Check for drift
npx prisma migrate diff

# Reset if needed (dev only!)
npx prisma migrate reset
```

### Failed Migration
```bash
# Mark as rolled back
npx prisma migrate resolve --rolled-back [migration_name]

# Or mark as applied (if manually fixed)
npx prisma migrate resolve --applied [migration_name]
```

### Schema Out of Sync
```bash
# Pull current schema
npx prisma db pull

# Generate migration to fix
npx prisma migrate dev
```
