# Migrate Legacy Command

Migrate existing projects to the Claude Code Project Framework.

## Usage

```
/migrate-legacy
```

## Purpose

Onboard existing projects that don't have the framework structure. This command:
- Analyzes existing project documentation
- Extracts relevant information
- Generates framework files
- Preserves all existing content

## Process

### Step 0: Pre-flight Checks

```
1. Verify this is a git repository
2. Check for existing .claude/ directory
3. Detect if framework already installed
4. Create migration log for recovery
```

If framework exists:
```
Framework already detected. Use /upgrade-framework instead.
```

### Step 1: Discovery Phase

Scan for existing documentation:

```
Locations checked:
├── Root directory
│   ├── README.md
│   ├── TODO.md / BACKLOG.md
│   ├── ROADMAP.md
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING.md
│
├── Documentation directories
│   ├── docs/
│   ├── documentation/
│   ├── wiki/
│   └── .github/
│
├── Project metadata
│   ├── package.json (name, description)
│   └── git log (recent activity)
│
└── Code structure
    └── Directory tree analysis
```

### Step 2: Security Scan

Before proceeding, scan for credentials:

```
Check for:
- .env files with actual values
- Hardcoded API keys in code
- Credentials in existing docs

Options if found:
1. Report and remind to clean up
2. Automatic redaction (with confirmation)
3. Manual fix guidance
```

### Step 3: Analysis

Using discovered documentation:

```
Extract:
- Project name and description
- Current status / phase
- Active tasks / backlog items
- Architecture overview
- Technology stack
- Key decisions made
```

### Step 4: User Questions

Clarify gaps with targeted questions:

```
Questions may include:
- What is the primary goal of this project?
- What phase is development in?
- Are there pending tasks not in docs?
- Any architectural decisions to note?
```

### Step 5: Generate Report

Before creating files, show analysis:

```markdown
## Migration Analysis

### Project: [Detected Name]
[Detected description]

### Discovered Documentation
- README.md (450 lines) - Project overview
- docs/ARCHITECTURE.md (200 lines) - System design
- TODO.md (50 lines) - Task list

### Extracted Information

**Status:** Active development
**Phase:** MVP implementation
**Stack:** Next.js, TypeScript, Prisma
**Tasks Found:** 12 pending items

### Files to Generate
1. dev-docs/prd.md - From README + discovered requirements
2. dev-docs/trd.md - From ARCHITECTURE + package.json
3. dev-docs/to-do.md - From TODO.md + extracted tasks
4. dev-docs/snapshot.md - Current state summary
5. dev-docs/architecture.md - From existing architecture docs
6. CLAUDE.md - Framework instruction router
7. .claude/settings.json - Default configuration

Proceed with migration? [Y/n]
```

### Step 6: Generate Framework Files

Create files in parallel:

```
Files created:
├── dev-docs/
│   ├── prd.md (extracted requirements)
│   ├── trd.md (extracted technical spec)
│   ├── to-do.md (extracted tasks)
│   ├── snapshot.md (current state)
│   └── architecture.md (code structure)
│
├── .claude/
│   ├── settings.json
│   ├── COMMIT_POLICY.md
│   ├── commands/ (full command set)
│   ├── protocols/ (session protocols)
│   └── skills/ (development skills)
│
├── dialog/
│   ├── .gitignore
│   └── README.md
│
└── CLAUDE.md
```

### Step 7: Install Git Hooks

```bash
.claude/scripts/install-git-hooks.sh
```

### Step 8: Verification

Confirm all files created:

```
✓ dev-docs/prd.md (45 lines)
✓ dev-docs/trd.md (120 lines)
✓ dev-docs/to-do.md (35 lines)
✓ dev-docs/snapshot.md (25 lines)
✓ dev-docs/architecture.md (80 lines)
✓ CLAUDE.md (150 lines)
✓ .claude/settings.json
✓ Git hooks installed
```

### Step 9: Summary

```markdown
## Migration Complete

### What Was Created
- 5 documentation files in dev-docs/
- Framework configuration in .claude/
- AI instruction router (CLAUDE.md)
- Git hooks for security

### Existing Files
- Preserved: All original documentation untouched
- Enhanced: Can now use /prd, /trd, /to-do to refine

### Next Steps
1. Review generated files for accuracy
2. Run /prd to enhance product requirements
3. Run /trd to enhance technical spec
4. Run /to-do to refine task breakdown
5. Start development with /autonomous-development

### Quick Start
"start" - Load project context
/autonomous-development - Begin working on tasks
"done" - Save progress and end session
```

## Non-Destructive Guarantee

This migration:
- **NEVER** deletes existing files
- **NEVER** modifies existing documentation
- **ONLY** creates new files in dev-docs/ and .claude/
- **ONLY** adds CLAUDE.md at project root

Existing README.md, TODO.md, etc. remain untouched.

## Recovery

If migration fails or needs to be undone:

```bash
# Remove generated files
rm -rf dev-docs/ .claude/ dialog/ CLAUDE.md

# Remove git hooks
rm .git/hooks/pre-commit
```

## Configuration

After migration, customize in `.claude/settings.json`:

```json
{
  "framework": {
    "name": "your-project-name"
  },
  "documents": {
    "prd": "dev-docs/prd.md",
    "trd": "dev-docs/trd.md",
    "todo": "dev-docs/to-do.md"
  }
}
```
