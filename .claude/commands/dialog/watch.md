# Watch Command (Dialog Monitor)

Monitor and automatically export Claude Code dialogs in real-time.

## Usage

```
/watch
```

## Purpose

Continuously monitors Claude Code sessions and automatically:
- Exports new dialogs to `dialog/` directory
- Converts to readable Markdown format
- Adds exports to `.gitignore`
- Tracks session statistics

## How It Works

### Step 1: Start Watcher

```bash
# The command starts a background process that monitors:
# ~/.claude/projects/ for new session files
```

### Step 2: Monitor Output

```
┌─────────────────────────────────────────────────────────────────┐
│ Dialog Watcher                                         [Active] │
├─────────────────────────────────────────────────────────────────┤
│ Watching: ~/.claude/projects/                                   │
│ Export to: ./dialog/                                            │
│                                                                  │
│ Recent Activity:                                                 │
│ [10:15:32] New session detected: abc123                         │
│ [10:45:12] Session updated: abc123 (+15 messages)               │
│ [11:00:00] Session exported: dialog/2024-01-15-abc123.md        │
│                                                                  │
│ Statistics:                                                      │
│ Sessions today: 2 | Messages: 45 | Exports: 1                   │
│                                                                  │
│ Press Ctrl+C to stop                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Auto-Export

When a session ends or reaches a checkpoint:
1. Converts JSONL format to Markdown
2. Applies credential redaction
3. Saves to `dialog/[date]-[session-id].md`
4. Updates `.gitignore` if needed

## Export Format

Generated Markdown files contain:

```markdown
# Development Session: 2024-01-15

> Session ID: abc123
> Duration: 2h 15m
> Project: my-project

## Summary
- Tasks completed: 3
- Files changed: 12
- Commits: 2

## Conversation

### User (10:15:32)
Let's implement the user authentication feature.

### Claude (10:15:45)
I'll help you implement authentication. Let me first review
the technical requirements...

[Tool Call: Read dev-docs/trd.md]

Based on the TRD, we need:
1. JWT-based authentication
2. Refresh token rotation
...

### User (10:20:15)
Looks good, please proceed.

...
```

## Privacy Features

### Automatic Credential Redaction

The watcher scans exports for:
- API keys → `[REDACTED_API_KEY]`
- Passwords → `[REDACTED_PASSWORD]`
- Tokens → `[REDACTED_TOKEN]`
- Private keys → `[REDACTED_KEY]`

### Git Protection

Exports are automatically:
1. Added to `dialog/.gitignore`
2. Excluded from commits via `COMMIT_POLICY.md`
3. Blocked by pre-commit hook

## Stopping the Watcher

```
Ctrl+C - Stop the watcher gracefully
```

The watcher will:
1. Complete any in-progress export
2. Save final statistics
3. Exit cleanly

## Background Mode

To run the watcher in the background:

```bash
# Start in background
/watch &

# Or use nohup
nohup /watch > watch.log 2>&1 &

# Check if running
ps aux | grep watch

# Stop background watcher
kill $(pgrep -f "watch")
```

## Configuration

In `.claude/settings.json`:
```json
{
  "dialog": {
    "exportPath": "dialog/",
    "autoExport": true,
    "exportFormat": "markdown",
    "redactCredentials": true,
    "watchInterval": 5000
  }
}
```

## Comparison with /fi Export

| Feature | /watch | /fi export |
|---------|--------|------------|
| Timing | Real-time | End of session |
| Trigger | Automatic | Manual/protocol |
| Scope | All sessions | Current session |
| Background | Yes | No |

**Recommendation:** Use `/watch` during active development periods. Use `/fi` for single-session exports.

## Troubleshooting

### Watcher not detecting sessions
```
1. Check Claude Code is running
2. Verify ~/.claude/projects/ exists
3. Ensure read permissions on directory
```

### Exports not appearing
```
1. Check dialog/ directory exists
2. Verify write permissions
3. Check disk space
```

### High CPU usage
```
# Increase watch interval in settings
"watchInterval": 10000  // 10 seconds instead of 5
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/watch` | Auto-export dialogs (this command) |
| `/ui` | Browse exported dialogs |
| `/fi` | Manual export on session end |
