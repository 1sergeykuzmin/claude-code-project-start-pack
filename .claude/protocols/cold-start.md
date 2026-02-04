# Cold Start Protocol

> Session Initialization Protocol
> Triggers: "start", "resume", "continue", "begin", or work request after idle

## Purpose

Efficiently restore project context when resuming work after a break, minimizing token usage while providing complete situational awareness.

## Execution Steps

### Step 0: Crash Recovery Check

Check for crashed previous session:

```
Read .claude/.last_session (if exists):
{
  "status": "active" | "clean",
  "timestamp": "ISO-8601",
  "lastTask": "task description",
  "uncommittedChanges": true | false
}
```

**If status is "active"** (previous session didn't complete properly):

```
⚠️ Previous session did not complete cleanly.

Last activity: [timestamp]
Last task: [lastTask]
Uncommitted changes: [yes/no]

Options:
1. Review and recover uncommitted work
2. Start fresh (changes preserved in git)
3. Show what happened
```

**If uncommitted changes exist:**
```bash
git status
git diff --stat
```

Offer to:
- Commit the pending changes
- Stash for later
- Review before deciding

**If status is "clean" or file doesn't exist:**
→ Proceed to Step 1

### Step 0.5: Mark Session Active

Create/update `.claude/.last_session`:
```json
{
  "status": "active",
  "timestamp": "[current ISO-8601]",
  "lastTask": null,
  "uncommittedChanges": false
}
```

This enables crash detection for the current session.

### Step 1: Load Project State

Read minimal context files in order:

```
1. dev-docs/snapshot.md    (~500 tokens)  - Current state
2. dev-docs/to-do.md       (~1000 tokens) - Incomplete tasks only
3. Relevant PRD/TRD        (~1500 tokens) - Current phase sections
                           ─────────────────
                  Target:  ~3000 tokens (vs ~15-20k full load)
```

### Step 2: Parse Current State

From `snapshot.md`, identify:
- Current phase (from to-do.md phases)
- Last completed task
- Next pending task
- Any documented blockers
- Key decisions made in previous sessions

### Step 3: Check for Uncommitted Work

```bash
git status
git diff --stat
```

If uncommitted changes exist:
- Alert user about pending changes
- Offer to review and commit before proceeding
- Or continue with current work

### Step 4: Present State Summary

Output concise status:

```
┌─────────────────────────────────────────┐
│ 📍 Project: [name from snapshot]        │
│ 📊 Phase: [N] - [Phase Name]            │
│ ✅ Last: [last completed task]          │
│ ➡️  Next: [next pending task]            │
│ ⚠️  Blockers: [any blockers or "None"]   │
│                                         │
│ Ready to continue?                      │
└─────────────────────────────────────────┘
```

### Step 5: Await User Direction

- If user confirms → Begin work on next task
- If user specifies different task → Adjust accordingly
- If user asks question → Answer using loaded context
- If user wants to review → Show more details

## On-Demand Context Loading

Load additional files only when needed:

| Trigger | Load |
|---------|------|
| Working on feature | Relevant PRD section |
| Technical question | Relevant TRD section |
| Architecture question | `dev-docs/architecture.md` |
| Full task list | Complete `dev-docs/to-do.md` |

## Context Priority

```
ALWAYS LOAD (Essential):
├── dev-docs/snapshot.md
└── dev-docs/to-do.md (incomplete tasks)

LOAD ON DEMAND (When Referenced):
├── dev-docs/prd.md
├── dev-docs/trd.md
└── dev-docs/architecture.md

NEVER AUTO-LOAD (User Request Only):
├── Full codebase
├── All test files
└── Historical dialogs
```

## Error Handling

### Missing snapshot.md
```
Project not initialized. Would you like to:
1. Run /prd to create requirements?
2. Start fresh session without context?
```

### Missing to-do.md
```
No task list found. Would you like to:
1. Run /to-do to generate tasks? (requires prd.md + trd.md)
2. Start with ad-hoc work?
```

### Corrupted State
```
Could not parse project state. Starting fresh session.
Consider running completion protocol after finishing work.
```

## Integration with Other Skills

After Cold Start, user can:
- `/autonomous-development` - Continue executing tasks
- `/fix <issue>` - Work on specific bug
- `/commit` - Commit pending changes
- Ask questions - Using loaded context

## Notes

- This protocol runs fresh each session, immune to context compaction
- Token budget should stay under 3000 for initial load
- Additional context loaded incrementally as needed
- State is preserved via `snapshot.md` updates during Completion Protocol
