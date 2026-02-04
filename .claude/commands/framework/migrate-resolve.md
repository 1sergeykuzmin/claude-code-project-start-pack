# Migrate Resolve Command

> Resolve conflicts during framework migration
> Version: 2.0

## Usage

```
/migrate-resolve
```

## Purpose

Interactively resolve conflicts detected during `/migrate`. Each conflict is presented with options for how to handle the difference between your customizations and the new version.

## Prerequisites

- Active migration in progress (`migration-log.json` exists)
- Status is "paused" with conflicts

**If no migration active:**
```
No migration in progress.

Start a migration first:
  /migrate
```

## Process

### Step 1: Load Migration State

Read `.claude/migration-log.json`:

```
Loading migration state...

Migration: 1.0.0 → 2.0.0
Status: paused
Conflicts: 2 unresolved
```

### Step 2: List Conflicts

```
Unresolved Conflicts:

1. .claude/settings.json
   Status: ⚠️ Needs resolution

2. .claude/protocols/auto-triggers.md
   Status: ⚠️ Needs resolution

Resolve all conflicts to continue migration.
```

### Step 3: Resolve Each Conflict

For each conflict, show detailed diff and options:

#### Conflict 1: settings.json

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conflict 1/2: .claude/settings.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your version has:
  "security": {
    "blockedPatterns": [
      ".env",
      ".env.*",
+     "*.secret",        ← Your addition
+     "config/local.*"   ← Your addition
    ]
  }

New version adds:
  + "preset": "verbose"
  + "execution": { "mode": "verbose", "parallelism": true }
  + "autoUpdate": { "enabled": true }
  + "protocols.autoTriggers.completionConfidenceThreshold": 0.8

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
  [K] Keep mine    - Preserve your settings.json, manually add new fields later
  [T] Take theirs  - Use new version, lose your custom blockedPatterns
  [M] Merge        - Keep your customizations AND add new fields (Recommended)
  [S] Skip         - Decide later

Choice [K/T/M/S]:
```

**On Merge (M):**
```
Merging settings.json...

Result:
  ✓ Preserved: Your custom blockedPatterns
  ✓ Added: preset, execution, autoUpdate fields
  ✓ Added: New autoTriggers settings

Merged successfully. Preview:
{
  "preset": "verbose",
  "execution": { ... },
  "security": {
    "blockedPatterns": [
      ".env", ".env.*",
      "*.secret",        ← Preserved
      "config/local.*"   ← Preserved
    ]
  }
}

Accept merge? [Y/n]
```

#### Conflict 2: auto-triggers.md

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conflict 2/2: .claude/protocols/auto-triggers.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your version has:
  Custom trigger keywords:
+   "deploy", "ship it", "launch"

New version changes:
  • AI-based completion probability scoring
  • Last 10 message analysis
  • Idle time monitoring
  • Enhanced false positive prevention

This is a significant rewrite. Your custom keywords would need
to be re-added to the new version.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
  [K] Keep mine    - Keep your auto-triggers.md as-is
  [T] Take theirs  - Use new version (Recommended), re-add keywords manually
  [M] Merge        - Attempt automatic merge (may need manual review)
  [S] Skip         - Decide later

Choice [K/T/M/S]:
```

**On Take Theirs (T):**
```
Using new auto-triggers.md

Note: Your custom keywords were:
  • "deploy"
  • "ship it"
  • "launch"

To re-add them, edit .claude/protocols/auto-triggers.md after migration.

Continue? [Y/n]
```

### Step 4: Update Migration Log

After each resolution:

```json
{
  "status": "in_progress",
  "conflicts": [
    {
      "file": ".claude/settings.json",
      "resolved": true,
      "resolution": "merge",
      "resolved_at": "2026-02-04T10:45:00Z"
    },
    {
      "file": ".claude/protocols/auto-triggers.md",
      "resolved": true,
      "resolution": "take_theirs",
      "resolved_at": "2026-02-04T10:46:00Z"
    }
  ]
}
```

### Step 5: Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conflict Resolution Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resolved:
  ✓ .claude/settings.json (merged)
  ✓ .claude/protocols/auto-triggers.md (take theirs)

All conflicts resolved.

Next step:
  /migrate-finalize
```

## Resolution Options

### [K] Keep Mine
- Preserves your version entirely
- New version changes are NOT applied to this file
- You may need to manually update later

### [T] Take Theirs
- Uses the new version entirely
- Your customizations are lost for this file
- Your changes are logged for reference

### [M] Merge
- Attempts to combine both versions
- Your customizations are preserved where possible
- New additions are included
- May require manual review if complex

### [S] Skip
- Defers this conflict for later
- Migration remains paused
- Can resume with `/migrate-resolve`

## Partial Resolution

You can resolve some conflicts and skip others:

```
2 conflicts: 1 resolved, 1 skipped

Skipped conflicts must be resolved before /migrate-finalize.

Continue resolving? [Y/n]
```

## Undo Resolution

If you made a mistake:

```
/migrate-resolve --undo settings.json
```

Reverts the resolution for that file, marking it as unresolved.

## View Conflict Details

To see full diff without resolving:

```
/migrate-resolve --show settings.json
```

Shows complete file comparison without prompting for resolution.

## Related Commands

| Command | Purpose |
|---------|---------|
| `/migrate` | Start migration |
| `/migrate-resolve` | Resolve conflicts (this command) |
| `/migrate-finalize` | Complete migration |
| `/migrate-rollback` | Revert migration |
