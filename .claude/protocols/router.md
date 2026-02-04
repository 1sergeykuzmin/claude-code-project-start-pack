# Protocol Router

> Selects appropriate protocol variant based on active preset
> Version: 2.0

## Purpose

Routes session triggers to the correct protocol variant based on the active preset configuration.

## Routing Logic

### Step 1: Determine Active Preset

Check in order:
1. `.claude/.framework-config` → `active_preset`
2. `.claude/settings.json` → `preset`
3. Default: `"verbose"`

### Step 2: Route to Protocol

#### Cold Start Routing

| Preset | Protocol File |
|--------|---------------|
| `paranoid` | `cold-start.md` |
| `verbose` | `cold-start.md` |
| `balanced` | `cold-start-optimized.md` |
| `autopilot` | `cold-start-silent.md` |
| `silent` | `cold-start-silent.md` |

#### Completion Routing

| Preset | Protocol File |
|--------|---------------|
| `paranoid` | `completion.md` |
| `verbose` | `completion.md` |
| `balanced` | `completion-optimized.md` |
| `autopilot` | `completion-silent.md` |
| `silent` | `completion-silent.md` |

### Step 3: Execute Protocol

Load and execute the selected protocol file.

## Trigger Detection

### Cold Start Triggers
- Explicit: `start`, `resume`, `continue`, `begin`
- Implicit: Work request after idle, session boundary detection

### Completion Triggers
- Explicit: `done`, `finish`, `/fi`, `end session`
- Implicit: Task completion signals, satisfaction markers

## Auto-Trigger Behavior by Preset

| Preset | Cold Start | Completion |
|--------|------------|------------|
| `paranoid` | Manual only | Manual only |
| `verbose` | Auto-detect, suggest | Auto-detect, suggest |
| `balanced` | Auto-detect, suggest | Auto-detect, suggest |
| `autopilot` | Auto-detect, execute explicit | Auto-detect, execute explicit |
| `silent` | Auto-detect, execute all | Auto-detect, execute all |

## Settings Override

Users can override protocol behavior in `settings.json`:

```json
{
  "preset": "silent",
  "execution": {
    "mode": "optimized"  // Override: use optimized instead of silent
  }
}
```

Override priority:
1. `execution.mode` (if set)
2. Preset default
3. Framework default (`verbose`)

## Protocol Selection Matrix

```
                    ┌─────────────────────────────────────────┐
                    │           Active Preset                  │
                    ├─────────┬─────────┬─────────┬───────────┤
                    │ paranoid│ balanced│autopilot│  silent   │
                    │ verbose │         │         │           │
┌───────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Cold Start        │ verbose │optimized│ silent  │  silent   │
├───────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Completion        │ verbose │optimized│ silent  │  silent   │
├───────────────────┼─────────┼─────────┼─────────┼───────────┤
│ Auto-Trigger Mode │ manual/ │assisted │proactive│ proactive │
│                   │ assisted│         │         │           │
└───────────────────┴─────────┴─────────┴─────────┴───────────┘
```

## Python Core Integration

For silent and optimized modes, Python core provides execution:

```bash
# Silent mode (global flags must come BEFORE subcommand)
python3 src/framework-core/main.py --silent cold-start
python3 src/framework-core/main.py --silent completion

# Optimized mode (uses Python for speed, Claude for output)
python3 src/framework-core/main.py --json cold-start
# Parse JSON, format optimized output
```

## Fallback Handling

### Python Unavailable

If Python not found and silent/autopilot preset active:

```
Python 3.8+ required for silent mode.

Options:
1. Install Python: https://www.python.org/downloads/
2. Switch to verbose: /apply-preset verbose

Using verbose mode for this session.
```

Then route to verbose protocol.

### Protocol File Missing

If protocol file not found:

```
Warning: cold-start-optimized.md not found
Falling back to cold-start.md
```

Fallback chain:
1. Requested protocol
2. Verbose protocol
3. Inline minimal protocol

## Logging

Router decisions logged to `.claude/logs/router/`:

```json
{
  "timestamp": "2026-02-04T10:30:00Z",
  "trigger": "start",
  "detected_preset": "balanced",
  "selected_protocol": "cold-start-optimized.md",
  "overrides_applied": [],
  "fallbacks_used": []
}
```

## Integration

The router is invoked:
1. When session trigger detected
2. When `/apply-preset` changes preset
3. On first run (determine default)

## Notes

- Router runs before protocol execution
- Preset can change mid-session with `/apply-preset`
- Logs help debug routing decisions
- Fallbacks ensure graceful degradation
