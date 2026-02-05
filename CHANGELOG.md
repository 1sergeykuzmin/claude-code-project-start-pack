# Changelog

All notable changes to the Claude Code Project Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2026-02-05

### Added

#### Documentation Redesign
- **User-friendly README** restructured around user journey (not features)
- Real command/response examples for all 5 main commands (`/prd`, `/trd`, `/to-do`, `/autonomous-development`, `/codex-review`)
- Session management section with crash recovery examples
- Proper credits section acknowledging planning skills and [claude-code-starter](https://github.com/alexeykrol/claude-code-starter) architecture
- **Russian translation** (`README.ru.md`) with language switcher
- Reduced time-to-first-example from line 84 to line 6

#### Installer Script
- **One-line installation** for existing projects: `curl -fsSL .../install.sh | bash`
- Installation options: `--minimal`, `--force`, `--no-hooks`, `--update`, `--dry-run`
- Intelligent CLAUDE.md merging (preserves existing project-specific content)
- Automatic .gitignore updates with framework patterns
- Backup creation before overwriting existing installations
- Update mode to refresh framework while preserving customizations

### Changed

#### Autonomous Development - Continuous Loop Execution
- `/autonomous-development` now runs in **mandatory continuous loop** until ALL tasks complete
- Explicit anti-stopping rules: cannot pause to summarize, ask user, or take breaks
- Only 3 valid stop conditions: all tasks done, unfixable error after 3 retries, user interrupt
- After every commit, immediately finds and starts the next task
- Added enforcement rules to prevent premature session termination
- Context management guidance: context pressure is not a valid reason to stop

### Fixed
- Removed `$schema` from settings.json (caused Claude Code validation errors)

## [2.0.0] - 2026-02-04

### Added

#### Preset System
- **5 execution presets**: paranoid, balanced, autopilot, verbose, silent
- Preset definitions in `.claude/presets.json`
- Override mechanism for fine-grained control
- Invariants (codex-review always mandatory, PR confirmation required)

#### Silent Mode
- Zero output on success philosophy
- Protocol variants: `cold-start-silent.md`, `completion-silent.md`
- Optimized variants for balanced mode
- Protocol router for automatic variant selection

#### Python Framework Core (`src/framework-core/`)
- 10 parallel initialization tasks during cold start
- 3 parallel + sequential tasks during completion
- ThreadPoolExecutor-based parallel execution
- JSON output format for programmatic use
- Structured logging to `.claude/logs/`
- Task modules: config, git, hooks, security, session, version

#### TypeScript Dialog Exporter (`src/claude-export/`)
- Session discovery and parsing
- Export formats: Markdown, HTML, JSON
- Automatic credential redaction
- Web viewer at localhost:3333
- File watching for auto-export
- CLI commands: export, ui, watch, list

#### Migration Command Suite
- `/migrate` - Start version migration with conflict detection
- `/migrate-resolve` - Interactive conflict resolution
- `/migrate-finalize` - Complete migration after resolution
- `/migrate-rollback` - Revert migration using backup

#### Security Scripts (`security/`)
- `initial-scan.sh` - Comprehensive credential scanning
- `check-triggers.sh` - Verify all 6 security layers
- `cleanup-dialogs.sh` - Redact credentials from exports
- `auto-invoke-agent.sh` - AI scan trigger with fallback

#### Configuration
- Extended `settings.json` schema with v2.0 fields
- JSON Schema for validation (`settings.schema.json`)
- `.framework-config` for runtime state
- Settings migration from v1.x automatic

#### Documentation
- Architectural Decision Records (ADRs) in `.claude/analysis/`
- GitHub issue templates for bugs and features
- Updated README.md with v2.0 features
- This CHANGELOG

### Changed

- **settings.json schema extended** (backward compatible)
  - Added `preset` field
  - Added `execution.mode` field
  - Added `execution.parallelism` field
  - Added `autoUpdate` section
  - Added `protocols.autoTriggers` configuration

- **Auto-triggers enhanced**
  - AI-based completion probability scoring
  - Last 10 message analysis
  - Idle time monitoring
  - Russian keyword support
  - Configurable confidence threshold

- **Protocol routing**
  - Automatic selection based on active preset
  - Fallback to verbose for unknown presets

### Fixed

- None (initial v2.0 release)

### Deprecated

- None

### Removed

- None

### Security

- Credential scanning in all protocols
- Pre-commit hook with security patterns
- Mandatory codex-review regardless of preset
- Automatic credential redaction in dialog exports

---

## [1.x.x] - Previous Versions

See git history for changes prior to v2.0.0.

The v1.x series included:
- PRD/TRD/To-Do skills
- Autonomous development workflow
- Codex review integration
- Basic cold start and completion protocols
- dev-docs/ structure for project documentation
