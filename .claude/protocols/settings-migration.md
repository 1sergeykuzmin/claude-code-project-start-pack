# Settings Migration Protocol

> Automatically migrate settings.json from v1.x to v2.0 format
> Version: 2.0

## Purpose

Seamlessly upgrade existing `settings.json` files to the v2.0 schema while preserving all user customizations.

## When to Run

This protocol runs automatically when:
1. Cold start detects v1.x settings format
2. User runs `/upgrade-framework`
3. Framework version mismatch detected

## Detection

### v1.x Format Indicators

```json
{
  "framework": {
    "version": "1.0.0"  // or 1.x.x
  }
  // Missing: "preset", "execution", "autoUpdate" fields
}
```

### v2.0 Format Indicators

```json
{
  "framework": {
    "version": "2.0.0"  // or 2.x.x
  },
  "preset": "verbose",
  "execution": { ... },
  "autoUpdate": { ... }
}
```

## Migration Steps

### Step 1: Backup Current Settings

```bash
cp .claude/settings.json .claude/settings.json.v1.backup
```

### Step 2: Read Existing Configuration

Load all existing v1.x settings and preserve them.

### Step 3: Add New v2.0 Fields

Add missing fields with backward-compatible defaults:

```json
{
  "preset": "verbose",

  "execution": {
    "mode": "verbose",
    "parallelism": true,
    "pythonPath": "auto"
  },

  "autoUpdate": {
    "enabled": true,
    "confirmBeforeUpdate": true,
    "channel": "stable"
  }
}
```

### Step 4: Migrate Existing Fields

Map v1.x fields to v2.0 equivalents:

| v1.x Field | v2.0 Field | Transformation |
|------------|------------|----------------|
| `protocols.autoTriggers.enabled` | `protocols.autoTriggers.enabled` | Keep as-is |
| `protocols.autoTriggers.mode` | `protocols.autoTriggers.mode` | Keep as-is |
| (new) | `protocols.autoTriggers.completionConfidenceThreshold` | Add: `0.8` |
| (new) | `protocols.autoTriggers.analyzeLastMessages` | Add: `10` |
| `review.compulsory` | `review.compulsory` | Force: `true` |
| (new) | `review.showInSilentMode` | Add: `"always"` |
| (new) | `security.runSecurityScripts` | Add: `true` |
| (new) | `git.autoPush` | Add: `false` |
| (new) | `git.confirmPush` | Add: `true` |
| (new) | `dialog.format` | Add: `"markdown"` |
| (new) | `dialog.useTypeScriptExporter` | Add: `true` |

### Step 5: Update Version

```json
{
  "framework": {
    "version": "2.0.0"
  }
}
```

### Step 6: Validate Against Schema

Validate migrated settings against `.claude/settings.schema.json`.

If validation fails:
- Log specific errors
- Use schema defaults for invalid fields
- Continue with valid configuration

### Step 7: Write Migrated Settings

Save to `.claude/settings.json`.

### Step 8: Update Framework Config

Update `.claude/.framework-config`:

```json
{
  "initialization": {
    "settings_migrated": true,
    "settings_migration_date": "[ISO-8601]",
    "migrated_from_version": "1.0.0"
  }
}
```

### Step 9: Report Migration

**Verbose mode:**
```
┌─────────────────────────────────────────────────────────────┐
│ Settings Migrated: v1.0.0 → v2.0.0                          │
├─────────────────────────────────────────────────────────────┤
│ Preserved:                                                  │
│ ✓ All existing protocol settings                            │
│ ✓ Security configuration                                    │
│ ✓ Git settings                                              │
│ ✓ Document paths                                            │
│                                                             │
│ Added:                                                      │
│ + Preset system (default: verbose)                          │
│ + Execution mode settings                                   │
│ + Auto-update configuration                                 │
│ + Enhanced auto-trigger settings                            │
│                                                             │
│ Backup saved: .claude/settings.json.v1.backup               │
└─────────────────────────────────────────────────────────────┘
```

**Silent mode:**
```
[No output - migration happens silently]
```

## Rollback

If migration causes issues:

```bash
# Restore v1.x settings
cp .claude/settings.json.v1.backup .claude/settings.json

# Reset framework config
# Edit .claude/.framework-config:
# "initialization.settings_migrated": false
```

## Schema Changes Summary

### New Top-Level Fields (v2.0)

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `preset` | string | `"verbose"` | Active preset name |
| `execution` | object | See below | Execution mode config |
| `autoUpdate` | object | See below | Update behavior |

### New Nested Fields (v2.0)

**execution:**
```json
{
  "mode": "verbose",
  "parallelism": true,
  "pythonPath": "auto"
}
```

**autoUpdate:**
```json
{
  "enabled": true,
  "confirmBeforeUpdate": true,
  "channel": "stable"
}
```

**protocols.autoTriggers (additions):**
```json
{
  "completionConfidenceThreshold": 0.8,
  "analyzeLastMessages": 10
}
```

**review (additions):**
```json
{
  "showInSilentMode": "failures_only"
}
```

**security (additions):**
```json
{
  "runSecurityScripts": true
}
```

**git (additions):**
```json
{
  "autoPush": false,
  "confirmPush": true
}
```

**dialog (additions):**
```json
{
  "format": "markdown",
  "useTypeScriptExporter": true
}
```

## Compatibility Notes

1. **v1.x settings continue to work** - Missing fields use defaults
2. **Existing customizations preserved** - User values never overwritten
3. **Backward migration not supported** - v2.0 → v1.x requires manual editing
4. **Schema validation** - Invalid fields logged but don't block migration

## Error Handling

### Cannot Read Settings

```
Error: Cannot read .claude/settings.json
Creating new settings file with defaults.
```

### Invalid JSON

```
Error: Invalid JSON in settings.json
Attempting to parse and recover...
[If recovery fails, create new with defaults]
```

### Schema Validation Failures

```
Warning: Field "execution.mode" has invalid value "turbo"
Using default: "verbose"
```

## Integration

This protocol integrates with:
- Cold Start Protocol (runs migration before loading context)
- Upgrade Framework Command (runs migration as part of upgrade)
- Apply Preset Protocol (runs after migration completes)
