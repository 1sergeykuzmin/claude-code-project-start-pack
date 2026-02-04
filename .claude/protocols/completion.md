# Completion Protocol

> Session Finalization Protocol
> Triggers: "done", "finish", "end session", "stop", or detected session end

## Purpose

Safely conclude a development session by reviewing changes, updating project state, and preparing for the next session.

## Execution Steps

### Step 1: Check Uncommitted Changes

```bash
git status
git diff --stat
```

**If uncommitted changes exist:**
1. Run `/codex-review` to validate changes
2. If review passes → Prompt for `/commit`
3. If review fails → Report findings, ask user how to proceed

**If no changes:**
→ Skip to Step 3

### Step 2: Commit Pending Work

If user approves commit:
1. Stage relevant files (selective, not `git add .`)
2. Create commit with conventional message
3. Verify commit success

```bash
git log -1 --stat
```

### Step 3: Update Snapshot

Update `dev-docs/snapshot.md` with:

```markdown
## Current State

| Attribute | Value |
|-----------|-------|
| Project | [name] |
| Phase | [current phase from to-do] |
| Status | [In Progress/Blocked/Complete] |
| Last Task | [what was just completed] |
| Next Task | [next pending task] |
| Blockers | [any blockers encountered] |

## Session History

| Date | Duration | Tasks Completed | Commits | Notes |
|------|----------|-----------------|---------|-------|
| [today] | [duration] | [count] | [count] | [brief notes] |

## Quick Context

### What Exists
[Updated summary of implemented functionality]

### What's Next
[Updated next steps]

### Key Decisions This Sprint
[Any new decisions made]
```

### Step 4: Update To-Do

Mark completed tasks in `dev-docs/to-do.md`:
- Change `- [ ]` to `- [x]` for completed tasks
- Add completion date if tracking

### Step 5: Update Architecture (If Structural Changes)

If new files, modules, or significant restructuring occurred:
- Update `dev-docs/architecture.md` with new components
- Document any new patterns or conventions introduced

### Step 6: Export Dialog (Optional)

If configured in settings:
1. Export conversation to `dialog/[date]-[session-id].md`
2. Ensure dialog directory has `.gitignore`
3. Redact any credentials from export

### Step 7: Present Session Summary

```
┌─────────────────────────────────────────┐
│ 📊 Session Summary                      │
│ ─────────────────                       │
│ ⏱️  Duration: [time estimate]            │
│ ✅ Completed: [N] tasks                 │
│ 📝 Commits: [N]                         │
│ 📄 Files changed: [N]                   │
│                                         │
│ 🔜 Next session:                        │
│    [Next task description]              │
│                                         │
│ State saved. See you next time!         │
└─────────────────────────────────────────┘
```

## Auto-Detection Triggers

The Completion Protocol may be suggested when:

### Explicit Keywords
- "done", "finished", "complete"
- "that's all", "stop here"
- "end session", "signing off"

### Implicit Signals
- Task completion language
- Satisfaction markers ("great", "perfect", "looks good")
- Natural conversation ending

### Activity-Based
- Extended idle time with uncommitted changes
- Multiple completed tasks without commit

## Error Handling

### Uncommitted Risky Changes
```
⚠️ Uncommitted changes detected that include:
- [sensitive file patterns]

Please review before committing or discard.
```

### Review Failures
```
Code review found issues:
[List of issues]

Options:
1. Fix issues now
2. Commit anyway (not recommended)
3. Discard changes
4. End session without commit
```

### Cannot Update Snapshot
```
Warning: Could not update snapshot.md
Session state may not be preserved for next time.
```

## Checklist

Before completing session:
- [ ] All work committed (or intentionally left uncommitted)
- [ ] Code review passed (`/codex-review`)
- [ ] Snapshot updated with current state
- [ ] To-do list reflects completed tasks
- [ ] No sensitive data in committed files

## Integration

The Completion Protocol ensures:
- Cold Start Protocol has accurate state to load
- `/autonomous-development` knows where to resume
- Team members can understand project state
- No work is lost between sessions
