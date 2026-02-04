# Project Snapshot

> Claude Code Project Framework v2.0
> Last Updated: 2026-02-04

## Current State

| Attribute | Value |
|-----------|-------|
| Project | claude-code-project-start-pack |
| Version | 2.0 |
| Phase | Framework Complete |
| Status | Active Development |
| Last Task | Enhanced /feature command with orchestration workflow |
| Next Task | User testing and feedback |
| Blockers | None |

## Session History

| Date | Duration | Tasks Completed | Commits | Notes |
|------|----------|-----------------|---------|-------|
| 2026-02-04 | ~4h | 8 | 2 | v2.0 release, architecture fixes, /feature enhancement |
| 2026-02-04 | ~2h | 5 | 1 | Architecture inconsistency fixes |
| Previous | - | - | - | v1.x to v2.0 integration (Phases 5-8) |

## Quick Context

### What Exists

**Framework Core (Complete):**
- Python parallel execution engine (10 tasks, ~350ms)
- TypeScript dialog export tools with web UI
- 5 behavior presets (paranoid, balanced, autopilot, verbose, silent)
- 6-layer security architecture
- Session management with crash recovery

**Commands (24 total):**
- Code: feature, fix, refactor, explain, optimize
- Git: commit, pr, release
- Quality: review, security, security-dialogs, test
- Database: migrate
- Dialog: ui, watch
- Framework: fi, migrate-*, upgrade, bug-reporting

**Skills (8 total):**
- Planning: prd, trd, to-do
- Execution: autonomous-development, codex-review
- Best Practices: vercel-react-best-practices, web-design-guidelines

**Protocols:**
- Cold Start: 3 variants (verbose/optimized/silent)
- Completion: 3 variants (verbose/optimized/silent)
- Router with preset-based selection

### What's Next

1. User testing with real projects
2. Gather feedback on preset behaviors
3. Refine auto-trigger detection
4. Add more best-practice skills as needed

### Key Decisions This Sprint

1. **Enhanced /feature command** - Now orchestrates full workflow:
   - Reads PRD/TRD context
   - Asks up to 5 clarifying questions
   - Updates PRD, TRD, and to-do.md
   - Auto-invokes /autonomous-development
   - Security review always added to TRD

2. **Architecture consistency fixes:**
   - CLI argument order (global flags before subcommands)
   - Session status values aligned ("completed" not "clean")
   - Task count verified (10 parallel tasks)
   - Codex review separation documented

3. **Schema validation:**
   - Created presets.schema.json for preset validation
   - All configuration now has JSON Schema

## Document Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| prd.md | Template | - |
| trd.md | Template | - |
| to-do.md | Template | - |
| architecture.md | Complete | 2026-02-04 |
| snapshot.md | Complete | 2026-02-04 |
| CLAUDE.md | Complete | 2026-02-04 |

## Hot Paths

Files frequently accessed or modified:
- `.claude/commands/code/feature.md` - Feature orchestration
- `.claude/skills/autonomous-development/SKILL.md` - Task execution
- `.claude/protocols/router.md` - Protocol selection
- `src/framework-core/main.py` - CLI entry point
- `CLAUDE.md` - Instruction router

## Technical Notes

### Framework Architecture
- **Python Core:** Zero external dependencies, stdlib only
- **TypeScript Tools:** Express + Chokidar + Marked
- **Preset System:** 5 presets with invariants (code review mandatory)
- **Protocol Routing:** Based on active preset setting

### Key Invariants (Cannot Override)
- `review.compulsory = true` - Code review always required
- `protocols.completion.requireReview = true` - Review before commit

### Recent Changes (v2.0)
- Parallel execution (10 tasks in ~350ms)
- Preset system with protocol routing
- Enhanced /feature with document updates
- Silent mode for flow-state optimization
- TypeScript dialog exporter with web UI

### CLI Usage
```bash
# Framework core
python3 src/framework-core/main.py cold-start
python3 src/framework-core/main.py completion
python3 src/framework-core/main.py --silent cold-start

# Dialog tools (requires npm install)
npm run dialog:export
npm run dialog:ui
npm run dialog:watch
```

### Git Commits (Recent)
- `ed55857` - fix: Resolve architecture inconsistencies
- `4e0f4f9` - feat: Release Framework v2.0

---

*This file is automatically updated by the Completion Protocol. Manual edits will be preserved.*
*Framework: claude-code-project-start-pack v2.0*
