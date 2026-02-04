# Claude Code Project Framework v1.1

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
| Commit Policy | `.claude/COMMIT_POLICY.md` | What can/cannot be committed |

## Protocol Routing

### Session Management

| Trigger | Action |
|---------|--------|
| `start`, `resume`, `continue`, `begin` | → Execute Cold Start Protocol |
| `done`, `finish`, `/fi`, `end session` | → Execute Completion Protocol |

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

### Code Commands

| Command | Purpose |
|---------|---------|
| `/feature <description>` | Plan and implement a new feature |
| `/fix <issue>` | Debug and fix issues |
| `/refactor [file]` | Improve code structure |
| `/explain [file]` | Explain how code works |
| `/optimize [file]` | Optimize performance |

### Quality Commands

| Command | Purpose |
|---------|---------|
| `/review [file]` | Manual code review checklist |
| `/security` | Run OWASP security audit |
| `/security-dialogs` | Deep AI credential scan |
| `/test` | Write and run tests |

### Git Commands

| Command | Purpose |
|---------|---------|
| `/commit` | Create structured git commit |
| `/pr` | Create pull request |
| `/release` | Manage version releases |

### Database Commands

| Command | Purpose |
|---------|---------|
| `/db:migrate` | Manage database migrations |

### Dialog Commands

| Command | Purpose |
|---------|---------|
| `/ui` | Browse exported dialogs |
| `/watch` | Auto-export dialogs in real-time |

### Framework Commands

| Command | Purpose |
|---------|---------|
| `/fi` | Finish session (trigger Completion Protocol) |
| `/migrate-legacy` | Migrate existing project to framework |
| `/upgrade-framework` | Update framework to latest version |
| `/bug-reporting` | Manage error reporting settings |
| `/analyze-bugs` | Analyze collected error logs |

### Best Practices

| Command | Purpose |
|---------|---------|
| `/vercel-react-best-practices` | React/Next.js performance patterns |
| `/web-design-guidelines` | Accessibility and UX compliance |

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
✓ Run Completion Protocol when ending a session (/fi)
```

### 4. Traceability
```
✓ Tasks MUST reference PRD/TRD sections (e.g., PRD FR-001, TRD 3.2)
✓ Commits SHOULD reference task IDs when applicable
```

### 5. Security
```
✓ COMMIT_POLICY.md defines what can/cannot be committed
✓ Pre-commit hook blocks sensitive files
✓ Run /security before releases
✓ Run /security-dialogs if credentials may have been exposed
```

## Workflow Patterns

### New Project Setup
```
1. /prd <product idea>     → Creates dev-docs/prd.md
2. /trd                    → Creates dev-docs/trd.md
3. /to-do                  → Creates dev-docs/to-do.md
4. /autonomous-development → Executes tasks
```

### Existing Project Onboarding
```
1. /migrate-legacy         → Analyzes project, creates framework files
2. Review generated docs   → Verify accuracy
3. /autonomous-development → Start working
```

### Daily Development Session
```
1. "start" or "resume"     → Cold Start Protocol (with crash recovery)
2. /autonomous-development → Work on tasks
3. /codex-review           → Review changes (per task)
4. /commit                 → Commit changes
5. /fi or "done"           → Completion Protocol
```

### New Feature
```
1. /feature <description>  → Plan implementation
2. Implement code          → Following the plan
3. /codex-review           → Review changes
4. /commit                 → Commit feature
```

### Quick Fix
```
1. /fix <issue>            → Debug and fix
2. /codex-review           → Review fix
3. /commit                 → Commit fix
```

### Security Audit
```
1. /security               → OWASP checklist audit
2. /security-dialogs       → Deep credential scan
3. Fix any findings        → Apply recommendations
4. /codex-review           → Verify fixes
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

## Security Layers

```
Layer 1: .gitignore           → Prevents tracking
Layer 2: COMMIT_POLICY.md     → Blocks staging
Layer 3: Pre-commit hook      → Regex pattern matching
Layer 4: /security-dialogs    → AI deep scan
Layer 5: /codex-review        → Code quality check
Layer 6: /security            → OWASP audit
```

### Never Commit
- `.env` files or environment secrets
- API keys or credentials
- `node_modules/` or build artifacts
- Dialog exports (may contain secrets)
- Personal configuration files

## Crash Recovery

If a session doesn't end cleanly (no `/fi` or "done"):
- Next Cold Start detects via `.claude/.last_session`
- Offers to recover uncommitted work
- Options: commit, stash, or review changes

## Configuration

Framework settings in `.claude/settings.json`:
- Protocol behavior (cold-start, completion)
- Review requirements
- Security scanning options
- Document paths
- Dialog export settings

## Git Hooks

Install security hooks:
```bash
.claude/scripts/install-git-hooks.sh
```

Provides:
- Pre-commit hook blocking sensitive files
- Pattern matching from COMMIT_POLICY.md

## File Structure

```
.claude/
├── commands/
│   ├── code/       (feature, fix, refactor, explain, optimize)
│   ├── git/        (commit, pr, release)
│   ├── quality/    (review, security, security-dialogs, test)
│   ├── db/         (migrate)
│   ├── dialog/     (ui, watch)
│   └── framework/  (fi, migrate-legacy, upgrade-framework, bug-reporting, analyze-bugs)
├── protocols/      (cold-start, completion, auto-triggers)
├── scripts/        (git hooks, utilities)
├── skills/         (prd, trd, to-do, autonomous-dev, codex-review, best-practices)
├── settings.json
└── COMMIT_POLICY.md
```

---

*Framework: claude-code-project-start-pack v1.1*
