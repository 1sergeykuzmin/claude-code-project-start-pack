# Migrate Command

> Migrate framework between versions
> Version: 2.0

## Usage

```
/migrate [--target <version>] [--local <path>]
```

## Purpose

Safely upgrade the framework from one version to another while:
- Preserving user customizations
- Detecting and handling conflicts
- Providing rollback capability
- Maintaining crash recovery

## Process

### Step 0: Pre-flight Checks

```
Checking migration prerequisites...

✓ Git repository detected
✓ Working directory clean
✓ Current version: 1.0.0
✓ Framework files located
```

**If uncommitted changes exist:**
```
⚠️ Uncommitted changes detected.

Commit or stash changes before migrating:
  git stash
  # or
  git commit -m "WIP: before migration"
```

**If not a git repo:**
```
⚠️ Git repository required for safe migration.

Initialize git:
  git init
  git add .
  git commit -m "Initial commit"
```

### Step 1: Initialize Migration Log

Create `.claude/migration-log.json`:

```json
{
  "migration_id": "uuid-here",
  "source_version": "1.0.0",
  "target_version": "2.0.0",
  "status": "in_progress",
  "current_step": 1,
  "started_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:00Z",
  "conflicts": [],
  "resolutions": [],
  "backed_up_files": [],
  "errors": []
}
```

This enables crash recovery - migration can resume from any step.

### Step 2: Version Detection

```
Current Version: 1.0.0
Target Version: 2.0.0

Changelog:
─────────
v2.0.0 (target)
• Preset system (paranoid, balanced, autopilot, verbose, silent)
• Silent mode protocols
• Python framework core
• Migration command suite
• Enhanced auto-triggers

v1.1.0
• Security scripts
• Crash recovery improvements
```

**If already at target:**
```
✓ Framework is already at v2.0.0
No migration needed.
```

### Step 3: Download Target Version

```
Downloading framework v2.0.0...

From: github.com/1sergeykuzmin/claude-code-project-start-pack/releases/v2.0.0
Files: 45 total
Size: 125 KB

Download complete.
```

**For local upgrade:**
```
Using local source: /path/to/release
Files: 45 total
```

### Step 4: Backup Current Files

```
Creating backup...

.claude/backup-1.0.0/
├── commands/ (15 files)
├── protocols/ (3 files)
├── skills/ (7 files)
├── settings.json
├── COMMIT_POLICY.md
└── [other framework files]

CLAUDE.md.backup created

Backup complete. 28 files preserved.
```

Update migration log with backed_up_files.

### Step 5: Analyze Changes

Compare current files with target version:

```
Analyzing changes...

Files to ADD (new in target):
├── .claude/protocols/cold-start-silent.md
├── .claude/protocols/completion-silent.md
├── .claude/protocols/router.md
├── .claude/presets.json
├── .claude/analysis/ (5 files)
└── src/framework-core/ (12 files)

Files to UPDATE:
├── .claude/settings.json (schema changes)
├── .claude/protocols/auto-triggers.md (enhanced)
├── CLAUDE.md (v2.0 documentation)
└── README.md (new features)

Files UNCHANGED:
├── dev-docs/* (your project docs)
├── .claude/skills/* (preserved)
└── .claude/COMMIT_POLICY.md (if unmodified)
```

### Step 6: Detect Conflicts

Check for user modifications to framework files:

```
Checking for conflicts...
```

**No conflicts:**
```
✓ No conflicts detected
Proceeding with automatic migration.
```

**Conflicts found:**
```
⚠️ Conflicts detected in 2 files:

1. .claude/settings.json
   You modified: Added custom blockedPatterns
   Target adds: New preset and execution fields

2. .claude/protocols/auto-triggers.md
   You modified: Custom trigger keywords
   Target changes: Enhanced detection logic

Run /migrate-resolve to handle conflicts.
```

Update migration log:
```json
{
  "status": "paused",
  "conflicts": [
    {
      "file": ".claude/settings.json",
      "type": "both_modified",
      "user_changes": "custom blockedPatterns",
      "target_changes": "preset, execution fields"
    }
  ]
}
```

### Step 7: Apply Non-Conflicting Changes

If no conflicts (or after resolution):

```
Applying changes...

Added:
  ✓ .claude/protocols/cold-start-silent.md
  ✓ .claude/protocols/completion-silent.md
  ✓ .claude/protocols/router.md
  ✓ .claude/presets.json
  ✓ src/framework-core/ (12 files)

Updated:
  ✓ CLAUDE.md
  ✓ README.md

Preserved (your customizations):
  • dev-docs/*
  • .claude/skills/*
```

### Step 8: Settings Migration

Run settings migration protocol:

```
Migrating settings.json...

Added fields:
  + preset: "verbose"
  + execution.mode: "verbose"
  + execution.parallelism: true
  + autoUpdate.enabled: true

Preserved your settings:
  • protocols.coldStart.triggers
  • security.blockedPatterns
  • All existing configuration

Settings migrated to v2.0 schema.
```

### Step 9: Next Steps

**If conflicts exist:**
```
Migration paused due to conflicts.

Next: /migrate-resolve
      Review and resolve each conflict.

Then: /migrate-finalize
      Complete the migration.
```

**If no conflicts:**
```
Migration ready to finalize.

Next: /migrate-finalize
      Complete migration and commit.
```

## Options

### --target <version>
Specify target version:
```
/migrate --target 2.1.0
```

### --local <path>
Use local release instead of downloading:
```
/migrate --local /path/to/release
```

### --force
Skip conflict detection (use with caution):
```
/migrate --force
```

## Crash Recovery

If migration is interrupted:

1. On next `/migrate`, detect incomplete migration
2. Read `migration-log.json` for state
3. Offer options:
   - Resume from last step
   - Rollback to pre-migration state
   - Start fresh

```
⚠️ Incomplete migration detected

Migration: 1.0.0 → 2.0.0
Status: paused at step 6
Started: 2026-02-04 10:30:00

[R]esume migration
[B]ack to start (rollback)
[C]ontinue where left off
>
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/migrate` | Start migration (this command) |
| `/migrate-resolve` | Resolve conflicts |
| `/migrate-finalize` | Complete migration |
| `/migrate-rollback` | Revert migration |
| `/upgrade-framework` | Simpler upgrade (no conflicts) |
