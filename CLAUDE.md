# Claude Code Project Framework v2.0

> AI Instruction Router - Auto-loaded by Claude Code

## Overview

This framework provides a complete AI-assisted development lifecycle:

```
Idea → PRD → TRD → Tasks → [Session: Start → Work → Review → Commit → End] → Ship
```

## What's New in v2.0

- **Preset System** - Choose behavior profile (paranoid, balanced, autopilot, verbose, silent)
- **Silent Mode** - Zero output on success for flow-state optimization
- **Parallel Execution** - Python core runs 10 tasks simultaneously
- **Enhanced Auto-Triggers** - AI-based completion detection
- **TypeScript Dialog Exporter** - Standalone tools for dialog management

## Quick Reference

| Document | Path | Purpose |
|----------|------|---------|
| PRD | `dev-docs/prd.md` | Product requirements |
| TRD | `dev-docs/trd.md` | Technical specification |
| Tasks | `dev-docs/to-do.md` | Development tasks |
| Snapshot | `dev-docs/snapshot.md` | Current project state |
| Architecture | `dev-docs/architecture.md` | Code structure |
| Commit Policy | `.claude/COMMIT_POLICY.md` | What can/cannot be committed |
| Presets | `.claude/presets.json` | Preset definitions |

## Preset System

Choose a preset to control framework behavior:

| Preset | Output | Confirmations | Auto-Triggers | Best For |
|--------|--------|---------------|---------------|----------|
| **paranoid** | Full | All | Disabled | Sensitive projects |
| **balanced** | Optimized | Single | Suggest | Daily development |
| **autopilot** | Silent | Minimal | Execute | Personal projects |
| **verbose** | Full | All | Suggest | Debugging (DEFAULT) |
| **silent** | None | None | Execute | Flow state |

### Set Preset

In `.claude/settings.json`:
```json
{
  "preset": "balanced"
}
```

Or via command:
```
/apply-preset balanced
```

### Preset Behaviors

| Behavior | paranoid | balanced | autopilot | verbose | silent |
|----------|----------|----------|-----------|---------|--------|
| Cold start | All steps | Summary | Nothing | All steps | Nothing |
| Completion | All steps | Summary | Hash only | All steps | Hash only |
| Commit | Confirm | Once | Auto | Confirm | Auto |
| Push | Confirm | Once | Once | Confirm | Auto |
| PR | Confirm | Confirm | Confirm | Confirm | Confirm |

### Invariants (Cannot Override)

These settings are locked regardless of preset:
- `review.compulsory = true` - /codex-review is ALWAYS mandatory
- `protocols.completion.requireReview = true` - Review before commit required

## Protocol Routing

Protocols are selected based on active preset:

| Preset | Cold Start Protocol | Completion Protocol |
|--------|---------------------|---------------------|
| paranoid, verbose | `cold-start.md` | `completion.md` |
| balanced | `cold-start-optimized.md` | `completion-optimized.md` |
| autopilot, silent | `cold-start-silent.md` | `completion-silent.md` |

### Session Triggers

| Trigger | Action |
|---------|--------|
| `start`, `resume`, `continue`, `begin` | → Execute Cold Start Protocol |
| `done`, `finish`, `/fi`, `end session` | → Execute Completion Protocol |

## Commands

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
| `/ui` | Browse exported dialogs (localhost:3333) |
| `/watch` | Auto-export dialogs in real-time |

### Framework Commands

| Command | Purpose |
|---------|---------|
| `/fi` | Finish session (trigger Completion Protocol) |
| `/apply-preset <name>` | Apply a preset configuration |
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
This rule applies to ALL presets, including silent and autopilot.
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

**Note:** In silent/autopilot mode, crash recovery is the one situation that always shows output.

## Configuration

### settings.json

Framework settings in `.claude/settings.json`:

```json
{
  "preset": "verbose",
  "execution": {
    "mode": "verbose",
    "parallelism": true,
    "pythonPath": "auto"
  },
  "autoUpdate": {
    "enabled": true,
    "confirmBeforeUpdate": true
  },
  "protocols": { ... },
  "review": { ... },
  "security": { ... }
}
```

### .framework-config

Runtime state in `.claude/.framework-config`:
- Active preset
- Python/Node detection status
- Session statistics
- Last update check

## Requirements

### Required
- Python 3.8+ (for parallel execution)
- Git 2.x
- Claude Code CLI

### Optional
- Node.js 18+ (for TypeScript dialog exporter)

## File Structure

```
.claude/
├── commands/
│   ├── code/       (feature, fix, refactor, explain, optimize)
│   ├── git/        (commit, pr, release)
│   ├── quality/    (review, security, security-dialogs, test)
│   ├── db/         (migrate)
│   ├── dialog/     (ui, watch)
│   └── framework/  (fi, apply-preset, migrate-legacy, upgrade, bugs)
├── protocols/
│   ├── cold-start.md           (verbose)
│   ├── cold-start-optimized.md (balanced)
│   ├── cold-start-silent.md    (silent)
│   ├── completion.md           (verbose)
│   ├── completion-optimized.md (balanced)
│   ├── completion-silent.md    (silent)
│   ├── auto-triggers.md
│   ├── apply-preset.md
│   ├── settings-migration.md
│   └── router.md
├── analysis/       (architectural decision records)
├── scripts/        (git hooks, utilities)
├── skills/         (prd, trd, to-do, autonomous-dev, codex-review)
├── settings.json
├── settings.schema.json
├── presets.json
├── .framework-config
└── COMMIT_POLICY.md
```

## Migration from v1.x

v1.x settings are automatically migrated:
1. Existing settings preserved
2. New fields added with defaults
3. Default preset: `verbose` (matches v1.x behavior)
4. Backup created: `.claude/settings.json.v1.backup`

No action required - migration happens on first cold start.

## Git Hooks

Install security hooks:
```bash
.claude/scripts/install-git-hooks.sh
```

Provides:
- Pre-commit hook blocking sensitive files
- Pattern matching from COMMIT_POLICY.md

---

*Framework: claude-code-project-start-pack v2.0*
