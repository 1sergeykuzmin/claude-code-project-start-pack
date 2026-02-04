# Completion Protocol - Optimized Mode

> Session Finalization Protocol (Optimized Variant)
> For preset: balanced
> Version: 2.0

## Philosophy

> "Summary, not step-by-step."

This protocol shows a brief session summary without verbose progress output. Users see what was accomplished and the result.

## Execution

### Step 1: Check Uncommitted Changes

```bash
git status --porcelain
```

**If no changes:**
```
No changes to commit.

Session ended.
```
Skip to Step 6.

### Step 2: Run Code Review (MANDATORY)

```bash
# /codex-review runs
```

**If passes:** Continue silently.

**If fails:**
```
Review found issues:

src/auth.ts:42 - Security issue
src/api.ts:156 - Error handling

Fix and run /fi again.
```

### Step 3: Update Metafiles

Update silently:
- `dev-docs/snapshot.md`
- `dev-docs/to-do.md`

### Step 4: Commit

**Single confirmation:**
```
Commit 5 files (+127 lines)?

feat: Add user authentication

[Y/n]
```

**On confirm:**
```bash
git add [files]
git commit -m "feat: Add user authentication..."
```

### Step 5: Session Summary

```
┌─────────────────────────────────────────┐
│ Session Complete                        │
│                                         │
│ ✓ 2 tasks completed                     │
│ ✓ Committed: abc1234                    │
│ → Next: Implement password reset        │
└─────────────────────────────────────────┘
```

**If no tasks completed:**
```
┌─────────────────────────────────────────┐
│ Session Complete                        │
│                                         │
│ ✓ Committed: abc1234                    │
│ → Next: Add user authentication         │
└─────────────────────────────────────────┘
```

### Step 6: Mark Session Clean

Update `.claude/.last_session`:
```json
{
  "status": "clean",
  "timestamp": "2026-02-04T11:30:00Z"
}
```

## Comparison

| Information | Verbose | Optimized | Silent |
|-------------|---------|-----------|--------|
| "Checking changes..." | ✓ | ✗ | ✗ |
| Review full report | ✓ | Failures only | Failures only |
| "Updating snapshot..." | ✓ | ✗ | ✗ |
| Commit confirmation | Always | Once | Never |
| Staged files list | ✓ | ✗ | ✗ |
| Commit message shown | ✓ | ✓ (brief) | ✗ |
| Commit hash | ✓ | ✓ | ✓ |
| Session summary box | Detailed | Brief | ✗ |
| Tasks completed | ✓ | Count only | ✗ |
| Duration | ✓ | ✗ | ✗ |
| Files changed count | ✓ | In confirm | ✗ |

## Auto-Trigger Behavior

In balanced mode, auto-triggers **suggest** but don't execute:

```
Looks like you're done. Save progress? [Y/n]
```

Single keypress to confirm, then optimized completion runs.

## What's Hidden

Compared to verbose mode, optimized hides:
- Step-by-step progress
- Detailed file listings
- Full review report (shows failures only)
- Duration tracking
- Detailed session statistics

## What's Shown

Essential information only:
- Commit confirmation (once)
- Brief commit message
- Task completion count
- Commit hash
- Next task indicator

## Error Handling

### Build Failure
```
Build failed:

src/index.ts:42 - Type error

Fix and run /fi again.
```

### Review Failure
```
Review found issues:

[Brief list of findings]

Fix and run /fi again.
```

### Commit Failure
```
Commit blocked:

.env file in staging area.

Fix: git reset HEAD .env
```

## Push Behavior

In balanced mode, push requires one confirmation:

```
Push to origin/main? [Y/n]
```

**On confirm:**
```
Pushed: origin/main abc1234
```

## Notes

- Review is mandatory - always runs
- Single confirmation for commit
- Summary shows what matters
- Full details in logs if needed
- Switch presets with `/apply-preset`
