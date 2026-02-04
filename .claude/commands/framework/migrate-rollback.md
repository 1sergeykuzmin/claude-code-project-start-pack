# Migrate Rollback Command

> Revert a framework migration
> Version: 2.0

## Usage

```
/migrate-rollback [--force]
```

## Purpose

Safely revert a migration, restoring the previous framework version. This command:
- Restores backed-up files
- Removes newly added files
- Reverts migration commit (if made)
- Cleans up migration artifacts

## When to Use

- Migration introduced breaking changes
- Incompatibility with your project
- Want to return to previous version
- Testing migration before committing

## Prerequisites

- Backup exists at `.claude/backup-{version}/`
- Migration log or archive exists

**If no backup:**
```
⚠️ No backup found for rollback.

Backups are created during /migrate and preserved until manually deleted.
Without a backup, manual restoration is required.
```

## Process

### Step 1: Detect Migration State

```
Detecting migration state...

Current version: 2.0.0
Backup version: 1.0.0
Backup location: .claude/backup-1.0.0/
Migration commit: abc1234 (if applicable)
```

### Step 2: Confirm Rollback

```
┌─────────────────────────────────────────────────────────────────┐
│ Rollback Confirmation                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ This will:                                                       │
│ • Restore framework v1.0.0 from backup                           │
│ • Remove v2.0.0 files not in backup                              │
│ • Revert migration commit (abc1234)                              │
│                                                                  │
│ Your project files are NOT affected:                             │
│ • dev-docs/* preserved                                           │
│ • Source code preserved                                          │
│ • Git history preserved (commit reverted, not deleted)           │
│                                                                  │
│ Backup will be preserved after rollback.                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Proceed with rollback? [y/N]
```

### Step 3: Revert Migration Commit

If migration was committed:

```
Reverting migration commit...

git revert abc1234 --no-edit

Reverted: abc1234 "chore: Migrate framework from v1.0.0 to v2.0.0"
New commit: def5678 "Revert: Migrate framework from v1.0.0 to v2.0.0"
```

**If commit was not made (--no-commit was used):**
```
No migration commit to revert.
Proceeding with file restoration.
```

### Step 4: Remove New Files

```
Removing v2.0.0 files not in backup...

Removed:
  ✓ .claude/protocols/cold-start-silent.md
  ✓ .claude/protocols/completion-silent.md
  ✓ .claude/protocols/cold-start-optimized.md
  ✓ .claude/protocols/completion-optimized.md
  ✓ .claude/protocols/router.md
  ✓ .claude/presets.json
  ✓ .claude/analysis/ (6 files)
  ✓ src/framework-core/ (12 files)
```

### Step 5: Restore Backup Files

```
Restoring from backup...

From .claude/backup-1.0.0/:
  ✓ .claude/settings.json
  ✓ .claude/protocols/cold-start.md
  ✓ .claude/protocols/completion.md
  ✓ .claude/protocols/auto-triggers.md
  ✓ CLAUDE.md

28 files restored.
```

### Step 6: Reset Framework Config

```
Resetting framework configuration...

.claude/.framework-config:
  ✓ framework_version: "1.0.0"
  ✓ active_preset: removed (v1.x doesn't have presets)
```

### Step 7: Clean Up

```
Cleaning up migration artifacts...

Removed:
  ✓ .claude/migration-log.json
  ✓ .claude/migrations/2026-02-04-1.0.0-to-2.0.0/ (archived data)

Preserved:
  • .claude/backup-1.0.0/ (for future reference)
```

### Step 8: Rollback Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ Rollback Complete                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Restored version: 1.0.0                                          │
│ Reverted commit: abc1234                                         │
│ New commit: def5678                                              │
│                                                                  │
│ Restored files: 28                                               │
│ Removed files: 25                                                │
│                                                                  │
│ Your project files: Unchanged                                    │
│                                                                  │
│ Backup preserved at: .claude/backup-1.0.0/                       │
│ (Delete when no longer needed)                                   │
│                                                                  │
│ Framework is now at v1.0.0                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Options

### --force
Skip confirmation prompt:
```
/migrate-rollback --force
```

Use with caution. Immediately begins rollback.

### --keep-new-files
Don't remove files added by migration:
```
/migrate-rollback --keep-new-files
```

Useful if you want to keep some v2.0 features while reverting core changes.

### --no-commit
Revert files but don't create revert commit:
```
/migrate-rollback --no-commit
```

Changes are applied but not committed. User can commit manually.

## Rollback During Migration

If migration is in progress (not yet finalized):

```
/migrate-rollback
```

```
Migration in progress detected.

This will:
• Cancel the current migration
• Restore original files from backup
• Clean up migration state

No commits were made, so no commits to revert.

Proceed? [y/N]
```

## Error Handling

### Backup Corrupted
```
⚠️ Backup verification failed:

Missing files in backup:
  • .claude/settings.json
  • CLAUDE.md

Partial rollback is risky. Options:
1. Attempt partial rollback (may break framework)
2. Download v1.0.0 fresh from GitHub
3. Cancel and investigate

Choice [1/2/3]:
```

### Revert Conflict
```
⚠️ Git revert conflict:

CONFLICT in CLAUDE.md

The file was modified after migration.
Resolve conflict manually:
  git status
  # edit conflicted files
  git add .
  git revert --continue
```

### Permission Error
```
⚠️ Cannot write to .claude/settings.json

Check file permissions and try again.
```

## Re-Migrating After Rollback

After rollback, you can migrate again:

```
/migrate
```

This starts a fresh migration. Previous backup may be used or a new backup created.

## Related Commands

| Command | Purpose |
|---------|---------|
| `/migrate` | Start migration |
| `/migrate-resolve` | Resolve conflicts |
| `/migrate-finalize` | Complete migration |
| `/migrate-rollback` | Revert migration (this command) |
