# Fi Command (Finish)

Shortcut to trigger the Completion Protocol for ending a development session.

## Usage

```
/fi
```

This is equivalent to saying "done" or "finish" but as an explicit command.

## What It Does

The `/fi` command triggers the Completion Protocol (`.claude/protocols/completion.md`), which:

### 1. Checks for Uncommitted Changes
```bash
git status
git diff --stat
```

If changes exist:
- Runs `/codex-review` to validate
- Prompts for commit if review passes
- Reports issues if review fails

### 2. Updates Project State

Updates `dev-docs/snapshot.md` with:
- Last completed task
- Next pending task
- Session duration
- Tasks completed this session
- Any blockers encountered

### 3. Updates Task List

Ensures `dev-docs/to-do.md` reflects:
- Completed tasks marked with `[x]`
- Phase summary updated if phase complete

### 4. Exports Dialog (Optional)

If configured in settings:
- Saves conversation to `dialog/`
- Redacts credentials
- Auto-adds to .gitignore

### 5. Marks Session Completed

Creates/updates `.claude/.last_session`:
```json
{
  "status": "completed",
  "task": "Implement user authentication",
  "timestamp": "2024-01-15T10:30:00Z",
  "pid": null,
  "metadata": {
    "completed_at": "2024-01-15T10:30:00Z"
  }
}
```

### 6. Displays Session Summary

```
┌─────────────────────────────────────────┐
│ 📊 Session Summary                      │
│ ─────────────────                       │
│ ⏱️  Duration: ~2h                        │
│ ✅ Completed: 3 tasks                   │
│ 📝 Commits: 2                           │
│ 📄 Files changed: 12                    │
│                                         │
│ 🔜 Next session:                        │
│    Create dashboard API endpoints       │
│                                         │
│ State saved. See you next time!         │
└─────────────────────────────────────────┘
```

## When to Use

Use `/fi` when:
- Ending a coding session
- Taking a break (save progress)
- Switching to a different project
- Before closing the terminal

## Alternative Triggers

These all trigger the same Completion Protocol:
- `/fi`
- "done"
- "finish"
- "end session"
- "stop"
- "that's all"

## Workflow Example

```
# Work on tasks
/autonomous-development

# ... implement features ...

# End session
/fi

# Output:
# ✅ Uncommitted changes reviewed and committed
# ✅ Snapshot updated
# ✅ Tasks marked complete
# ✅ Session state saved
```

## Skip Behaviors

The completion protocol will skip certain steps if not needed:

| Condition | Skipped Steps |
|-----------|---------------|
| No uncommitted changes | Review, commit |
| No tasks completed | Task update |
| Dialog export disabled | Dialog export |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/fi` | End session (this command) |
| "start" | Begin session (Cold Start) |
| `/commit` | Just commit, don't end session |
| `/codex-review` | Just review, don't end session |

## Configuration

In `.claude/settings.json`:
```json
{
  "protocols": {
    "completion": {
      "enabled": true,
      "autoCommit": false,      // Prompt before commit
      "exportDialog": true,     // Save conversation
      "updateSnapshot": true    // Update project state
    }
  }
}
```
