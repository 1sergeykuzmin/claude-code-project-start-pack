# Auto-Trigger System

> Automatic Detection of Session Events
> Version: 2.0

## Purpose

Automatically detect when to invoke Cold Start or Completion protocols without requiring explicit user commands. Enhanced with AI-based completion detection and multi-language support.

## Configuration

Settings in `.claude/settings.json`:

```json
{
  "protocols": {
    "autoTriggers": {
      "enabled": true,
      "mode": "assisted",
      "completionConfidenceThreshold": 0.8,
      "analyzeLastMessages": 10,
      "idleTimeThreshold": 300
    }
  }
}
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabled` | boolean | true | Enable/disable auto-trigger system |
| `mode` | string | "assisted" | Detection mode (see below) |
| `completionConfidenceThreshold` | float | 0.8 | Minimum confidence to suggest completion (0.0-1.0) |
| `analyzeLastMessages` | int | 10 | Number of recent messages to analyze for context |
| `idleTimeThreshold` | int | 300 | Seconds of inactivity before suggesting state save |

## Detection Modes

| Mode | Behavior |
|------|----------|
| `manual` | Never auto-detect, wait for explicit commands |
| `assisted` | Suggest protocols, never auto-execute (default) |
| `proactive` | Auto-execute for explicit keywords, suggest for implicit |
| `silent` | Log decisions but never interrupt (for silent presets) |

## Preset Integration

Auto-trigger behavior adapts to active preset:

| Preset | Mode Override | Output |
|--------|---------------|--------|
| verbose | assisted | Full suggestions with explanations |
| balanced | assisted | Concise suggestions |
| autopilot | proactive | Minimal prompts, auto-execute when confident |
| silent | silent | No suggestions (logged only) |
| paranoid | manual | Always require explicit commands |

---

## Detection Mechanisms

### 1. Explicit Keywords (Immediate Trigger)

**Cold Start Triggers (English):**
- "start", "begin", "resume", "continue"
- "let's get started", "picking up where we left off"
- "what's next", "where were we"

**Cold Start Triggers (Russian):**
- "начнём", "начинаем", "продолжим", "продолжаем"
- "давай начнём", "где мы остановились"
- "что дальше", "с чего начать"

**Completion Triggers (English):**
- "done", "finished", "complete", "ready"
- "that's all", "stop here", "end session"
- "let's commit", "wrap up"

**Completion Triggers (Russian):**
- "готово", "сделано", "завершено", "закончил"
- "хватит", "всё", "достаточно"
- "давай закоммитим", "заверши сессию"

### 2. Implicit Signals (Suggest, Don't Auto-Execute)

**Completion Indicators:**
- Task completion language: "feature is ready", "bug is fixed", "функция готова"
- Satisfaction markers: "looks good", "perfect", "exactly what I needed", "отлично", "идеально"
- Farewell patterns: "thanks", "great work", "talk later", "спасибо", "пока"

**Action:** Suggest running Completion Protocol, don't auto-execute.

### 3. Significant Changes Detection

Monitor for substantial work that should be preserved:

| Threshold | Action |
|-----------|--------|
| 100+ lines changed | Suggest commit |
| 5+ files modified | Suggest review + commit |
| New files created | Note in session summary |
| 50+ lines in single file | Suggest intermediate save |

**Check interval:** Every 5 user messages or after significant tool use.

### 4. AI-Based Completion Analysis

Analyze the last N messages (configurable via `analyzeLastMessages`) for completion probability:

**Scoring Factors:**

| Factor | Weight | Description |
|--------|--------|-------------|
| Task completion language | +0.3 | User says task is done |
| Satisfaction expressions | +0.2 | User expresses positive sentiment |
| Decreasing request rate | +0.15 | Fewer commands in recent messages |
| Question absence | +0.1 | User not asking more questions |
| Farewell patterns | +0.15 | User signaling end of conversation |
| Pending requests | -0.3 | Outstanding work mentioned |
| Error context | -0.25 | Recent errors discussed |

**Confidence Thresholds:**

| Probability | Action |
|-------------|--------|
| ≥ 0.9 | Auto-suggest Completion (strong) |
| 0.8 - 0.9 | Suggest Completion if `completionConfidenceThreshold` met |
| 0.5 - 0.8 | Mention option to save progress |
| < 0.5 | Continue normal operation |

### 5. Idle Time Monitoring

Detect session inactivity to prevent lost work:

```
┌─────────────────────────────────────────────────┐
│ Idle Detection Flow                              │
├─────────────────────────────────────────────────┤
│                                                  │
│  Last user message timestamp                     │
│           │                                      │
│           ▼                                      │
│  ┌─────────────────────┐                        │
│  │ Current time -      │                        │
│  │ Last message time   │                        │
│  └──────────┬──────────┘                        │
│             │                                    │
│     ┌───────┴───────┐                           │
│     │               │                           │
│     ▼               ▼                           │
│  < threshold    ≥ threshold                     │
│     │               │                           │
│     ▼               ▼                           │
│  Continue      Check unsaved work               │
│                    │                            │
│             ┌──────┴──────┐                     │
│             │             │                     │
│             ▼             ▼                     │
│          Has work     No work                   │
│             │             │                     │
│             ▼             ▼                     │
│       Suggest save    Silent                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## False Positive Prevention

**Do NOT trigger when:**
- Message contains questions (user seeking help)
- Message contains error reports
- Message requests changes or modifications
- No actual code changes exist
- AI recently asked questions awaiting answers
- User is in middle of explaining something
- Conversation is about planning (not execution)
- Recent context shows ongoing debugging

**Negative Indicators (English):**
- "but", "however", "also need"
- "can you", "please", "could you"
- "error", "bug", "issue", "problem"
- "wait", "hold on", "actually"
- "not yet", "still working", "one more thing"

**Negative Indicators (Russian):**
- "но", "однако", "ещё нужно"
- "можешь", "пожалуйста"
- "ошибка", "баг", "проблема"
- "подожди", "стоп", "на самом деле"
- "ещё не всё", "работаю над", "ещё одно"

---

## Trigger Flow

```
User Message
    │
    ▼
┌─────────────────────────────────┐
│ 1. Check Language               │
│    (English/Russian/Other)      │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│ 2. Check Explicit Keywords      │
│    (in detected language)       │
└─────────────┬───────────────────┘
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
      Match      No Match
        │           │
        ▼           ▼
┌───────────┐ ┌─────────────────────┐
│ Check     │ │ 3. Check Implicit   │
│ Negative  │ │    Signals          │
│ Override  │ └──────────┬──────────┘
└─────┬─────┘            │
      │            ┌─────┴─────┐
      │            │           │
      ▼            ▼           ▼
┌───────────┐  Detected    Not Detected
│ Execute   │      │           │
│ Protocol  │      ▼           ▼
│ (if mode  │ ┌──────────┐   Continue
│ allows)   │ │ 4. AI    │   Normal
└───────────┘ │ Analysis │   Operation
              │ (last N  │
              │ messages)│
              └────┬─────┘
                   │
                   ▼
              ┌─────────────────────┐
              │ 5. Calculate        │
              │ Confidence Score    │
              └──────────┬──────────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
         ≥ 0.8      0.5-0.8        < 0.5
            │            │            │
            ▼            ▼            ▼
       Suggest      Mention       Silent
       Protocol     Option
```

---

## Suggestion Formats

### Cold Start (Verbose Mode)

```
It looks like you're starting a new session. Would you like me to:
• Load your project state and show where you left off?
• Or dive straight into your request?
```

### Cold Start (Balanced Mode)

```
Session detected. Load previous state? (Run `/cold-start` or continue directly)
```

### Completion (Verbose Mode)

```
Nice progress! You've [completed N tasks / made significant changes].
Would you like to:
• Save your progress and update project state?
• Continue working?
```

### Completion (Balanced Mode)

```
Ready to save? [N files changed, M tasks done] → Run `/completion` or continue
```

### Idle Warning

```
You have unsaved changes (N files modified). Would you like to save progress?
```

---

## Logging

When enabled, auto-trigger decisions are logged:

```
[Auto-Trigger] Message analyzed
  - Language: en
  - Explicit keywords: none
  - Implicit signals: satisfaction (0.7), farewell (0.4)
  - Negative indicators: none
  - Message window: last 10 analyzed
  - Confidence score: 0.78
  - Threshold: 0.80
  - Decision: mention_option (below threshold)
```

**Log Location:** `.claude/.framework-log` (if logging enabled in preset)

---

## Integration Points

### With Protocol Router

The auto-trigger system feeds into the protocol router:

```
Auto-Trigger Detection
        │
        ▼
┌───────────────────┐
│ Protocol Router   │ ← Checks active preset
└────────┬──────────┘
         │
    ┌────┴────┬──────────┐
    │         │          │
    ▼         ▼          ▼
 Silent   Optimized   Verbose
 Variant   Variant    Variant
```

### With Preset System

Auto-trigger respects preset invariants:
- **Paranoid preset:** Always manual mode, never auto-trigger
- **Silent preset:** Logs triggers but never suggests
- **Autopilot preset:** Auto-executes high-confidence triggers

---

## Notes

- Auto-triggers are suggestions, not commands (except in autopilot mode)
- User always has final say
- Designed to reduce friction, not add it
- Can be disabled entirely if preferred
- Multi-language support can be extended
- Confidence thresholds are tunable per project
