# Migrate Finalize Command

> Complete framework migration after conflict resolution
> Version: 2.0

## Usage

```
/migrate-finalize
```

## Purpose

Finalize a migration after all conflicts have been resolved. This command:
- Applies all resolved changes
- Updates framework configuration
- Creates migration commit
- Cleans up temporary files

## Prerequisites

- Active migration in progress
- All conflicts resolved (none skipped)

**If conflicts remain:**
```
⚠️ Unresolved conflicts remain:

1. .claude/protocols/auto-triggers.md

Resolve all conflicts first:
  /migrate-resolve
```

**If no migration active:**
```
No migration in progress.

Start a migration:
  /migrate
```

## Process

### Step 1: Verify Resolution

```
Verifying migration state...

Migration: 1.0.0 → 2.0.0
Conflicts: 2 resolved, 0 remaining

✓ Ready to finalize
```

### Step 2: Apply Resolved Changes

```
Applying changes...

From resolution:
  ✓ .claude/settings.json (merged)
  ✓ .claude/protocols/auto-triggers.md (take theirs)

From automatic update:
  ✓ .claude/protocols/cold-start-silent.md (added)
  ✓ .claude/protocols/completion-silent.md (added)
  ✓ .claude/protocols/router.md (added)
  ✓ .claude/presets.json (added)
  ✓ src/framework-core/ (12 files added)
  ✓ CLAUDE.md (updated)
  ✓ README.md (updated)

All changes applied.
```

### Step 3: Update Framework Configuration

```
Updating framework configuration...

.claude/.framework-config:
  ✓ framework_version: "2.0.0"
  ✓ active_preset: "verbose"
  ✓ python_detected: true
  ✓ node_detected: true
```

### Step 4: Run Post-Migration Tasks

```
Running post-migration tasks...

  ✓ Validating settings.json against schema
  ✓ Installing git hooks
  ✓ Detecting Python installation
  ✓ Creating logs directory structure
```

### Step 5: Archive Migration Artifacts

```
Archiving migration artifacts...

Moved to .claude/migrations/2026-02-04-1.0.0-to-2.0.0/:
  • migration-log.json
  • conflict-resolutions.json
  • backup reference

Backup preserved at .claude/backup-1.0.0/
(Can be deleted after verifying migration)
```

### Step 6: Create Migration Commit

```
Creating migration commit...

Staged files:
  • .claude/protocols/ (6 files)
  • .claude/presets.json
  • .claude/settings.json
  • .claude/.framework-config
  • src/framework-core/ (12 files)
  • CLAUDE.md
  • README.md
  • [other migration files]

Commit message:
────────────────
chore: Migrate framework from v1.0.0 to v2.0.0

Changes:
- Added preset system (5 presets)
- Added silent mode protocols
- Added Python framework core
- Enhanced auto-triggers
- Updated documentation

Co-Authored-By: Claude <noreply@anthropic.com>
────────────────

Commit? [Y/n]
```

**On confirm:**
```
Committed: abc1234
```

### Step 7: Migration Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ Migration Complete                                               │
├─────────────────────────────────────────────────────────────────┤
│ Previous version: 1.0.0                                          │
│ Current version: 2.0.0                                           │
│ Commit: abc1234                                                  │
│                                                                  │
│ What's New:                                                      │
│ • Preset system - choose behavior profile                        │
│ • Silent mode - zero output on success                           │
│ • Python core - 10x faster protocol execution                    │
│ • Enhanced triggers - AI completion detection                    │
│                                                                  │
│ Your Customizations:                                             │
│ • Preserved: Custom security patterns in settings.json           │
│ • Note: Re-add custom triggers to auto-triggers.md if needed     │
│                                                                  │
│ Backup: .claude/backup-1.0.0/                                    │
│ Archive: .claude/migrations/2026-02-04-1.0.0-to-2.0.0/           │
│                                                                  │
│ Next Steps:                                                      │
│ 1. Review CLAUDE.md for v2.0 features                            │
│ 2. Try /apply-preset balanced for optimized experience           │
│ 3. Delete backup after verifying: rm -rf .claude/backup-1.0.0    │
└─────────────────────────────────────────────────────────────────┘
```

### Step 8: Cleanup

```
Cleaning up...

Removed:
  ✓ .claude/migration-log.json (archived)
  ✓ Temporary merge files

Preserved:
  • Backup at .claude/backup-1.0.0/
  • Migration archive for reference

Migration finalized.
```

## Options

### --no-commit
Apply changes without creating commit:
```
/migrate-finalize --no-commit
```

Changes are applied but not committed. User can commit manually later.

### --keep-backup
Don't prompt about backup deletion:
```
/migrate-finalize --keep-backup
```

### --delete-backup
Automatically delete backup after successful migration:
```
/migrate-finalize --delete-backup
```

## Error Handling

### Validation Failure
```
⚠️ Settings validation failed:

Field "preset" has invalid value "turbo"
Expected one of: paranoid, balanced, autopilot, verbose, silent

Fix settings.json and run /migrate-finalize again.
```

### Commit Failure
```
⚠️ Commit failed: pre-commit hook rejected

Changes applied but not committed.
Review and commit manually:
  git status
  git add .
  git commit -m "chore: Migrate to v2.0.0"
```

### File Write Failure
```
⚠️ Cannot write to .claude/settings.json

Check file permissions and try again.
```

## Rollback After Finalize

If issues found after finalization:

```
/migrate-rollback
```

This restores from `.claude/backup-1.0.0/` and reverts the migration commit.

**Note:** Rollback is only available while backup exists.

## Related Commands

| Command | Purpose |
|---------|---------|
| `/migrate` | Start migration |
| `/migrate-resolve` | Resolve conflicts |
| `/migrate-finalize` | Complete migration (this command) |
| `/migrate-rollback` | Revert migration |
