# Claude Code Project Start Pack

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

A comprehensive framework for AI-assisted development with Claude Code. This starter pack provides structured workflows for the entire development lifecycle - from idea to production.

## What's New in v2.0

- **10x Faster Session Management** - Python-based parallel execution (10 tasks in ~350ms)
- **Preset System** - 5 behavior presets for different workflows
- **TypeScript Dialog Exporter** - Web UI for browsing conversations
- **Enhanced Security** - 6-layer protection against credential leaks
- **Silent Mode** - Minimal output for CI/CD integration

## Overview

```
Idea → PRD → TRD → Tasks → [Session: Start → Work → Review → Commit → End] → Ship
```

This framework combines:
- **Strategic Planning Skills** - Generate requirements, specifications, and task breakdowns
- **Session Management** - Efficiently resume work with crash recovery
- **Autonomous Development** - Execute tasks with mandatory code review
- **Operational Commands** - Git workflows, debugging, refactoring, security audits
- **Security Layers** - 6-layer protection against credential leaks

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

### 2. Existing Project Onboarding
```bash
# Migrate existing project to framework
/migrate-legacy

# Review generated documentation
# Then start development
/autonomous-development
```

### 3. Daily Development Session
```bash
# Resume work (loads context, checks for crashes)
"start" or "resume"

# Work on tasks
/autonomous-development

# Or use specific commands
/feature "Add user authentication"
/fix "Login redirect issue"

# End session (saves state)
/fi or "done"
```

## Preset System

The framework supports 5 behavior presets that control confirmation requirements, security scanning, and output verbosity:

| Preset | Description | Use Case |
|--------|-------------|----------|
| `paranoid` | Maximum safety, requires confirmation for everything | Production deployments, security-critical work |
| `balanced` | Default preset, smart confirmations | Normal development |
| `autopilot` | Minimal confirmations, auto-commit | Rapid prototyping, trusted environments |
| `verbose` | Extra logging and progress output | Debugging, learning |
| `silent` | Minimal output, CI/CD optimized | Automated pipelines |

### Setting Presets

In `.claude/settings.json`:
```json
{
  "preset": "balanced",
  "presets": {
    "balanced": {
      "review_required": true,
      "auto_commit": false,
      "security_scan": "always",
      "confirmation_level": "smart",
      "output_verbosity": "normal"
    }
  }
}
```

Or via CLI:
```bash
npm run framework:cold-start -- --preset autopilot
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
| Cold Start | "start", "resume" | Load context, crash recovery |
| Completion | "done", `/fi` | Save state, update snapshot |
| Auto-triggers | Automatic | Detect session boundaries |

**Performance:** Cold Start executes 10 parallel tasks in ~350ms using Python ThreadPoolExecutor.

### Execution Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| Autonomous Dev | `/autonomous-development` | Execute tasks sequentially |
| Code Review | `/codex-review` | Validate changes (mandatory) |

### Code Commands

| Command | Purpose |
|---------|---------|
| `/feature <desc>` | Plan and implement new features |
| `/fix <issue>` | Debug and fix issues |
| `/refactor [file]` | Improve code structure |
| `/explain [file]` | Explain how code works |
| `/optimize [file]` | Performance optimization |

### Quality Commands

| Command | Purpose |
|---------|---------|
| `/review [file]` | Manual code review checklist |
| `/security` | OWASP security audit |
| `/security-dialogs` | AI credential deep scan |
| `/test` | Write and run tests |

### Git Commands

| Command | Purpose |
|---------|---------|
| `/commit` | Structured git commits |
| `/pr` | Create pull requests |
| `/release` | Version management |

### Database Commands

| Command | Purpose |
|---------|---------|
| `/db:migrate` | Schema migrations |

### Dialog Commands

| Command | Purpose |
|---------|---------|
| `/ui` | Browse exported dialogs (localhost:3333) |
| `/watch` | Auto-export in real-time |

### Framework Commands

| Command | Purpose |
|---------|---------|
| `/fi` | Finish session |
| `/migrate-legacy` | Onboard existing projects |
| `/upgrade-framework` | Update to latest version |
| `/bug-reporting` | Manage error reporting |
| `/analyze-bugs` | Analyze error patterns |

### Best Practices

| Skill | Command | Purpose |
|-------|---------|---------|
| React/Next.js | `/vercel-react-best-practices` | Performance optimization |
| Web Design | `/web-design-guidelines` | Accessibility, UX compliance |

## Directory Structure

```
project-root/
├── .claude/
│   ├── commands/                  # Operational commands
│   │   ├── code/                  # feature, fix, refactor, explain, optimize
│   │   ├── git/                   # commit, pr, release
│   │   ├── quality/               # review, security, security-dialogs, test
│   │   ├── db/                    # migrate
│   │   ├── dialog/                # ui, watch
│   │   └── framework/             # fi, migrate-legacy, upgrade, bug-reporting
│   │
│   ├── protocols/                 # Session management
│   │   ├── cold-start.md          # Session init + crash recovery
│   │   ├── completion.md          # Session finalization
│   │   └── auto-triggers.md       # Automatic detection
│   │
│   ├── scripts/                   # Automation
│   │   ├── pre-commit-hook.sh     # Block sensitive files
│   │   └── install-git-hooks.sh   # Hook installer
│   │
│   ├── skills/                    # Strategic skills
│   │   ├── prd/                   # Product requirements
│   │   ├── trd/                   # Technical specification
│   │   ├── to-do/                 # Task breakdown
│   │   ├── autonomous-development/
│   │   ├── codex-review/
│   │   ├── vercel-react-best-practices/
│   │   └── web-design-guidelines/
│   │
│   ├── settings.json              # Framework configuration
│   └── COMMIT_POLICY.md           # Commit rules
│
├── src/
│   ├── framework-core/            # Python session management (v2.0)
│   │   ├── commands/              # cold_start.py, completion.py
│   │   ├── tasks/                 # config, git, hooks, security, session
│   │   ├── utils/                 # parallel, result, logger
│   │   └── main.py                # CLI entry point
│   │
│   └── claude-export/             # TypeScript dialog exporter (v2.0)
│       ├── cli.ts                 # export, ui, watch commands
│       ├── exporter.ts            # Session parsing + redaction
│       ├── server.ts              # Express web viewer
│       └── watcher.ts             # Real-time export
│
├── security/                      # Security scripts
│   ├── check-triggers.sh          # Verify 6 security layers
│   └── initial-scan.sh            # Quick credential scan
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
├── CLAUDE.md                      # AI instruction router
├── CHANGELOG.md                   # Version history
└── package.json                   # npm scripts
```

## Security Layers

The framework implements 6 layers of security:

```
Layer 1: .gitignore           → Prevents tracking sensitive files
Layer 2: COMMIT_POLICY.md     → Defines commit rules
Layer 3: Pre-commit hook      → Blocks forbidden patterns
Layer 4: /security-dialogs    → AI deep credential scan
Layer 5: /codex-review        → Code quality validation
Layer 6: /security            → OWASP security audit
```

### Verify Security Configuration

```bash
npm run security:check
# or directly:
./security/check-triggers.sh
```

### Install Git Hooks

```bash
.claude/scripts/install-git-hooks.sh
```

This installs a pre-commit hook that:
- Blocks `.env` files and credentials
- Scans for hardcoded secrets
- Enforces COMMIT_POLICY.md rules

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
- Crash recovery detects incomplete sessions

### Token Efficiency
```
Cold Start loads:
├── snapshot.md      (~500 tokens)
├── to-do.md         (~1000 tokens, incomplete only)
└── Relevant PRD/TRD (~1500 tokens)
                     ─────────────
Total:               ~3000 tokens
```

### Parallel Execution (v2.0)
The Python framework core executes tasks in parallel:
```
Cold Start (10 parallel tasks):
├── migration_cleanup     ┐
├── crash_detection       │
├── config_init           │
├── context_load          ├── All execute simultaneously
├── git_hooks_install     │   in ~350ms total
├── commit_policy_verify  │
├── version_check         │
├── security_cleanup      │
└── session_activate      ┘
```

## Configuration

Edit `.claude/settings.json` to customize:

```json
{
  "preset": "balanced",
  "silent_mode": false,
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
  },
  "presets": {
    "paranoid": {
      "review_required": true,
      "auto_commit": false,
      "security_scan": "always",
      "confirmation_level": "all"
    },
    "balanced": {
      "review_required": true,
      "auto_commit": false,
      "security_scan": "always",
      "confirmation_level": "smart"
    },
    "autopilot": {
      "review_required": false,
      "auto_commit": true,
      "security_scan": "quick",
      "confirmation_level": "none"
    }
  }
}
```

## Requirements

### Required
- **Claude Code CLI** - Latest version
- **Python 3.8+** - For framework core
- **Git** - Version control

### Optional
- **Node.js 18+** - For dialog exporter web UI
- **tmux** and **codex** CLI - For code review

## NPM Scripts

```bash
# Framework commands
npm run framework:cold-start    # Start session
npm run framework:completion    # End session

# Dialog exporter
npm run dialog:export           # Export conversations
npm run dialog:ui               # Start web viewer (localhost:3333)

# Security
npm run security:scan           # Run credential scan
npm run security:check          # Verify security layers
```

## Migration from v1.x

If upgrading from v1.x:

1. **Backup configuration**: Save `.claude/settings.json`
2. **Update files**: Copy new `src/` directory
3. **Merge settings**: Add `preset` and `presets` to settings.json
4. **Test**: Run `npm run framework:cold-start`

See [CHANGELOG.md](CHANGELOG.md) for detailed changes.

## Troubleshooting

### Cold Start Fails
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Run with verbose output
npm run framework:cold-start -- --verbose
```

### Security Scan False Positives
The security scan may flag patterns in test files. Add exclusions to `.claude/settings.json`:
```json
{
  "security": {
    "excludePaths": ["**/*.test.ts", "**/fixtures/**"]
  }
}
```

### Dialog Exporter Not Starting
```bash
# Install dependencies
cd src/claude-export && npm install

# Then run
npm run dialog:ui
```

## Credits

This framework combines concepts from:
- Original planning skills (PRD, TRD, To-Do)
- [claude-code-starter](https://github.com/alexeykrol/claude-code-starter) by Alexey Krol (session management, operational commands)
- [Vercel Engineering](https://vercel.com) (React best practices)

## License

MIT

---

*Built for AI-assisted development with Claude Code*
