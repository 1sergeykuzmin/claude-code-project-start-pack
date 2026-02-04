# Completion Protocol - Silent Mode

> Session Finalization Protocol (Silent Variant)
> For presets: autopilot, silent
> Version: 2.0

## Philosophy

> "Show the commit hash. Nothing else."

This protocol completes sessions with minimal output:
- Success → commit hash only (or nothing if no changes)
- Failure → error with fix instructions
- Review failures → findings only

## Execution

### Step 1: Invoke Python Core

```bash
python3 src/framework-core/main.py completion --silent
```

### Step 2: Parallel Tasks (3 total)

Run simultaneously:

| Task | Purpose | On Failure |
|------|---------|------------|
| `build_check` | Verify build passes | Show error |
| `dialog_export` | Export current session | Log, continue |
| `security_scan` | Scan for credentials | Show critical only |

### Step 3: Sequential Tasks

After parallel tasks complete:

#### 3a. Update Metafiles (Silent)

Update without output:
- `dev-docs/snapshot.md` - Current state
- `dev-docs/to-do.md` - Mark completed tasks
- `dev-docs/architecture.md` - If structural changes

#### 3b. Run Code Review (MANDATORY)

```bash
# /codex-review runs silently
# Output only if review FAILS
```

**If review passes:**
```
[No output]
```

**If review fails:**
```
❌ Review failed

src/auth.ts:42
  Security: Hardcoded credential detected

src/api.ts:156
  Error handling: Unhandled promise rejection

Fix issues and run again.
```

#### 3c. Commit Changes

**If changes exist and review passed:**
```bash
git add [files per COMMIT_POLICY.md]
git commit -m "[generated message]"
```

**Output (success):**
```
abc1234
```

Just the commit hash. Nothing else.

**Output (no changes):**
```
[No output]
```

**Output (commit failed):**
```
❌ Commit failed: pre-commit hook rejected

.env file detected in staging.
Remove with: git reset HEAD .env
```

#### 3d. Mark Session Clean

Update `.claude/.last_session`:
```json
{
  "status": "clean",
  "timestamp": "2026-02-04T11:30:00Z",
  "lastTask": "Implemented user authentication",
  "uncommittedChanges": false
}
```

## Auto-Trigger Detection

In silent mode, completion can trigger automatically:

### Explicit Keywords (Immediate)
- "done", "finished", "готово", "complete"
- Auto-execute completion without confirmation

### Implicit Signals (With Confirmation)
- Task completion phrases
- Satisfaction markers
- Natural conversation ending

```
Work complete. Commit? [Y/n]
```

Single character response, then silent completion.

### Significant Changes
- 100+ lines changed
- 5+ files modified
- 30+ minutes since last commit

```
Significant changes detected. Commit? [Y/n]
```

## Output Summary

| Scenario | Output |
|----------|--------|
| Success, changes committed | `abc1234` |
| Success, no changes | (nothing) |
| Build failed | Error + fix |
| Review failed | Findings only |
| Commit blocked | Error + fix |
| Security critical | Warning + details |

## Comparison with Verbose

| Step | Verbose | Silent |
|------|---------|--------|
| Check uncommitted | "Checking changes..." | (nothing) |
| Run review | Full report | Failures only |
| Update snapshot | "Updating snapshot..." | (nothing) |
| Stage files | List of files | (nothing) |
| Commit | Message + stats | Hash only |
| Session summary | Full box | (nothing) |

## Error Handling

### Build Failure
```
❌ Build failed

src/index.ts:42 - Type error
  Expected 'string', got 'number'

Fix and run /fi again.
```

### Review Failure
```
❌ Review found issues

[List of findings]

Fix issues and run /fi again.
```

### Security Critical
```
⚠️ CRITICAL: Credential detected

src/config.ts:12
  API_KEY = "sk-live-xxx..."

Remove credential before commit.
```

### Commit Policy Violation
```
❌ Blocked by COMMIT_POLICY.md

Cannot commit: .env.local

Remove from staging: git reset HEAD .env.local
```

## Logging

All activity logged to `.claude/logs/completion/`:
```json
{
  "timestamp": "2026-02-04T11:30:00Z",
  "preset": "silent",
  "tasks": [...],
  "review_result": "passed",
  "commit_hash": "abc1234",
  "duration_ms": 1250
}
```

## Invariants

Even in silent mode:
- `/codex-review` ALWAYS runs (shows failures only)
- Security scan ALWAYS runs (shows critical only)
- COMMIT_POLICY.md ALWAYS enforced
- Pre-commit hook ALWAYS executes

## Push Behavior

Based on preset:

| Preset | Auto-Push | Output |
|--------|-----------|--------|
| autopilot | After confirm | `origin/main abc1234` |
| silent | Auto (no confirm) | (nothing) |

**Push failure:**
```
❌ Push failed: rejected by remote

Pull first: git pull --rebase origin main
```

## Notes

- Review is mandatory - cannot be skipped
- Critical security always surfaces
- Logs capture full details
- Hash output enables scripting/automation
- Switch to verbose with `/apply-preset verbose`
