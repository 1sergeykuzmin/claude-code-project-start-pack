# Claude Code Project Framework v1.0

> AI Instruction Router - Auto-loaded by Claude Code

## Overview

This framework provides a complete AI-assisted development lifecycle:

```
Idea → PRD → TRD → Tasks → [Session: Start → Work → Review → Commit → End] → Ship
```

## Quick Reference

| Document | Path | Purpose |
|----------|------|---------|
| PRD | `dev-docs/prd.md` | Product requirements |
| TRD | `dev-docs/trd.md` | Technical specification |
| Tasks | `dev-docs/to-do.md` | Development tasks |
| Snapshot | `dev-docs/snapshot.md` | Current project state |
| Architecture | `dev-docs/architecture.md` | Code structure |

## Protocol Routing

### Session Management

| Trigger | Action |
|---------|--------|
| `start`, `resume`, `continue`, `begin` | → Execute Cold Start Protocol |
| `done`, `finish`, `end session`, `stop` | → Execute Completion Protocol |

### Planning Skills

| Command | Purpose |
|---------|---------|
| `/prd <idea>` | Generate Product Requirements Document |
| `/trd` | Generate Technical Requirements Document |
| `/to-do` | Generate task breakdown from PRD + TRD |

### Execution Skills

| Command | Purpose |
|---------|---------|
| `/autonomous-development` | Execute tasks with mandatory review |
| `/codex-review` | Run code review (COMPULSORY after each task) |

### Operational Commands

| Command | Purpose |
|---------|---------|
| `/commit` | Create structured git commit |
| `/pr` | Create pull request |
| `/fix` | Debug and fix issues |
| `/refactor` | Improve code structure |
| `/security` | Run security audit |
| `/release` | Manage version releases |
| `/test` | Write and run tests |
| `/explain` | Explain code |
| `/optimize` | Optimize performance |

## Core Rules

### 1. Mandatory Code Review
```
⚠️ NEVER commit without running /codex-review first
```

### 2. Document Updates
```
✓ ALWAYS update dev-docs/snapshot.md after completing tasks
✓ ALWAYS update dev-docs/to-do.md when marking tasks complete
```

### 3. Session Management
```
✓ Run Cold Start when resuming after a break
✓ Run Completion Protocol when ending a session
```

### 4. Traceability
```
✓ Tasks MUST reference PRD/TRD sections (e.g., PRD FR-001, TRD 3.2)
✓ Commits SHOULD reference task IDs when applicable
```

## Workflow Patterns

### New Project Setup
```
1. /prd <product idea>     → Creates dev-docs/prd.md
2. /trd                    → Creates dev-docs/trd.md
3. /to-do                  → Creates dev-docs/to-do.md
4. /autonomous-development → Executes tasks
```

### Daily Development Session
```
1. "start" or "resume"     → Cold Start Protocol
2. /autonomous-development → Work on tasks
3. /codex-review           → Review changes (per task)
4. /commit                 → Commit changes
5. "done" or "finish"      → Completion Protocol
```

### Quick Fix
```
1. /fix <issue>            → Debug and fix
2. /codex-review           → Review fix
3. /commit                 → Commit fix
```

## Document Dependencies

```
                 ┌─────────┐
                 │  /prd   │
                 └────┬────┘
                      │
                      ▼
                 ┌─────────┐
                 │  /trd   │ ← reads prd.md
                 └────┬────┘
                      │
                      ▼
                 ┌─────────┐
                 │ /to-do  │ ← reads prd.md + trd.md
                 └────┬────┘
                      │
                      ▼
              ┌──────────────┐
              │ /autonomous- │ ← reads to-do.md + snapshot.md
              │ development  │
              └──────────────┘
```

## Security Guidelines

### Never Commit
- `.env` files or environment secrets
- API keys or credentials
- `node_modules/` or build artifacts
- Personal configuration files

### Always Check
- Run `/security` before major releases
- Review changes with `/codex-review`
- Validate no secrets in committed code

## Configuration

Framework settings are in `.claude/settings.json`. Customize:
- Protocol behavior (cold-start, completion)
- Review requirements
- Security scanning options
- Document paths

## Best Practices Skills

The framework includes best practices for:
- **React/Next.js**: `/vercel-react-best-practices`
- **Web Design**: `/web-design-guidelines`

Use these when building UI components.

---

*Framework: claude-code-project-start-pack v1.0*
