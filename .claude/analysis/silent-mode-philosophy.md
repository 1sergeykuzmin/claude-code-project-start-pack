# Silent Mode Philosophy

## Status
Accepted

## Date
2026-02-04

## Core Principle

> "Users should forget the framework exists."

Silent mode is designed around the idea that protocol overhead should be imperceptible. The framework should work invisibly in the background, surfacing only when user input is genuinely required.

## Philosophy

### The Problem with Verbose Output

Traditional verbose protocols create cognitive overhead:

```
✓ Checking crash recovery...
✓ Loading context files...
✓ Verifying git hooks...
✓ Checking for updates...
✓ Initializing session...
✓ Session ready!
```

This output:
- Interrupts flow state
- Demands user attention
- Creates waiting time
- Adds visual noise
- Provides little actionable value (99% of the time)

### The Silent Mode Solution

Silent mode inverts the default:

```
[nothing]
```

Output only appears when:
1. **User input required** - Crash recovery decision
2. **Critical error** - Something failed that needs fixing
3. **Meaningful result** - Commit hash after completion

### When to Show Output

| Scenario | Verbose Mode | Silent Mode |
|----------|--------------|-------------|
| Initialization success | All steps | Nothing |
| Initialization failure | Error + steps | Error + fix |
| Crash recovery needed | Warning + steps | Warning + options |
| Update available | Notice + confirm | Auto-apply |
| Commit success | Summary + hash | Hash only |
| Commit failure | Error + details | Error + details |
| Review passed | Full report | Nothing |
| Review failed | Full report | Failures only |

### Measuring Success

**Quantitative:**
- Protocol overhead: 10-12 min/session → imperceptible
- Confirmations required: 10+ → 0-1
- User attention demand: constant → negligible

**Qualitative:**
- User forgets protocols exist
- Framework feels like infrastructure, not a tool
- Flow state maintained

## Implementation

### Silent Cold Start

1. Run 10 parallel initialization tasks
2. Parse JSON results
3. If all success → no output
4. If crash detected → show recovery prompt
5. If error → show error with fix instructions
6. If update available → auto-apply

### Silent Completion

1. Run 3 parallel finalization tasks
2. Update metafiles in background
3. Run review silently
4. If review passes → auto-commit
5. If review fails → show failures only
6. Output: commit hash or nothing

### Invariants in Silent Mode

Even in silent mode, some things cannot be skipped:

| Invariant | Behavior |
|-----------|----------|
| `/codex-review` | Runs silently, shows failures only |
| Security scan | Runs silently, shows critical findings |
| Git hooks | Execute normally |

## User Experience Design

### Progressive Disclosure

Information is revealed only when needed:

```
Level 0: Nothing (success)
Level 1: Result only (commit hash)
Level 2: Warning (needs attention)
Level 3: Error (needs action)
Level 4: Full output (requested or debug)
```

### Escape Hatches

Users can always:
- Set `preset: verbose` for full output
- Run specific commands to see details
- Check logs in `.claude/logs/`

### Clear Error Messages

When errors occur, silent mode provides actionable output:

```
❌ Build failed

src/index.ts:42 - Type error
  Expected 'string', got 'number'

Fix the error and run again.
```

Not verbose noise, but clear next steps.

## Trade-offs

### Accepted
- Users don't see what's happening (by design)
- Debugging requires checking logs
- May feel "magical" or opaque to new users

### Mitigated
- Verbose mode available for debugging
- Logs capture all details
- Errors always surface with context

### Rejected
- Showing "minimal" output (defeats purpose)
- Progress indicators (still demands attention)
- Success confirmations (unnecessary)

## Philosophical Alignment

Silent mode aligns with:

1. **Unix Philosophy**: Do one thing well, quietly
2. **Progressive Web Apps**: Invisible until needed
3. **Good Infrastructure**: You notice it when it breaks

The best framework is one you don't think about.

## Related Decisions

- `execution-mode-decision.md` - Why we offer both modes
- `preset-system-design.md` - How silent preset is configured
- `python-core-decision.md` - Why fast execution enables silent mode
