# Claude Code Project Start Pack

A comprehensive framework for AI-assisted development with Claude Code. This starter pack provides structured workflows for the entire development lifecycle - from idea to production.

## Overview

```
Idea → PRD → TRD → Tasks → [Session: Start → Work → Review → Commit → End] → Ship
```

This framework combines:
- **Strategic Planning Skills** - Generate requirements, specifications, and task breakdowns
- **Session Management** - Efficiently resume work between sessions with minimal context loading
- **Autonomous Development** - Execute tasks with mandatory code review
- **Operational Commands** - Git workflows, debugging, refactoring, security audits

## Quick Start

### 1. New Project Setup
```bash
# Generate product requirements
/prd "A mobile app that helps users track their daily water intake"

# Generate technical specification
/trd

# Generate task breakdown
/to-do

# Start autonomous development
/autonomous-development
```

### 2. Daily Development Session
```bash
# Resume work (loads context efficiently)
"start" or "resume"

# Work on tasks
/autonomous-development

# Or use operational commands
/fix "bug in authentication"
/refactor src/components/UserProfile.tsx

# End session (saves state)
"done" or "finish"
```

## Features

### Planning Skills

| Skill | Command | Output |
|-------|---------|--------|
| Product Requirements | `/prd <idea>` | `dev-docs/prd.md` |
| Technical Specification | `/trd` | `dev-docs/trd.md` |
| Task Breakdown | `/to-do` | `dev-docs/to-do.md` |

### Session Management

| Protocol | Trigger | Purpose |
|----------|---------|---------|
| Cold Start | "start", "resume" | Load minimal context (~3k tokens) |
| Completion | "done", "finish" | Save state, update snapshot |
| Auto-triggers | Automatic | Detect session boundaries |

### Execution Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| Autonomous Dev | `/autonomous-development` | Execute tasks sequentially |
| Code Review | `/codex-review` | Validate changes (mandatory) |

### Operational Commands

| Category | Commands | Purpose |
|----------|----------|---------|
| Git | `/commit`, `/pr`, `/release` | Version control workflows |
| Code | `/fix`, `/refactor`, `/explain`, `/optimize` | Code improvements |
| Quality | `/security`, `/test` | Security audits, testing |
| Database | `/db:migrate` | Schema migrations |

### Best Practices

| Skill | Command | Purpose |
|-------|---------|---------|
| React/Next.js | `/vercel-react-best-practices` | Performance optimization |
| Web Design | `/web-design-guidelines` | Accessibility, UX compliance |

## Directory Structure

```
project-root/
├── .claude/
│   ├── skills/                    # Strategic skills
│   │   ├── prd/                   # Product requirements generator
│   │   ├── trd/                   # Technical spec generator
│   │   ├── to-do/                 # Task breakdown generator
│   │   ├── autonomous-development/# Task executor
│   │   ├── codex-review/          # Code review
│   │   ├── vercel-react-best-practices/
│   │   └── web-design-guidelines/
│   │
│   ├── commands/                  # Operational commands
│   │   ├── git/                   # commit, pr, release
│   │   ├── code/                  # fix, refactor, explain, optimize
│   │   ├── quality/               # security, test
│   │   └── db/                    # migrate
│   │
│   ├── protocols/                 # Session management
│   │   ├── cold-start.md
│   │   ├── completion.md
│   │   └── auto-triggers.md
│   │
│   └── settings.json              # Framework configuration
│
├── dev-docs/                      # Generated documentation
│   ├── prd.md                     # Product requirements
│   ├── trd.md                     # Technical specification
│   ├── to-do.md                   # Task breakdown
│   ├── snapshot.md                # Project state (live)
│   └── architecture.md            # Code structure (live)
│
├── dialog/                        # Conversation exports (gitignored)
│
└── CLAUDE.md                      # AI instruction router
```

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT INITIATION                        │
└─────────────────────────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │  /prd   │───────▶│  /trd   │───────▶│ /to-do  │
    │  (idea) │        │  (prd)  │        │(prd+trd)│
    └─────────┘        └─────────┘        └─────────┘
                                               │
┌─────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT SESSION                        │
└─────────────────────────────────────────────────────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    ▼                       ▼                       ▼
┌─────────┐           ┌───────────┐           ┌─────────┐
│ "start" │           │   WORK    │           │ "done"  │
│         │           │           │           │         │
│  Cold   │──────────▶│ /auto-dev │──────────▶│Complete │
│  Start  │           │ /fix      │           │Protocol │
│         │           │ /refactor │           │         │
└─────────┘           │ /commit   │           └─────────┘
                      └─────┬─────┘
                            │
                            ▼
                    ┌─────────────┐
                    │/codex-review│
                    │ (MANDATORY) │
                    └─────────────┘
```

## Key Concepts

### Document Traceability
Tasks in `to-do.md` reference PRD and TRD sections:
```markdown
- [ ] Implement user authentication (TRD 5.1, PRD FR-003)
```

### Mandatory Code Review
Every task must pass `/codex-review` before commit. This is enforced by the autonomous development skill.

### Session Continuity
The framework solves the "AI has no memory" problem:
- `snapshot.md` tracks project state
- Cold Start loads only necessary context (~3k tokens vs ~15-20k)
- Completion Protocol saves state for next session

### Token Efficiency
```
Cold Start loads:
├── snapshot.md      (~500 tokens)
├── to-do.md         (~1000 tokens, incomplete only)
└── Relevant PRD/TRD (~1500 tokens)
                     ─────────────
Total:               ~3000 tokens
```

## Configuration

Edit `.claude/settings.json` to customize:

```json
{
  "protocols": {
    "coldStart": { "enabled": true, "autoDetect": true },
    "completion": { "enabled": true, "exportDialog": true }
  },
  "review": {
    "compulsory": true,
    "maxRetries": 3
  },
  "security": {
    "credentialScan": true,
    "preCommitCheck": true
  }
}
```

## Requirements

- Claude Code CLI
- Git
- `tmux` and `codex` CLI (for code review)
- Node.js (for most projects)

## Credits

This framework combines concepts from:
- Original planning skills (PRD, TRD, To-Do)
- [claude-code-starter](https://github.com/alexeykrol/claude-code-starter) by Alexey Krol (session management, operational commands)
- [Vercel Engineering](https://vercel.com) (React best practices)

## License

MIT

---

*Built for AI-assisted development with Claude Code*
