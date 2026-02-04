# Auto-Trigger System

> Automatic Detection of Session Events
> Version: 1.0

## Purpose

Automatically detect when to invoke Cold Start or Completion protocols without requiring explicit user commands.

## Detection Mechanisms

### 1. Explicit Keywords (Immediate Trigger)

**Cold Start Triggers:**
- "start", "begin", "resume", "continue"
- "let's get started", "picking up where we left off"
- "what's next", "where were we"

**Completion Triggers:**
- "done", "finished", "complete", "ready"
- "that's all", "stop here", "end session"
- "let's commit", "wrap up"

### 2. Implicit Signals (Suggest, Don't Auto-Execute)

**Completion Indicators:**
- Task completion language: "feature is ready", "bug is fixed"
- Satisfaction markers: "looks good", "perfect", "exactly what I needed"
- Farewell patterns: "thanks", "great work", "talk later"

**Action:** Suggest running Completion Protocol, don't auto-execute.

### 3. Significant Changes Detection

Monitor for substantial work that should be preserved:

| Threshold | Action |
|-----------|--------|
| 100+ lines changed | Suggest commit |
| 5+ files modified | Suggest review + commit |
| New files created | Note in session summary |

**Check interval:** Every 5 user messages or after significant tool use.

### 4. Context Analysis

Analyze conversation flow for completion probability:

**High Probability (> 0.8):**
- Multiple tasks completed
- User expressing satisfaction
- Natural conversation winding down

**Medium Probability (0.5 - 0.8):**
- Single task completed
- User asking "what else" questions

**Action:**
- High → Suggest Completion Protocol
- Medium → Mention option to save progress

## Configuration Modes

Users can set behavior in `.claude/settings.json`:

```json
{
  "protocols": {
    "autoTriggers": {
      "enabled": true,
      "mode": "assisted"
    }
  }
}
```

| Mode | Behavior |
|------|----------|
| `manual` | Never auto-detect, wait for explicit commands |
| `assisted` | Suggest protocols, never auto-execute (default) |
| `proactive` | Auto-execute for explicit keywords, suggest for implicit |

## False Positive Prevention

**Do NOT trigger when:**
- Message contains questions (user seeking help)
- Message contains error reports
- Message requests changes or modifications
- No actual code changes exist
- AI recently asked questions awaiting answers
- User is in middle of explaining something

**Negative Indicators:**
- "but", "however", "also need"
- "can you", "please", "could you"
- "error", "bug", "issue", "problem"
- "wait", "hold on", "actually"

## Trigger Flow

```
User Message
    │
    ▼
┌─────────────────────┐
│ Check Explicit      │
│ Keywords            │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
  Match      No Match
    │           │
    ▼           ▼
┌─────────┐ ┌─────────────────┐
│ Execute │ │ Check Implicit  │
│ Protocol│ │ Signals         │
└─────────┘ └────────┬────────┘
                     │
               ┌─────┴─────┐
               │           │
               ▼           ▼
           Detected    Not Detected
               │           │
               ▼           ▼
        ┌──────────┐   Continue
        │ Check    │   Normal
        │ Negative │   Operation
        │ Indicators│
        └────┬─────┘
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
    Present    Suppress
       │       Suggestion
       ▼
┌──────────────┐
│ Suggest      │
│ Protocol     │
│ (Don't Auto) │
└──────────────┘
```

## Suggestion Format

When suggesting a protocol:

**Cold Start:**
```
It looks like you're starting a new session. Would you like me to:
• Load your project state and show where you left off?
• Or dive straight into your request?
```

**Completion:**
```
Nice progress! You've [completed N tasks / made significant changes].
Would you like to:
• Save your progress and update project state?
• Continue working?
```

## Logging

When enabled, auto-trigger decisions are logged for debugging:

```
[Auto-Trigger] Message analyzed
  - Explicit keywords: none
  - Implicit signals: satisfaction (0.7)
  - Negative indicators: none
  - Decision: suggest_completion (confidence: 0.7)
```

## Notes

- Auto-triggers are suggestions, not commands
- User always has final say
- Designed to reduce friction, not add it
- Can be disabled entirely if preferred
