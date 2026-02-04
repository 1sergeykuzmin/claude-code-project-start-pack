# Apply Preset Protocol

> Applies a preset configuration to the current session
> Version: 2.0

## Purpose

Load and apply preset settings to control framework behavior. Presets provide predefined configurations for different use cases.

## Available Presets

| Preset | Output | Confirmations | Auto-Triggers | Best For |
|--------|--------|---------------|---------------|----------|
| **paranoid** | Full | All | Disabled | Sensitive projects, learning |
| **balanced** | Optimized | Single | Suggest | Daily development |
| **autopilot** | Silent | Minimal | Execute | Personal projects, prototyping |
| **verbose** | Full | All | Suggest | Transparency, debugging (DEFAULT) |
| **silent** | None | None | Execute | Flow state, experienced users |

## Execution

### Step 1: Determine Active Preset

Check in order:
1. Command argument: `/apply-preset <preset-name>`
2. `.claude/.framework-config` → `active_preset`
3. `.claude/settings.json` → `preset`
4. Default: `"verbose"`

```
Active preset: [preset-name]
```

### Step 2: Load Preset Definition

Read from `.claude/presets.json`:

```json
{
  "presets": {
    "[preset-name]": {
      "settings": { ... },
      "behaviors": { ... }
    }
  }
}
```

### Step 3: Check Invariants

**These settings CANNOT be changed by any preset:**

| Setting | Value | Reason |
|---------|-------|--------|
| `review.compulsory` | `true` | /codex-review is always mandatory |
| `protocols.completion.requireReview` | `true` | Review before commit is required |

If preset attempts to override invariants → Ignore and warn.

### Step 4: Apply Settings

Merge preset settings with current configuration:

```
Priority (highest to lowest):
1. User overrides in settings.json
2. Preset settings
3. Schema defaults
```

### Step 5: Configure Session Behavior

Based on `behaviors` from preset:

**Cold Start:**
- `full` → Use `cold-start.md`
- `optimized` → Use `cold-start-optimized.md`
- `silent` → Use `cold-start-silent.md`

**Completion:**
- `full` → Use `completion.md`
- `summary` / `minimal` → Use `completion-optimized.md`
- `hash_only` → Use `completion-silent.md`

**Auto-Triggers:**
- `disabled` → Set `autoTriggers.mode = "manual"`
- `suggest` → Set `autoTriggers.mode = "assisted"`
- `execute` → Set `autoTriggers.mode = "proactive"`

### Step 6: Update Framework Config

Write to `.claude/.framework-config`:

```json
{
  "active_preset": "[preset-name]",
  "preset_applied_at": "[ISO-8601 timestamp]"
}
```

### Step 7: Confirmation

**Verbose/Paranoid mode:**
```
┌─────────────────────────────────────────────────────────────┐
│ Preset Applied: [PRESET-NAME]                               │
├─────────────────────────────────────────────────────────────┤
│ Output mode: [verbose|optimized|silent]                     │
│ Commit confirmation: [always|once|never]                    │
│ Auto-triggers: [disabled|suggest|execute]                   │
│ Auto-update: [confirm|auto+notice|auto+silent]              │
│                                                             │
│ Invariants preserved:                                       │
│ ✓ /codex-review remains mandatory                           │
│ ✓ Review before commit enabled                              │
└─────────────────────────────────────────────────────────────┘
```

**Silent mode:**
```
[No output]
```

## Changing Presets

### Via Command

```
/apply-preset balanced
```

### Via Settings

Edit `.claude/settings.json`:
```json
{
  "preset": "balanced"
}
```

### Via Framework Config

Edit `.claude/.framework-config`:
```json
{
  "active_preset": "balanced"
}
```

## Override Specific Settings

Presets can be overridden for specific settings:

```json
{
  "preset": "silent",
  "protocols": {
    "completion": {
      "autoCommit": false  // Override: still ask for commit
    }
  }
}
```

User overrides in `settings.json` always take precedence over preset defaults.

## Preset Comparison

### Output Verbosity

| Event | paranoid | balanced | autopilot | verbose | silent |
|-------|----------|----------|-----------|---------|--------|
| Cold start init | All steps | Summary | Nothing | All steps | Nothing |
| Task progress | All | Key milestones | Nothing | All | Nothing |
| Review results | Full report | Failures only | Failures only | Full report | Failures only |
| Commit | Confirm + details | Confirm once | Auto + hash | Confirm + details | Hash only |
| Session end | Full summary | Brief summary | Nothing | Full summary | Nothing |

### Confirmation Prompts

| Action | paranoid | balanced | autopilot | verbose | silent |
|--------|----------|----------|-----------|---------|--------|
| Commit changes | Always | Once | Never | Always | Never |
| Push to remote | Always | Once | Once | Always | Never |
| Create PR | Always | Always | Always | Always | Always |
| Apply update | Always | Auto | Auto | Always | Auto |
| Delete files | Always | Always | Once | Always | Once |

## Error Handling

### Unknown Preset

```
Error: Unknown preset "[name]"

Available presets:
- paranoid: Maximum safety, all confirmations
- balanced: Recommended for daily development
- autopilot: Maximum automation
- verbose: Full visibility (default)
- silent: Zero output on success

Use: /apply-preset <preset-name>
```

### Invalid Override

```
Warning: Cannot override invariant setting "review.compulsory"
This setting is locked to "true" for security.
Continuing with invariant preserved.
```

## Integration

This protocol is called:
1. On cold start (load active preset)
2. When user runs `/apply-preset`
3. When `settings.json` preset field changes
4. On first run (apply default preset)

## Notes

- Presets affect behavior, not functionality
- All skills (/prd, /trd, /to-do, etc.) work with all presets
- /codex-review is ALWAYS mandatory regardless of preset
- Preset changes take effect immediately
- Session history is not affected by preset changes
