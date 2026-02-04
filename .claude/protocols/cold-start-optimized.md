# Cold Start Protocol - Optimized Mode

> Session Initialization Protocol (Optimized Variant)
> For preset: balanced
> Version: 2.0

## Philosophy

> "Key information only. No noise."

This protocol shows essential information without verbose step-by-step output. Users see what matters: project state, next task, any issues.

## Execution

### Step 1: Check for Crashes

Read `.claude/.last_session`:

**If crash detected:**
```
⚠️ Previous session incomplete

Last: Implementing user authentication
Changes: 5 files (+127 lines)

[R]ecover | [C]ommit | [S]tash
>
```

**If clean:** Continue silently.

### Step 2: Mark Session Active

Update `.claude/.last_session`:
```json
{
  "status": "active",
  "timestamp": "2026-02-04T10:30:00Z",
  "preset": "balanced"
}
```

### Step 3: Load Context

Load silently:
- `dev-docs/snapshot.md`
- `dev-docs/to-do.md` (incomplete tasks)

### Step 4: Check Git Status

```bash
git status --porcelain
git diff --stat
```

### Step 5: Present Summary

```
┌─────────────────────────────────────────┐
│ Project Name                            │
│ Phase 2: Core Implementation            │
│                                         │
│ Next: Add user authentication (TRD 3.1) │
│                                         │
│ ⚡ 3 uncommitted files                  │
└─────────────────────────────────────────┘
```

**If no uncommitted changes:**
```
┌─────────────────────────────────────────┐
│ Project Name                            │
│ Phase 2: Core Implementation            │
│                                         │
│ Next: Add user authentication (TRD 3.1) │
└─────────────────────────────────────────┘
```

**If blockers exist:**
```
┌─────────────────────────────────────────┐
│ Project Name                            │
│ Phase 2: Core Implementation            │
│                                         │
│ Next: Add user authentication (TRD 3.1) │
│                                         │
│ ⚠️ Blocker: Waiting for API spec        │
└─────────────────────────────────────────┘
```

### Step 6: Ready

No explicit "ready" message. Summary box indicates readiness.

## Comparison

| Information | Verbose | Optimized | Silent |
|-------------|---------|-----------|--------|
| Project name | ✓ | ✓ | ✗ |
| Current phase | ✓ | ✓ | ✗ |
| Next task | ✓ | ✓ | ✗ |
| Last completed | ✓ | ✗ | ✗ |
| Uncommitted indicator | ✓ (detailed) | ✓ (count) | ✗ |
| Blockers | ✓ | ✓ | ✗ |
| Loading steps | ✓ | ✗ | ✗ |
| Git status detail | ✓ | ✗ | ✗ |
| Ready message | ✓ | ✗ | ✗ |

## What's Hidden

Compared to verbose mode, optimized hides:
- "Checking crash recovery..."
- "Loading dev-docs/snapshot.md..."
- "Loading dev-docs/to-do.md..."
- "Checking git status..."
- "Session ready!"
- Detailed git diff stats
- Last completed task
- Full blocker descriptions

## What's Shown

Essential information only:
- Project identity (name, phase)
- Immediate next action
- Uncommitted work indicator
- Critical blockers

## Error Handling

### Missing Files
```
⚠️ snapshot.md not found

Run /migrate-legacy to initialize.
```

### Corrupted State
```
⚠️ Cannot parse project state

Starting with minimal context.
Run /fi when done to rebuild state.
```

## Auto-Update

In balanced mode:
1. Check for updates silently
2. If available → apply automatically
3. Show brief notice:
```
Updated to v2.1.0
```

## Notes

- Crash recovery always shows full prompt (safety)
- Errors show with fix instructions
- Detailed info available via specific commands
- Switch presets anytime with `/apply-preset`
