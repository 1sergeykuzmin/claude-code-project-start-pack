# Cold Start Protocol - Silent Mode

> Session Initialization Protocol (Silent Variant)
> For presets: autopilot, silent
> Version: 2.0

## Philosophy

> "Users should forget the framework exists."

This protocol produces **zero output on success**. Output appears only when:
1. Crash recovery decision needed
2. Critical error requiring user action
3. Update available (auto-applies silently)

## Execution

### Step 1: Invoke Python Core

```bash
python3 src/framework-core/main.py cold-start --silent
```

**If Python unavailable:**
```
❌ Python 3.8+ required for silent mode.

Install Python or switch to verbose preset:
  "preset": "verbose"

https://www.python.org/downloads/
```

### Step 2: Parse Results

Python core returns JSON:

```json
{
  "status": "success" | "error" | "user_input_required",
  "tasks": [
    {"name": "crash_detection", "status": "success", "data": {...}},
    {"name": "context_load", "status": "success", "data": {...}},
    ...
  ],
  "total_duration_ms": 359,
  "user_prompt": null | "crash_recovery_needed"
}
```

### Step 3: Handle Results

#### Success (99% of cases)
```
[No output - immediately ready to work]
```

#### Crash Recovery Needed
```
⚠️ Previous session did not complete cleanly.

Last activity: 2026-02-04 10:30:00
Last task: Implementing user authentication
Uncommitted changes: Yes (5 files, +127 lines)

[R]ecover and review changes
[C]ommit pending work now
[S]tart fresh (changes preserved in git stash)
>
```

#### Critical Error
```
❌ Cold start failed: Cannot read dev-docs/snapshot.md

Fix: Run /migrate-legacy to initialize framework files.
```

#### Update Available
```
[Auto-downloads and installs update silently]
[No output unless update fails]
```

### Step 4: Mark Session Active

Create `.claude/.last_session`:
```json
{
  "status": "active",
  "timestamp": "2026-02-04T10:30:00Z",
  "lastTask": null,
  "uncommittedChanges": false,
  "preset": "silent"
}
```

## Parallel Tasks (10 total)

All run simultaneously via Python ThreadPoolExecutor:

| Task | Purpose | On Failure |
|------|---------|------------|
| `migration_cleanup` | Check incomplete migrations | Log, continue |
| `crash_detection` | Read .last_session | Show recovery prompt |
| `version_check` | Compare versions | Auto-update |
| `security_cleanup` | Quick security scan | Log findings |
| `dialog_export` | Export pending dialogs | Log, continue |
| `commit_policy_verify` | Check COMMIT_POLICY.md | Log warning |
| `git_hooks_install` | Ensure hooks present | Install silently |
| `config_init` | Initialize .framework-config | Create defaults |
| `context_load` | Load snapshot.md, to-do.md | Fail if missing |
| `session_activate` | Create .last_session | Always succeeds |

## Context Loading

Files loaded silently:
- `dev-docs/snapshot.md` - Current state
- `dev-docs/to-do.md` - Incomplete tasks only

Files loaded on-demand (when referenced):
- `dev-docs/prd.md`
- `dev-docs/trd.md`
- `dev-docs/architecture.md`

## Auto-Update Behavior

In silent mode, updates are aggressive:

1. Check for updates (background)
2. If available → download silently
3. Apply update silently
4. Log to `.claude/logs/updates/`
5. No user notification

**Exception:** Major version updates (2.x → 3.x) always prompt.

## Error Logging

All activity logged to `.claude/logs/cold-start/`:
```
.claude/logs/cold-start/
└── 2026-02-04.json
```

Users can check logs for debugging:
```bash
cat .claude/logs/cold-start/$(date +%Y-%m-%d).json | jq
```

## Fallback to Verbose

If silent mode encounters repeated failures:
1. Log failure count
2. After 3 failures → suggest switching to verbose
3. User can debug with full output

```
⚠️ Silent mode failed 3 times.

Run with verbose output for debugging:
  /apply-preset verbose
  start
```

## Integration with Skills

After silent cold start completes:
- `/prd`, `/trd`, `/to-do` work normally
- `/autonomous-development` starts silently
- `/codex-review` runs silently (shows failures only)
- All commands function identically

## Comparison with Verbose

| Aspect | Verbose | Silent |
|--------|---------|--------|
| Initialization steps | Shown | Hidden |
| Context loaded | Listed | Hidden |
| Git status | Shown | Hidden |
| Ready message | Yes | No |
| Crash recovery | Verbose prompt | Minimal prompt |
| Errors | Full context | Error + fix only |

## Notes

- Crash recovery ALWAYS shows prompt (safety requirement)
- Critical errors ALWAYS surface (can't hide failures)
- Logs capture everything for debugging
- Switch to verbose anytime with `/apply-preset verbose`
