# Architecture Documentation

> Claude Code Project Framework v2.0
> Last Updated: 2026-02-04

## Overview

The Claude Code Project Framework is a comprehensive AI-assisted development system that provides structured workflows for the complete software development lifecycle. It combines Python for fast parallel execution, TypeScript for dialog management, and Markdown-based protocols for workflow definitions.

```
Idea → PRD → TRD → Tasks → [Session: Start → Work → Review → Commit → End] → Ship
```

## Directory Structure

```
claude-code-project-start-pack/
├── .claude/                        # Framework configuration
│   ├── commands/                   # 24 command definitions
│   │   ├── code/                   # feature, fix, refactor, explain, optimize
│   │   ├── git/                    # commit, pr, release
│   │   ├── quality/                # review, security, security-dialogs, test
│   │   ├── db/                     # migrate
│   │   ├── dialog/                 # ui, watch
│   │   └── framework/              # fi, migrate-*, upgrade, bug-reporting
│   ├── protocols/                  # 10 protocol files
│   │   ├── router.md               # Protocol selector
│   │   ├── cold-start*.md          # 3 variants (verbose/optimized/silent)
│   │   ├── completion*.md          # 3 variants (verbose/optimized/silent)
│   │   ├── auto-triggers.md        # Trigger detection logic
│   │   ├── apply-preset.md         # Preset application
│   │   └── settings-migration.md   # Settings upgrade
│   ├── skills/                     # 8 skill directories
│   │   ├── prd/                    # PRD generation
│   │   ├── trd/                    # TRD generation
│   │   ├── to-do/                  # Task breakdown
│   │   ├── autonomous-development/ # Task execution with review
│   │   ├── codex-review/           # Code review (mandatory)
│   │   ├── vercel-react-best-practices/  # 50+ React/Next.js rules
│   │   └── web-design-guidelines/  # Accessibility compliance
│   ├── analysis/                   # 6 ADR files
│   ├── scripts/                    # Git hooks and utilities
│   ├── settings.json               # Framework configuration
│   ├── settings.schema.json        # Settings validation
│   ├── presets.json                # 5 preset definitions
│   ├── presets.schema.json         # Presets validation
│   └── COMMIT_POLICY.md            # Commit rules
├── src/
│   ├── framework-core/             # Python parallel execution engine
│   │   ├── main.py                 # CLI entry point
│   │   ├── commands/               # cold_start.py, completion.py
│   │   ├── tasks/                  # config, git, hooks, security, session, version
│   │   └── utils/                  # parallel, result, logger
│   └── claude-export/              # TypeScript dialog tools
│       ├── cli.ts                  # CLI entry point
│       ├── exporter.ts             # Session export logic
│       ├── server.ts               # Express web UI (port 3333)
│       ├── watcher.ts              # File system watcher
│       └── types.ts                # Type definitions
├── dev-docs/                       # Project documentation
│   ├── prd.md                      # Product requirements
│   ├── trd.md                      # Technical requirements
│   ├── to-do.md                    # Task breakdown
│   ├── snapshot.md                 # Project state
│   └── architecture.md             # This file
├── dialog/                         # Exported session dialogs
├── security/                       # Security scanning utilities
├── migration/                      # Legacy migration support
├── CLAUDE.md                       # Framework instruction router
├── package.json                    # NPM configuration
└── README.md                       # User documentation
```

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework Core | Python | 3.8+ | Fast parallel execution (zero deps) |
| Dialog Tools | TypeScript/Node.js | 18+ | Session export and web UI |
| Session Format | JSONL | - | Claude session storage |
| Protocols | Markdown | - | Workflow definitions |
| Configuration | JSON | - | Settings with schema validation |
| Version Control | Git | 2.x | Repository operations |

## Key Components

### Python Framework Core (`src/framework-core/`)

**Purpose:** Execute parallel tasks for session protocols with minimal latency.

**Characteristics:**
- Zero external dependencies (stdlib only)
- ThreadPoolExecutor with 10 workers max
- ~350ms cold-start execution time
- Structured JSON output for Claude integration
- Exit codes: 0 (success), 1 (error), 2 (user input required)

**Module Structure:**

| Module | Purpose |
|--------|---------|
| `main.py` | CLI entry point, argument parsing |
| `commands/cold_start.py` | 10 parallel initialization tasks |
| `commands/completion.py` | Session finalization workflow |
| `tasks/config.py` | Framework configuration management |
| `tasks/git.py` | Git operations wrapper |
| `tasks/hooks.py` | Git hooks installation |
| `tasks/security.py` | Security scanning |
| `tasks/session.py` | Session state management |
| `tasks/version.py` | Version checking |
| `utils/parallel.py` | Parallel execution utilities |
| `utils/result.py` | Structured result objects |
| `utils/logger.py` | Thread-safe logging |

### TypeScript Dialog Tools (`src/claude-export/`)

**Purpose:** Export Claude sessions with credential redaction.

**Capabilities:**
- Session discovery from `~/.claude/projects/`
- JSONL parsing and transformation
- 15+ credential redaction patterns
- Export formats: Markdown, HTML, JSON
- Web UI browser (Express on port 3333)
- Real-time file watching

### Protocol System (`.claude/protocols/`)

**Purpose:** Define session workflows based on preset.

**Protocol Routing:**

| Preset | Cold Start | Completion |
|--------|------------|------------|
| paranoid, verbose | cold-start.md | completion.md |
| balanced | cold-start-optimized.md | completion-optimized.md |
| autopilot, silent | cold-start-silent.md | completion-silent.md |

### Preset System (`.claude/presets.json`)

**Purpose:** Control framework behavior profiles.

| Preset | Output | Confirmations | Auto-Triggers | Use Case |
|--------|--------|---------------|---------------|----------|
| paranoid | Full | All | Disabled | Sensitive projects |
| balanced | Optimized | Single | Suggest | Daily development |
| autopilot | Silent | Minimal | Execute | Personal projects |
| verbose | Full | All | Suggest | Debugging (default) |
| silent | None | None | Execute | Flow state |

### Command System (`.claude/commands/`)

**24 Commands across 6 categories:**

| Category | Commands | Purpose |
|----------|----------|---------|
| code | feature, fix, refactor, explain, optimize | Code operations |
| git | commit, pr, release | Version control |
| quality | review, security, security-dialogs, test | Quality assurance |
| db | migrate | Database operations |
| dialog | ui, watch | Dialog management |
| framework | fi, migrate-*, upgrade, bug-* | Framework operations |

### Skill System (`.claude/skills/`)

**8 Skills:**

| Skill | Purpose | Invocation |
|-------|---------|------------|
| prd | Generate Product Requirements Document | `/prd <idea>` |
| trd | Generate Technical Requirements Document | `/trd` |
| to-do | Generate task breakdown | `/to-do` |
| autonomous-development | Execute tasks with review | `/autonomous-development` |
| codex-review | Code review (MANDATORY) | `/codex-review` |
| vercel-react-best-practices | React/Next.js optimization | Automatic in React projects |
| web-design-guidelines | Accessibility compliance | UI reviews |

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Request                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code CLI                               │
│              (Loads CLAUDE.md instruction router)                │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    Commands     │ │    Protocols    │ │     Skills      │
│ (.claude/cmds/) │ │ (.claude/proto/)│ │ (.claude/skills)│
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Python Framework Core (if needed)                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           ThreadPoolExecutor (10 workers)                │   │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ... ┌────┐          │   │
│  │  │Task│ │Task│ │Task│ │Task│ │Task│     │Task│          │   │
│  │  │ 1  │ │ 2  │ │ 3  │ │ 4  │ │ 5  │     │ 10 │          │   │
│  │  └────┘ └────┘ └────┘ └────┘ └────┘     └────┘          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│                    JSON Result Aggregation                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Claude Processing                              │
│            (Parse results, format output, apply preset)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      User Output                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Security Architecture

### 6-Layer Protection Model

```
Layer 1: .gitignore
    └─ Prevent tracking of secrets, node_modules, IDE files
         ↓
Layer 2: COMMIT_POLICY.md
    └─ Semantic rules (NEVER/ALWAYS/ASK)
         ↓
Layer 3: Pre-commit Hook
    └─ Regex pattern matching on staged files
         ↓
Layer 4: /security-dialogs
    └─ Deep AI credential scan
         ↓
Layer 5: /codex-review (MANDATORY)
    └─ Code quality and security review
         ↓
Layer 6: /security
    └─ OWASP vulnerability audit
```

### Credential Redaction Patterns

Applied during dialog export:
- OpenAI API keys (`sk-*`)
- Stripe keys (`sk_live/sk_test`, `pk_live/pk_test`)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`)
- AWS credentials (`AKIA*`)
- Generic patterns (password, api_key, secret, token)
- Bearer tokens, Basic auth, Private keys

### Commit Policy

| Category | Policy | Examples |
|----------|--------|----------|
| NEVER | Always blocked | .env, *.key, credentials.*, dialog/ |
| ALWAYS | Always safe | src/, tests/, docs/, package.json |
| ASK | Require confirmation | New directories, binary files |

## Key Design Decisions

### ADR-001: Python for Framework Core
- **Context**: Need fast parallel execution with minimal startup time
- **Decision**: Python with stdlib only (no pip dependencies)
- **Consequences**: ~350ms cold-start, zero-install for users with Python
- **Reference**: `.claude/analysis/python-core-decision.md`

### ADR-002: TypeScript for Dialog Tools
- **Context**: Need file watching, web server, rich CLI
- **Decision**: TypeScript with Node.js ecosystem
- **Consequences**: Requires Node.js 18+, but gains express/chokidar/marked
- **Reference**: `.claude/analysis/dialog-exporter-decision.md`

### ADR-003: Preset System
- **Context**: Users need different behavior profiles
- **Decision**: 5 presets with protocol routing and invariants
- **Consequences**: Flexible behavior with locked security rules
- **Reference**: `.claude/analysis/preset-system-design.md`

### ADR-004: Mandatory Code Review
- **Context**: Code quality must be enforced
- **Decision**: `/codex-review` is compulsory (invariant)
- **Consequences**: No commit without review, even in silent mode
- **Reference**: `.claude/presets.json` (invariants section)

## Performance Characteristics

| Operation | Time | Details |
|-----------|------|---------|
| Cold Start | ~350ms | 10 parallel tasks |
| Completion | Variable | Includes mandatory review |
| Dialog Export | Depends on size | Linear with message count |

**Concurrency:**
- Max 10 parallel workers
- Sequential tasks stop on first error
- Thread-safe logging

## Key Workflows

### New Project Setup
```
/prd <idea> → /trd → /to-do → /autonomous-development
```

### Adding Features
```
/feature <description> → Updates PRD/TRD/to-do → /autonomous-development
```

### Daily Development
```
"start" → /autonomous-development → /codex-review → /commit → "done"
```

### Session Management
```
Cold Start: Load context, verify state, detect crashes
Completion: Review, update docs, commit, cleanup
```

## Module Dependencies

```
CLAUDE.md (instruction router)
    ├── .claude/protocols/router.md
    │       ├── cold-start*.md → Python Framework Core
    │       └── completion*.md → Python Framework Core
    ├── .claude/commands/*
    │       └── Various command definitions
    ├── .claude/skills/*
    │       ├── prd, trd, to-do (planning)
    │       ├── autonomous-development (execution)
    │       ├── codex-review (quality)
    │       └── best-practices (guidance)
    └── .claude/settings.json
            ├── presets.json
            └── COMMIT_POLICY.md
```

## Extension Points

### Adding Commands
1. Create `.claude/commands/<category>/<name>.md`
2. Define command workflow
3. Reference from CLAUDE.md if needed

### Adding Skills
1. Create `.claude/skills/<name>/SKILL.md`
2. Add `rules/` directory if applicable
3. Register in skill discovery

### Adding Protocols
1. Create `.claude/protocols/<name>.md`
2. Update router.md routing table
3. Test with relevant presets

### Modifying Presets
1. Edit `.claude/presets.json`
2. Validate against schema
3. Document changes in CLAUDE.md

---

*This file documents the framework architecture. Update when structural changes occur.*
*Framework: claude-code-project-start-pack v2.0*
