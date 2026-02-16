🌐 **Language:** English | [Русский](README.ru.md)

# Claude Code Project Framework

**Go from idea to working code with one conversation.**

```
You: /prd A CLI tool that converts markdown to PDF
     ↓  (or /prd --team for multi-agent mode)
Claude: Creates requirements, technical spec, tasks
     ↓
You: /autonomous-development
     ↓
Claude: Builds everything, reviews code, commits each step
     ↓
You: Working code with tests ✓
```

No more "AI forgot what we discussed." No more broken commits. No more managing the AI — let it manage the project.

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

---

## Quick Start

**Install** (pick one):

```bash
# New project
git clone https://github.com/1sergeykuzmin/claude-code-project-start-pack.git my-app
cd my-app && rm -rf .git && git init

# Existing project
curl -fsSL https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack/main/install.sh | bash
```

**Try it:**

```bash
claude
```

```
You: /prd A personal finance tracker

Claude: I'll create a Product Requirements Document.
        First, a few questions...
```

That's it. You're using the framework.

---

## The 5 Main Commands

These commands form the core workflow:

```
/prd → /trd → /to-do → /autonomous-development
                              ↓
                        /codex-review (automatic)
```

---

### `/prd` — Describe Your Idea

Turns your idea into a structured Product Requirements Document.

```
You: /prd A mobile app for tracking daily water intake

Claude: I'll help create a PRD. Let me ask a few questions:

        1. Target platforms? (iOS, Android, web?)
You: iOS and Android

Claude: 2. Key features beyond basic tracking?
You: Reminders, daily goals, weekly stats

Claude: 3. Any integrations?
You: Apple Health and Google Fit

Claude: ✓ Created dev-docs/prd.md

        Summary:
        - 8 functional requirements defined
        - 4 non-functional requirements
        - 3 user personas identified
        - Success metrics established
```

**What you get:** `dev-docs/prd.md` — a complete product spec you can share with stakeholders or use as the source of truth.

Add `--team` for multi-perspective generation with AI specialists:

```
You: /prd --team A marketplace for handmade goods
```

Uses 3 core agents (Product Strategist, UX Researcher, Tech Analyst) plus up to 3 auto-detected domain specialists (SEO, Mobile, Enterprise, etc.) with quality gates.

---

### `/trd` — Plan the Technical Approach

Turns your PRD into a Technical Requirements Document.

```
You: /trd

Claude: Analyzing PRD...

        ✓ Created dev-docs/trd.md

        Architecture decisions:
        - Framework: React Native + Expo
        - Database: SQLite (local) + optional cloud sync
        - APIs: HealthKit, Google Fit
        - Auth: Biometric + email fallback

        Security review:
        - Health data encryption: Required
        - API key storage: Secure keychain
        - Data retention: User-controlled
```

**What you get:** `dev-docs/trd.md` — technical blueprint with architecture, dependencies, and security considerations.

Add `--team` for architect + reviewer collaboration:

```
You: /trd --team
```

Lead architect drafts the full TRD, reviewers validate each section, and optional specialists (Security, Database, Performance) audit their domains.

---

### `/to-do` — Break It Into Tasks

Turns your TRD into a prioritized task list.

```
You: /to-do

Claude: Breaking down the technical requirements...

        ✓ Created dev-docs/to-do.md

        Phase 1: Foundation (4 tasks)
        - [ ] T-001 Initialize React Native project [M] (TRD 2.1)
        - [ ] T-002 Set up SQLite schema [M] (TRD 3.1)
        - [ ] T-003 Create navigation structure [S] (TRD 2.2)
        - [ ] T-004 Implement auth flow [L] (TRD 4.1, PRD FR-005)

        Phase 2: Core Features (5 tasks)
        - [ ] T-005 Water logging screen [M] (PRD FR-001)
        - [ ] T-006 Daily goal system [S] (PRD FR-002)
        - [ ] T-007 Reminder notifications [L] (PRD FR-003)
        ...

        12 tasks total across 3 phases
        Complexity: 3S / 5M / 3L / 1XL
```

**What you get:** `dev-docs/to-do.md` — each task has a stable ID, complexity tag, and traces back to PRD/TRD sections. Tasks are sliced vertically by feature, not horizontally by tech layer.

Add `--team` for a Decomposer + Validator pair that reviews coverage and quality. Add `--update` to re-generate while preserving existing task IDs and completion statuses.

---

### `/autonomous-development` — Build Everything

Executes ALL tasks automatically in a continuous loop.

```
You: /autonomous-development

Claude: Starting continuous execution...

        ┌─────────────────────────────────────────────┐
        │ LOOP: Find Task → Build → Review → Commit  │
        │       ↑_______________________________↓     │
        └─────────────────────────────────────────────┘

        → Task 1/12: Initialize React Native project
          Creating project structure...
          Adding dependencies...
          Running /codex-review... ✓ Passed
          Committed: "feat: Initialize React Native with Expo"

        → Task 2/12: Set up SQLite schema
          Writing database models...
          Running /codex-review... ⚠ Issue found
          Auto-fixing: Added missing index
          Running /codex-review... ✓ Passed
          Committed: "feat: Add SQLite database schema"

        → Task 3/12: Create navigation structure
          ...

        [Continues until ALL tasks complete]

        ✓ All 12 tasks complete
        ✓ 12 commits created
        ✓ Ready for release
```

**Key behavior:**
- Runs until ALL tasks are done (not just one)
- Automatically runs code review after each task
- Auto-fixes issues (up to 3 attempts)
- Only stops when: all done, unfixable error, or you interrupt

---

### `/codex-review` — Quality Gate

Validates code before every commit. Runs automatically during `/autonomous-development`, but you can also run it manually.

```
You: /codex-review

Claude: Running code review...

        Checking:
        ✓ Syntax valid
        ✓ No security vulnerabilities
        ✓ No hardcoded secrets
        ✓ Tests pass (14/14)
        ⚠ Warning: Function 'processData' is 67 lines

        Suggestion: Consider breaking into smaller functions.

        Result: PASS (1 warning)
```

**This is mandatory.** Every task must pass review before commit — no exceptions, regardless of settings.

---

## Team Mode

Add `--team` to any planning command for multi-agent generation:

| Command | Team Model | Agents |
|---------|-----------|--------|
| `/prd --team` | Research + Debate | 3 core + up to 3 specialists |
| `/trd --team` | Draft + Review | 1 architect + 1-2 reviewers + specialists |
| `/to-do --team` | Decompose + Validate | 1 decomposer + 1 validator |

Each agent brings a different perspective. The lead synthesizes everything into the final document with quality gates.

Requires: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings (enabled by default).

---

## Session Management

The framework remembers where you left off.

### Starting a Session

```
You: start

Claude: Loading your project...

        ✓ Context loaded (3,241 tokens)
        ✓ Git status: clean
        ✓ 4 tasks remaining in Phase 2

        Ready to continue. Run /autonomous-development
        or ask me anything about the project.
```

Other trigger words: `resume`, `continue`, `begin`

### Ending a Session

```
You: done

Claude: Wrapping up...

        ✓ All changes committed
        ✓ Snapshot updated
        ✓ Session saved

        Progress: 8/12 tasks complete
        Next time: Phase 2, Task 5 (Reminder notifications)
```

Other trigger words: `finish`, `/fi`, `end session`

### Why This Matters

| Without Session Management | With Session Management |
|---------------------------|------------------------|
| Claude loads entire codebase (~15k tokens) | Loads smart summary (~3k tokens) |
| No memory of previous work | Knows exactly where you left off |
| Lost work if you forget to commit | Automatic crash recovery |

### Crash Recovery

Forgot to say `done`? No problem.

```
You: start

Claude: ⚠ Found incomplete session from yesterday

        Uncommitted changes:
        - src/notifications.ts (new)
        - src/api/health.ts (modified)

        What would you like to do?
        1. Commit and continue
        2. Stash and start fresh
        3. Review changes first

You: 1

Claude: ✓ Committed: "feat: Add notification system"
        Continuing where you left off...
```

---

## Other Useful Commands

### Adding Features to Existing Code

```
You: /feature Add dark mode support

Claude: I'll plan this feature. A few questions...
        [Asks 2-3 clarifying questions]

        ✓ Updated PRD with new requirements
        ✓ Updated TRD with implementation approach
        ✓ Added 4 tasks to to-do.md

        Starting /autonomous-development...
```

### Quick Fixes

| Command | What It Does |
|---------|--------------|
| `/fix "login not working"` | Debug and fix specific issues |
| `/refactor auth.ts` | Improve code structure |
| `/explain api/` | Understand how code works |
| `/optimize utils.ts` | Performance improvements |
| `/test users` | Write tests for a module |

### Git Shortcuts

| Command | What It Does |
|---------|--------------|
| `/commit` | Structured commit with proper message |
| `/pr` | Create pull request |
| `/release` | Bump version and tag |

### Security

| Command | What It Does |
|---------|--------------|
| `/security` | Run OWASP security audit |
| `/security-dialogs` | Check for leaked credentials in conversations |

### For Existing Projects

```
You: /migrate-legacy

Claude: Analyzing your codebase...

        ✓ Found: Next.js 14 app, 47 components, PostgreSQL
        ✓ Generated dev-docs/prd.md (reverse-engineered)
        ✓ Generated dev-docs/trd.md (architecture analysis)

        Ready for /feature or /autonomous-development
```

---

## Configuration

### Presets

Choose how much Claude confirms with you:

| Preset | Behavior | Best For |
|--------|----------|----------|
| `balanced` | Confirms important actions | Daily work (default) |
| `autopilot` | Minimal confirmations | Fast prototyping |
| `paranoid` | Confirms everything | Production code |
| `verbose` | Full output, all confirmations | Debugging |
| `silent` | Minimal output | CI/CD pipelines |

Set in `.claude/settings.json`:

```json
{
  "preset": "balanced"
}
```

**Note:** Code review is **always required** regardless of preset.

### Key Files

| File | Purpose |
|------|---------|
| `dev-docs/prd.md` | Product requirements |
| `dev-docs/trd.md` | Technical specification |
| `dev-docs/to-do.md` | Task breakdown |
| `dev-docs/snapshot.md` | Current project state |
| `.claude/settings.json` | Framework configuration |

---

## Installation

### New Project

```bash
git clone https://github.com/1sergeykuzmin/claude-code-project-start-pack.git my-project
cd my-project && rm -rf .git && git init
```

### Existing Project

```bash
curl -fsSL https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack/main/install.sh | bash
```

### Installer Options

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview without making changes |
| `--minimal` | Only install `.claude/` folder |
| `--update` | Refresh existing installation |
| `--force` | Overwrite without prompts |
| `--no-hooks` | Skip git hooks |

### Requirements

**Required:**
- Claude Code CLI
- Python 3.8+
- Git

**Optional:**
- Node.js 18+ (for dialog web UI)

---

## Origins & Credits

This framework combines two approaches to AI-assisted development:

### Planning Skills

The idea-to-execution pipeline:

| Skill | Purpose |
|-------|---------|
| `/prd` | Generate Product Requirements from ideas |
| `/trd` | Generate Technical Specification from PRD |
| `/to-do` | Break down into actionable tasks |
| `/autonomous-development` | Execute all tasks in continuous loop |
| `/codex-review` | Mandatory code review gate |

### Starter Architecture

Session management and operational commands based on [claude-code-starter](https://github.com/alexeykrol/claude-code-starter) by [Alexey Krol](https://github.com/alexeykrol):

- Session protocols (Cold Start, Completion, crash recovery)
- Operational commands (`/commit`, `/pr`, `/fix`, `/refactor`)
- Document conventions (`snapshot.md`, `architecture.md`)
- Security layers (pre-commit hooks, commit policies)

### The Combination

```
┌─────────────────────────────────────────────────────┐
│         Claude Code Project Framework               │
├─────────────────────────────────────────────────────┤
│  PLANNING                                           │
│  /prd → /trd → /to-do → /autonomous-development    │
├─────────────────────────────────────────────────────┤
│  SESSIONS (based on claude-code-starter)            │
│  start → work → done (with crash recovery)          │
├─────────────────────────────────────────────────────┤
│  COMMANDS                                           │
│  /commit, /pr, /fix, /refactor, /security           │
└─────────────────────────────────────────────────────┘
```

---

## License

MIT

---

*Built for AI-assisted development with Claude Code*
