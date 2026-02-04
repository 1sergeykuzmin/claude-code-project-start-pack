# Preset System Design

## Status
Accepted

## Date
2026-02-04

## Overview

The preset system provides predefined configurations that control framework behavior. Users select a preset to change multiple settings at once, simplifying configuration.

## Presets

### paranoid
**Philosophy:** Maximum safety and visibility.

| Aspect | Setting |
|--------|---------|
| Output | Full progress for all operations |
| Confirmations | Always ask before commit, push, PR |
| Auto-triggers | Disabled - manual commands only |
| Auto-update | Always confirm before applying |
| Security warnings | Show all, including low severity |

**Best for:** Sensitive projects, corporate environments, learning the framework.

### balanced
**Philosophy:** Practical defaults for daily development.

| Aspect | Setting |
|--------|---------|
| Output | Optimized - key information only |
| Confirmations | Once per session for commits |
| Auto-triggers | Suggest but don't auto-execute |
| Auto-update | Auto-apply with notification |
| Security warnings | Show critical and high only |

**Best for:** Regular development, trusted codebases.

### autopilot
**Philosophy:** Maximum automation with minimal interruption.

| Aspect | Setting |
|--------|---------|
| Output | Silent - minimal feedback |
| Confirmations | Never for commits, once for push |
| Auto-triggers | Execute for explicit keywords |
| Auto-update | Auto-apply silently |
| Security warnings | Show critical only |

**Best for:** Personal projects, rapid prototyping.

### verbose
**Philosophy:** Full transparency (v1.x compatibility).

| Aspect | Setting |
|--------|---------|
| Output | Full progress for all operations |
| Confirmations | Always ask |
| Auto-triggers | Suggest but don't auto-execute |
| Auto-update | Always confirm |
| Security warnings | Show all |

**Best for:** Debugging, understanding framework behavior, v1.x users.

### silent
**Philosophy:** Zero output unless necessary.

| Aspect | Setting |
|--------|---------|
| Output | Nothing on success, errors only |
| Confirmations | Never for commits or push |
| Auto-triggers | Execute automatically |
| Auto-update | Auto-apply silently |
| Security warnings | Show critical only |

**Best for:** Flow state optimization, experienced users.

## Architecture

### Files

```
.claude/
├── settings.json         # User configuration + active preset
├── presets.json          # Preset definitions
├── .framework-config     # Runtime state including active preset
└── protocols/
    └── apply-preset.md   # Preset application logic
```

### Preset Definition Schema

```json
{
  "presets": {
    "<preset-name>": {
      "name": "Display Name",
      "description": "What this preset does",
      "recommended_for": "Use cases",
      "default": false,
      "settings": {
        "<path.to.setting>": "<value>"
      },
      "behaviors": {
        "<behavior-name>": "<behavior-value>"
      }
    }
  }
}
```

### Setting Resolution Order

1. **User overrides** in `settings.json` (highest priority)
2. **Preset settings** from `presets.json`
3. **Schema defaults** from `settings.schema.json` (lowest priority)

This allows users to select a preset but override specific settings.

## Invariants

Some settings cannot be changed by any preset:

| Setting | Fixed Value | Reason |
|---------|-------------|--------|
| `review.compulsory` | `true` | Code review is core framework principle |
| `protocols.completion.requireReview` | `true` | Review before commit is mandatory |

Attempts to override invariants are silently ignored.

## Behaviors

Behaviors are high-level descriptions that map to protocol selection:

| Behavior | Values | Effect |
|----------|--------|--------|
| `cold_start_output` | full, optimized, silent | Selects protocol variant |
| `completion_output` | full, summary, minimal, hash_only | Selects protocol variant |
| `commit_confirmation` | always, once, never | Controls commit prompts |
| `auto_triggers` | disabled, suggest, execute | Controls auto-detection |
| `auto_update` | confirm_always, auto_with_notice, auto_silent | Controls updates |

## Usage

### Set Preset via Settings

```json
{
  "preset": "balanced"
}
```

### Set Preset via Command

```
/apply-preset silent
```

### Override Specific Setting

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

## Protocol Routing

Based on active preset, the protocol router selects:

| Preset | Cold Start | Completion |
|--------|------------|------------|
| paranoid | cold-start.md | completion.md |
| balanced | cold-start-optimized.md | completion-optimized.md |
| autopilot | cold-start-silent.md | completion-silent.md |
| verbose | cold-start.md | completion.md |
| silent | cold-start-silent.md | completion-silent.md |

## Migration from v1.x

- v1.x settings don't have `preset` field
- Default preset is `verbose` (matches v1.x behavior)
- Existing settings are preserved as overrides
- No action required from users

## Adding New Presets

1. Add definition to `presets.json`
2. Document in this file
3. Add to settings.schema.json enum
4. Update apply-preset.md if new behaviors needed
5. Update documentation

## Related Decisions

- `execution-mode-decision.md` - Why dual mode exists
- `silent-mode-philosophy.md` - Philosophy behind silent preset
