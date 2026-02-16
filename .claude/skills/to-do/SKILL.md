---
name: to-do
description: Generate a development task breakdown from the existing PRD and TRD. Use when asked to create a task list, plan development work, or break down implementation into phases. Invoked as "/to-do". Supports --team flag for multi-perspective generation using decomposer + validator agents, and --update flag for incremental updates preserving progress.
metadata:
  author: custom
  version: "2.0.0"
  argument-hint: [--team] [--update]
---

# Development Task Breakdown Generator

Generate structured development task lists based on the Product Requirements Document (PRD) and Technical Requirements Document (TRD). This skill decomposes the implementation into actionable tasks organized by vertical feature slices with task IDs, complexity metadata, acceptance criteria, dependency graphs, and quality gates.

Supports three modes:
- **Solo mode** (default): Single-agent task decomposition with adaptive archetype detection
- **Team mode** (`--team`): Decompose + Validate model using a Decomposer who generates the full breakdown, reviewed by a Validator for coverage and quality
- **Update mode** (`--update`): Incremental re-generation preserving existing task IDs and statuses

## Input Format

```
/to-do                # Solo mode (default)
/to-do --team         # Team mode (decompose + validate)
/to-do --update       # Update mode (preserve progress)
```

No other arguments required. The skill reads context from PRD and TRD.

## Mode Selection

### Detecting Mode

1. If the input contains `--team`, use **Team Mode**
2. If the input contains `--update`, use **Update Mode**
3. Otherwise, use **Solo Mode**

### When to Suggest Team Mode

If solo mode is invoked but the project meets ANY of these criteria, **suggest** (don't force) team mode:
- Complex multi-domain project spanning 3+ distinct feature areas
- PRD has 15+ functional requirements
- TRD describes microservices or distributed architecture
- Multi-platform product (web + mobile + API)

Suggestion format:
```
This project could benefit from validated task decomposition.
Would you like to use team mode (/to-do --team) for a more
thorough breakdown with independent validation of coverage
and granularity?
```

If the user declines, proceed with solo mode normally.

### Team Mode Prerequisites

Team mode requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to be enabled. If not enabled and `--team` is used:
```
Team mode requires agent teams to be enabled.
Add to your settings.json:
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }

Proceeding with solo mode instead.
```

### Detecting Update Mode

If `--update` is used:
1. Check if `dev-docs/to-do.md` exists
2. If it does NOT exist, inform the user and fall back to solo mode:
   ```
   No existing to-do.md found at dev-docs/to-do.md.
   Cannot run update mode without an existing task breakdown.
   Running solo mode instead to generate a fresh breakdown.
   ```
3. If it exists, proceed with update mode

## Prerequisites

Before running, ensure:
- PRD exists at `dev-docs/prd.md`
- TRD exists at `dev-docs/trd.md`

If either document is missing, the skill will prompt for the missing information or suggest running `/prd` or `/trd` first.

## Core Principles

**CRITICAL**: This skill must adhere to the following principles:

1. **No New Features**: Tasks must only implement what is defined in PRD/TRD
2. **No Contradictions**: Tasks must align with both PRD and TRD specifications
3. **Traceability**: Each task must trace back to a PRD feature or TRD component
4. **Completeness**: All PRD features and TRD components must have corresponding tasks
5. **Actionability**: Each task must be specific enough to implement
6. **Testability**: Each task must have explicit acceptance criteria
7. **Vertical Slicing**: Features are grouped by domain, not by tech layer
8. **Stable IDs**: Task IDs (T-xxx) are permanent and never reassigned

---

# SOLO MODE

The default task breakdown generation process using a single agent.

## Step 1: Read and Parse Documents

Read both documents and extract key information:

**From PRD (`dev-docs/prd.md`):**
```
1. Product name and overview
2. User stories (US-XXX) with priorities (P0/P1/P2)
3. Functional requirements (FR-XXX) with acceptance criteria
4. Non-functional requirements
5. Features with priorities
6. Scope boundaries (in/out of scope)
7. Success metrics
8. Product type signals (web app, mobile, CLI, API, etc.)
```

**From TRD (`dev-docs/trd.md`):**
```
1. Technology stack decisions
2. System architecture components
3. Database schema and models
4. API endpoints
5. Authentication/authorization approach
6. Infrastructure requirements
7. Implementation phases (if defined)
8. Testing strategy
9. CI/CD pipeline
10. Monitoring requirements
11. Project archetype signals (framework, backend type, deployment model)
```

**Additional extraction for v2.0:**
- Count all FRs and note their priority levels (P0/P1/P2)
- Extract acceptance criteria from PRD FRs (if present)
- Identify the project's tech stack category from TRD

## Step 2: Detect Project Archetype

Analyze PRD and TRD to determine the project archetype. The archetype drives the phase structure — replacing the fixed 9-phase horizontal layout with adaptive vertical slicing.

### Archetype Taxonomy

| Archetype | Detection Signals (from PRD/TRD) | Phase Structure |
|-----------|--------------------------------|-----------------|
| Full-stack web app | Frontend framework + backend API + database in TRD | Vertical slices by feature group |
| Frontend-only (SPA) | No backend/API in TRD, or BaaS (Firebase, Supabase) | UI component groups, state slices |
| API/Backend-only | No UI, API endpoints, microservices in TRD | Endpoint groups by domain |
| CLI tool | Command-line, terminal, no web UI mentioned | Command groups |
| Mobile app | React Native, Flutter, Swift, Kotlin in TRD | Screen/flow based slices |
| Data pipeline | ETL, batch processing, analytics, data warehouse | Pipeline stages |
| Library/SDK | npm package, pip install, public API surface | Public API surface groups |
| Serverless/Event-driven | Lambda, Cloud Functions, event bus, triggers | Event handler groups |

### Detection Logic

1. Scan TRD tech stack + architecture sections for archetype signals
2. Scan PRD product type and platform sections for confirmation
3. If clear match (3+ signals for one archetype) → assign that archetype
4. If ambiguous (signals spread across multiple archetypes) → default to "Full-stack web app"
5. Log the detected archetype in the output header

## Step 3: Generate Vertical-Slice Phases

Based on the detected archetype, generate phases that follow vertical feature slicing instead of horizontal tech layers.

### Universal Phases (always present)

Every project, regardless of archetype, includes these bookend phases:

- **Phase 0: Project Foundation** — Environment setup, dependency installation, configuration, project structure. Always first.
- **Phase N-1: Testing & Quality** — Integration tests, E2E tests, test infrastructure that spans features. Always second-to-last.
- **Phase N: DevOps & Launch** — CI/CD pipeline, deployment, monitoring, production readiness. Always last.

### Middle Phases: Vertical Feature Slices

Group related PRD features by domain into vertical slices. Each slice includes its own data model + API + UI + unit tests as tasks within the slice.

**Grouping rules:**
1. Group by PRD feature domain, not by tech layer
2. Order by priority: P0 slices first, then P1, then P2
3. Each slice should have 3-15 tasks (split if >15, merge if <3)
4. Name slices by feature/domain name, not by technology

**Example — Full-stack todo app:**
```
Phase 0: Project Foundation
Phase 1: User Management (signup, login, profile) — P0
Phase 2: Task CRUD & Organization — P0
Phase 3: Sharing & Collaboration — P1
Phase 4: Notifications & Reminders — P1
Phase 5: Analytics Dashboard — P2
Phase 6: Testing & Quality
Phase 7: DevOps & Launch
```

**Contrast with old v1.0 horizontal layout:**
```
Phase 1: Setup, Phase 2: DB, Phase 3: Auth, Phase 4: API,
Phase 5: Core Features, Phase 6: Extended Features...
```

### Archetype-Specific Phase Templates

**Full-stack web app:**
```
Phase 0: Project Foundation
Phases 1-N: Vertical feature slices (grouped by domain, P0→P1→P2)
Phase N-1: Testing & Quality
Phase N: DevOps & Launch
```

**Frontend-only (SPA):**
```
Phase 0: Project Foundation (framework, design system, state management setup)
Phases 1-N: UI feature groups (each includes components + state + API integration)
Phase N-1: Testing & Quality (component tests, visual regression, E2E)
Phase N: DevOps & Launch (build, deploy, CDN)
```

**API/Backend-only:**
```
Phase 0: Project Foundation (runtime, framework, database connection)
Phases 1-N: API domain groups (each includes models + endpoints + validation + tests)
Phase N-1: Testing & Quality (integration tests, load tests, API contract tests)
Phase N: DevOps & Launch (containerization, deployment, monitoring)
```

**CLI tool:**
```
Phase 0: Project Foundation (runtime, CLI framework, argument parsing)
Phases 1-N: Command groups (each includes command + options + output + help text)
Phase N-1: Testing & Quality (command tests, integration tests, shell tests)
Phase N: DevOps & Launch (packaging, distribution, installation)
```

**Mobile app:**
```
Phase 0: Project Foundation (framework, navigation, design tokens)
Phases 1-N: Screen/flow groups (each includes screen + state + API + offline)
Phase N-1: Testing & Quality (unit, integration, device testing)
Phase N: DevOps & Launch (app store, CI/CD, push notifications)
```

**Data pipeline:**
```
Phase 0: Project Foundation (runtime, orchestrator, connections)
Phases 1-N: Pipeline stages (ingestion, transformation, loading, reporting)
Phase N-1: Testing & Quality (data validation, integration tests, monitoring)
Phase N: DevOps & Launch (scheduling, alerting, disaster recovery)
```

**Library/SDK:**
```
Phase 0: Project Foundation (build system, package config, dev tooling)
Phases 1-N: API surface groups (each includes public API + internals + docs)
Phase N-1: Testing & Quality (unit tests, integration tests, compatibility)
Phase N: DevOps & Launch (publishing, versioning, documentation site)
```

**Serverless/Event-driven:**
```
Phase 0: Project Foundation (cloud config, IAM, shared utilities)
Phases 1-N: Event handler groups (each includes handler + trigger + state + DLQ)
Phase N-1: Testing & Quality (local emulation, integration tests)
Phase N: DevOps & Launch (IaC, deployment, monitoring, cost alerts)
```

## Step 4: Generate Tasks with Metadata

For each phase, create granular tasks with full metadata.

### Task Format

Every task MUST follow this format:

```markdown
- [ ] T-001 Create User model with email, password_hash, created_at fields [M] (TRD 3.2, PRD FR-001)
  - AC: User table exists with email unique constraint; password_hash is bcrypt; created_at defaults to now()
  - [depends: none] [files: src/models/user.ts, prisma/schema.prisma]
```

### Task Components

- **Checkbox**: `- [ ]` — pending status (see Expanded Status Model below)
- **Task ID**: `T-001` through `T-NNN` — stable, sequential, unique. Never reassigned.
- **Description**: Action verb + specific outcome. Same naming rules as v1.0.
- **Complexity tag**: `[S]`, `[M]`, `[L]`, or `[XL]` — in brackets after description
- **Traceability**: `(TRD X.X, PRD FR-XXX)` — in parentheses, referencing source sections
- **Acceptance criteria** (indented line, prefixed `AC:`): 1-3 crisp, testable conditions. Carried from PRD FR acceptance criteria or derived from TRD spec.
- **Dependency tag** (indented line): `[depends: T-003, T-005]` or `[depends: none]`
- **File hints** (indented, optional): `[files: path/to/likely/files]` — AI's best guess at which files will be touched

### Complexity Assignment Rules

| Tag | Meaning | Criteria |
|-----|---------|----------|
| `[S]` | Small (< 1h) | Single file, straightforward change, config-only |
| `[M]` | Medium (1-3h) | 2-3 files, some logic, typical feature task |
| `[L]` | Large (3-6h) | 4+ files, cross-cutting concern, complex logic |
| `[XL]` | Extra-large (should be split) | Flag in quality gates — decompose further |

### Task Naming Convention

- Start with action verb (Create, Implement, Add, Configure, Set up, Write, etc.)
- Be specific about what is being done
- Include component/file name when relevant
- Avoid vague terms like "handle", "manage", "process"

**Good Task Examples:**
```
- [ ] T-012 Create User model with email, password_hash, and created_at fields [M] (TRD 3.2, PRD FR-001)
  - AC: User table exists with unique email constraint; password stored as bcrypt hash
  - [depends: T-003] [files: src/models/user.ts, prisma/schema.prisma]

- [ ] T-015 Implement POST /api/auth/register endpoint with email validation [M] (TRD 4.2, PRD FR-002)
  - AC: Returns 201 on success with user object; returns 400 on invalid email; returns 409 on duplicate email
  - [depends: T-012] [files: src/routes/auth.ts, src/services/auth.ts]

- [ ] T-023 Add password strength validation (min 8 chars, 1 uppercase, 1 number) [S] (TRD 5.3, PRD FR-002)
  - AC: Registration rejects passwords not meeting criteria with specific error message
  - [depends: T-015] [files: src/validators/password.ts]
```

**Bad Task Examples (avoid):**
```
- [ ] Handle user authentication (too vague, no ID, no metadata)
- [ ] Set up the database (not specific enough)
- [ ] Make things work (meaningless)
- [ ] Implement everything for users (too broad)
```

## Step 5: Validate & Quality Gates

After generating all tasks, run quality gates to ensure completeness and correctness.

### Quality Gate Definitions

| Gate | Name | Severity | Detection |
|------|------|----------|-----------|
| TDQG-001 | PRD Coverage | ERROR | Every PRD FR-xxx must map to at least 1 task. List unmapped FRs. |
| TDQG-002 | TRD Coverage | ERROR | Every TRD component (DB model, API endpoint, infra element) must have at least 1 task. List unmapped components. |
| TDQG-003 | No Scope Creep | ERROR | Every task must trace back to a PRD FR or TRD section. Flag orphan tasks with no traceability reference. |
| TDQG-004 | Dependency Validity | ERROR | No circular dependencies. All `[depends: T-xxx]` must reference valid task IDs that exist. |
| TDQG-005 | XL Detection | WARNING | Flag any `[XL]` tasks — suggest decomposition into smaller tasks. |
| TDQG-006 | Acceptance Criteria | WARNING | Every task should have at least 1 AC line. Flag tasks without AC. |
| TDQG-007 | Phase Balance | WARNING | No phase should have more than 15 tasks or fewer than 2. Flag imbalanced phases. |
| TDQG-008 | Dependency Ordering | WARNING | Tasks within a phase should be ordered so that dependencies come before dependents. Flag ordering violations. |

### Gate Enforcement Procedure

1. After generating all tasks, scan for each gate (TDQG-001 through TDQG-008)
2. For ERROR gates: fix the issue inline before writing output
3. For WARNING gates: note in Quality Gate Results section
4. Append quality gate results table to the output document

## Step 6: Generate the Document

Create the task document at `dev-docs/to-do.md` with the following structure:

```markdown
# Development Tasks: [Product Name]

> Generated: [Date]
> Based on PRD: v[version]
> Based on TRD: v[version]
> Archetype: [detected archetype]
> Total Tasks: [count] (S: [n] | M: [n] | L: [n] | XL: [n])
> Status: Not Started
> Mode: Solo | Team

## Summary

| Phase | Description | Tasks | Complexity | Status |
|-------|-------------|-------|------------|--------|
| 0 | Project Foundation | [N] | S:[n] M:[n] L:[n] | ⬜ Not Started |
| 1 | [Feature Group Name] (P0) | [N] | S:[n] M:[n] L:[n] | ⬜ Not Started |
| 2 | [Feature Group Name] (P0) | [N] | S:[n] M:[n] L:[n] | ⬜ Not Started |
| ... | ... | ... | ... | ... |
| N-1 | Testing & Quality | [N] | S:[n] M:[n] L:[n] | ⬜ Not Started |
| N | DevOps & Launch | [N] | S:[n] M:[n] L:[n] | ⬜ Not Started |
| **Total** | | **[N]** | **S:[n] M:[n] L:[n]** | |

## Dependency Graph

[ASCII or markdown representation of critical-path dependencies between phases and key tasks]

Example:
```
Phase 0 ──→ Phase 1 ──→ Phase 3
                  └──→ Phase 2 ──→ Phase 4
                                       └──→ Phase 5
All feature phases ──→ Phase 6 (Testing) ──→ Phase 7 (DevOps)
```

---

## Phase 0: Project Foundation

Tasks to initialize the project with the technology stack defined in TRD.

- [ ] T-001 [Task description] [S] (TRD X.X)
  - AC: [Acceptance criteria]
  - [depends: none] [files: path/to/files]

- [ ] T-002 [Task description] [S] (TRD X.X)
  - AC: [Acceptance criteria]
  - [depends: T-001] [files: path/to/files]

---

## Phase 1: [Feature Group Name] (P0)

[Brief description of this vertical feature slice]

- [ ] T-00N [Task description] [M] (TRD X.X, PRD FR-XXX)
  - AC: [Acceptance criteria]
  - [depends: T-xxx] [files: path/to/files]

[Continue for all tasks in this phase...]

---

[Continue for all phases...]

---

## Quality Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| TDQG-001 PRD Coverage | PASS | All [N] FRs mapped |
| TDQG-002 TRD Coverage | PASS | All components covered |
| TDQG-003 No Scope Creep | PASS | No orphan tasks |
| TDQG-004 Dependency Validity | PASS | No circular deps, all refs valid |
| TDQG-005 XL Detection | PASS / WARN | [details if any XL tasks] |
| TDQG-006 Acceptance Criteria | PASS / WARN | [count of tasks without AC] |
| TDQG-007 Phase Balance | PASS / WARN | [phase sizes if imbalanced] |
| TDQG-008 Dependency Ordering | PASS / WARN | [ordering violations if any] |

---

## Notes

- Task IDs (T-xxx) are stable across updates — never reassigned
- Complexity: [S]mall < 1h, [M]edium 1-3h, [L]arge 3-6h, [XL] should be split
- Status markers: [ ] pending, [~] in-progress, [x] done, [!] blocked, [-] skipped
- Phase status: ⬜ Not Started, 🔄 In Progress, ✅ Complete, ⛔ Blocked
- All tasks trace back to PRD features or TRD specifications
- Update existing tasks with /to-do --update to preserve progress
```

## Expanded Status Model

Tasks support these status markers:

| Marker | Meaning | When to use |
|--------|---------|------------|
| `- [ ]` | Pending | Default state — task not yet started |
| `- [~]` | In-progress | Currently being worked on |
| `- [x]` | Completed | Done and verified |
| `- [!]` | Blocked | Cannot proceed — add a blocker note below the task |
| `- [-]` | Skipped | Intentionally skipped or descoped |

Phase summary status column uses:
- `⬜ Not Started` — no tasks started
- `🔄 In Progress` — at least one task in progress or completed
- `✅ Complete` — all tasks completed or skipped
- `⛔ Blocked` — at least one task blocked, no active progress

**Integration note:** The `/autonomous-development` skill currently recognizes `- [ ]` and `- [x]`. The new statuses (`[~]`, `[!]`, `[-]`) are forward-compatible — autonomous-dev treats `[~]` as incomplete (correct behavior), skips `[-]` naturally (no `[ ]` match), and can be taught to report `[!]` blockers. No changes to autonomous-dev are needed for basic compatibility.

---

# UPDATE MODE

Incremental re-generation that preserves existing task IDs and statuses while reflecting changes to PRD/TRD.

## When to Use

```
/to-do --update
```

Use after modifying `dev-docs/prd.md` or `dev-docs/trd.md` to sync the task breakdown without losing progress on completed or in-progress tasks.

## Update Procedure

1. **Read existing** `dev-docs/to-do.md` — parse all task IDs and their current statuses (`[ ]`, `[x]`, `[~]`, `[!]`, `[-]`)
2. **Read current** PRD and TRD
3. **Re-run archetype detection** and phase generation based on updated documents
4. **For each existing task:**
   - If the task's source FR/TRD section still exists → **preserve** task ID and status
   - If the source was removed from PRD/TRD → mark task `[-]` with note "(source removed in update)"
   - If the source was modified → **preserve** status, **update** description and acceptance criteria to match
5. **For new FRs/TRD sections** not covered by existing tasks:
   - Generate new tasks with the next available sequential T-xxx ID
   - Insert into the appropriate phase based on domain grouping
6. **Re-run quality gates** (TDQG-001 through TDQG-008)
7. **Write updated** `dev-docs/to-do.md`

## Key Invariants

- **Task IDs are never reassigned.** `T-001` always refers to the same task, even across updates. Deleted tasks leave a gap in the numbering.
- **Completed tasks are never reverted.** If `T-005` is `[x]` and its FR still exists, it stays `[x]`.
- **New tasks get the next sequential ID.** If the highest existing ID is `T-087`, new tasks start at `T-088`.
- **Phase structure may change.** If the archetype or feature grouping changes, tasks may move between phases while retaining their IDs.

## Error Handling

```
If dev-docs/to-do.md does not exist:
  1. Inform user that --update requires an existing task breakdown
  2. Fall back to solo mode for fresh generation
```

---

# TEAM MODE

Decompose + Validate task breakdown generation using agent teams. Spawns 1 Decomposer who generates the full task breakdown, reviewed by 1 Validator for coverage, granularity, and correctness. The lead revises based on validation feedback.

**How this differs from PRD and TRD team modes:**
- 2 agents only (lightest team model — vs TRD's 3-5, PRD's 3-6)
- 1 decomposer + 1 validator (not parallel researchers or draft + review)
- No specialist pool — task decomposition is domain-agnostic
- No user questions — PRD and TRD already contain all context

## Team Model: Decompose + Validate

```
Lead: Read PRD + TRD + detect archetype
  ↓
Lead: Spawn 1 Decomposer + 1 Validator
  ↓
Decomposer: Writes FULL task breakdown → .todo-workspace/tasks-draft.md
  ↓
Validator: Reviews draft → .todo-workspace/validation-review.md
  ↓
Lead: Reads review + revises draft → applies quality gates → writes dev-docs/to-do.md
  ↓
Lead: Cleanup (shutdown teammates → TeamDelete → delete workspace)
```

**Why Decompose + Validate (not Research+Debate or Draft+Review):**
- Task breakdown is a decomposition problem, not a creative/architectural one
- 1 decomposer produces better consistency than parallel decomposers
- 1 validator catches coverage gaps, ordering issues, and granularity problems
- No domain specialists needed — task decomposition is domain-agnostic
- Lightest team model: only 2 agents

## Team Roles

| Role | Name | Job |
|------|------|-----|
| Lead | (you) | Coordinator: intake, archetype detection, spawn, revision, quality gates, cleanup |
| Decomposer | `decomposer` | Reads PRD+TRD, generates full task breakdown with IDs/metadata/AC |
| Validator | `validator` | Reviews task breakdown for coverage, granularity, ordering, dependency correctness |

## Team Step 1: Lead Intake

No questions needed — the PRD and TRD already contain all context. Lead simply:
1. Reads `dev-docs/prd.md` and `dev-docs/trd.md`
2. Detects project archetype (using Step 2 logic from Solo Mode)
3. Creates workspace:

```bash
mkdir -p .todo-workspace
```

Also add `.todo-workspace/` to `.gitignore` if not already present.

**File naming convention:**
- Draft: `.todo-workspace/tasks-draft.md`
- Validation review: `.todo-workspace/validation-review.md`

**Why files instead of messages:** SendMessage content is ephemeral — if the lead's context compacts or messages are consumed before rendering, the data is lost. Files persist on disk and can be re-read at any time.

## Team Step 2: Spawn Team

Spawn Decomposer + Validator. Don't require plan approval.

| Teammate | Name | Role | Always? |
|----------|------|------|---------|
| 1 | `decomposer` | Generates the full task breakdown | Yes |
| 2 | `validator` | Reviews the task breakdown | Yes |

**Spawn configuration:**
- Require plan approval: NO (teammates should work freely)
- Use delegate mode: YES (lead should not implement, only coordinate)
- Model for teammates: Use the same model as the lead session

### Decomposer Spawn Prompt

```
You are the Task Decomposer for a to-do team. Your job is to read the PRD and
TRD and generate a COMPLETE task breakdown following the v2.0 format.

PRD LOCATION: dev-docs/prd.md
TRD LOCATION: dev-docs/trd.md
DETECTED ARCHETYPE: [archetype]

INSTRUCTIONS:

1. Read dev-docs/prd.md thoroughly — extract all FRs, user stories, priorities.
2. Read dev-docs/trd.md thoroughly — extract tech stack, DB schema, API endpoints,
   architecture decisions.

3. Generate a COMPLETE task breakdown following these rules:

PHASE STRUCTURE:
- Phase 0: Project Foundation (always first — env, deps, config)
- Phases 1-N: Vertical feature slices grouped by domain (P0 first, then P1, P2)
- Phase N-1: Testing & Quality (integration/E2E — always second-to-last)
- Phase N: DevOps & Launch (CI/CD, deploy, monitoring — always last)

TASK FORMAT (every task MUST follow this format):
- [ ] T-XXX Description [S/M/L/XL] (TRD X.X, PRD FR-XXX)
  - AC: Testable acceptance criterion
  - [depends: T-XXX or none] [files: likely/file/paths]

RULES:
- Every PRD FR must map to at least 1 task
- Every TRD component (model, endpoint, infra) must have at least 1 task
- No tasks beyond PRD/TRD scope
- No [XL] tasks — decompose them further
- Task IDs sequential: T-001, T-002, ...
- Acceptance criteria: 1-3 testable conditions per task
- Dependencies: reference by task ID, or "none"
- Complexity: [S] <1h, [M] 1-3h, [L] 3-6h

4. Include the full document structure:
   - Header with metadata (product name, dates, archetype, totals)
   - Summary table with phase breakdown and complexity counts
   - Dependency Graph section
   - All phases with tasks
   - Notes section

OUTPUT:
1. Write complete task breakdown to: .todo-workspace/tasks-draft.md
2. Send a SHORT notification to team lead confirming draft is ready.
   Summarize: total tasks, phase count, archetype used.
```

### Validator Spawn Prompt

```
You are the Task Validator for a to-do team. Your job is to review the
Decomposer's task breakdown for completeness, consistency, and quality.

PRD LOCATION: dev-docs/prd.md
TRD LOCATION: dev-docs/trd.md
TASK DRAFT LOCATION: .todo-workspace/tasks-draft.md

INSTRUCTIONS:

1. Read dev-docs/prd.md — note all FRs and their priorities.
2. Read dev-docs/trd.md — note all components and architecture.
3. Read .todo-workspace/tasks-draft.md — this is the Decomposer's draft.

4. Validate against these criteria:

COVERAGE CHECK:
- Does every PRD FR map to at least 1 task? List any gaps.
- Does every TRD component have a task? List any gaps.
- Are there any orphan tasks (no PRD/TRD source)? Flag them.

GRANULARITY CHECK:
- Are any tasks too large (should be [XL] or split)?
- Are any tasks too small (could be merged)?
- Is complexity tagging consistent?

ORDERING CHECK:
- Are dependencies valid (no circular refs, no forward refs within phase)?
- Is phase ordering logical (foundations first, features middle, deploy last)?
- Within each phase, do dependencies come before dependents?

QUALITY CHECK:
- Do all tasks have acceptance criteria?
- Are acceptance criteria testable (not vague)?
- Is the vertical slicing appropriate (not horizontal layering)?
- Are task descriptions specific enough to implement?

5. Write your review in this format:

## Validation Review

### Summary
[2-3 sentence overall assessment]

### Critical Issues (must fix)
- [Issue]: [What's wrong] → [Fix]

### Important Issues (should fix)
- [Issue]: [What's wrong] → [Fix]

### Suggestions
- [Suggestion]: [Rationale]

### Coverage Matrix
| PRD FR | Mapped Tasks | Status |
|--------|-------------|--------|
| FR-001 | T-001, T-003 | OK |
| FR-002 | (none) | MISSING |

OUTPUT:
1. Write complete review to: .todo-workspace/validation-review.md
2. Send SHORT notification to team lead confirming review is ready.
   Summarize: coverage %, critical issues count, top concern.
```

## Team Step 3: Draft Phase

**CRITICAL LEAD INSTRUCTION:** Wait for the Decomposer to complete the task breakdown before proceeding. Do NOT start the validation phase until the Decomposer has confirmed the draft is written to `.todo-workspace/tasks-draft.md`.

**Lead behavior during draft phase:**
- Wait for the Decomposer to finish
- If the Decomposer goes idle without sending a notification, send a direct message prompting them
- When the Decomposer confirms the draft is ready, verify the file exists by reading `.todo-workspace/tasks-draft.md`
- If the file is missing or empty after confirmation, send them a direct message asking them to rewrite it
- Do NOT start writing the task breakdown yourself
- Only proceed to Team Step 4 when the draft file exists and is non-empty

## Team Step 4: Validation Phase

Once draft is confirmed, send a message to the Validator to begin review:

```
The Decomposer has completed the task breakdown draft. Please review it now.

Read these files using the Read tool:
- PRD: dev-docs/prd.md
- TRD: dev-docs/trd.md
- Task Draft: .todo-workspace/tasks-draft.md

Write your review to: .todo-workspace/validation-review.md

After writing, send a SHORT notification to the team lead confirming
your review is ready. Do NOT include the full review in the message —
just confirm the file is written and summarize your top 2-3 findings.
```

**Lead behavior during validation phase:**
- Wait for the Validator to complete the review
- If the Validator goes idle without sending a notification, send a direct message prompting them
- Only proceed to Team Step 5 when the validation review file exists and is non-empty

## Team Step 5: Lead Revision & Quality Gates

**IMPORTANT**: The lead performs the revision directly — NOT a subagent.

**Why the lead does the revision:**
The revision task requires reading the full task draft plus the validation review plus writing a revised document. The lead already has full conversation context from the draft and review phases, making it the natural performer for revision.

**Lead revision procedure:**

1. Read `.todo-workspace/tasks-draft.md` (the original draft)
2. Read `.todo-workspace/validation-review.md` (the validation review)
3. For each review finding:
   - **Critical Issues**: MUST address — fix the issue or provide explicit rationale for why not
   - **Important Issues**: SHOULD address — fix or add a note
   - **Suggestions**: MAY incorporate if they improve the document
4. Apply revisions to create the final task breakdown
5. Run all quality gates (TDQG-001 through TDQG-008) on the revised version
6. Fix any ERROR-level quality gate failures
7. Add Quality Gate Results table
8. Add team mode header: `> Mode: Team (Decomposer + Validator)`
9. Write the final task breakdown to `dev-docs/to-do.md`

## Team Step 6: Cleanup

After the task breakdown is written and quality gates pass:
1. Send shutdown requests to Decomposer and Validator
2. Wait for shutdown confirmations
3. Clean up the team (TeamDelete)
4. Delete the workspace: remove `.todo-workspace/` directory
5. Report results to user (include quality gate summary and validation highlights)

---

# QUALITY GATES

## Universal Quality Gates

Applied to EVERY task breakdown (solo and team mode).

| Gate | Name | Severity | Detection Logic |
|------|------|----------|-----------------|
| TDQG-001 | PRD Coverage | ERROR | Every PRD Functional Requirement (FR-xxx) must map to at least 1 task. List each FR and the task(s) that address it. Flag any FR without coverage. |
| TDQG-002 | TRD Coverage | ERROR | Every TRD component (database model, API endpoint, infrastructure element) must have at least 1 task. Flag orphan components with no corresponding task. |
| TDQG-003 | No Scope Creep | ERROR | Every task must trace back to a PRD FR or TRD section via its traceability reference. Flag any task without a valid `(TRD X.X, PRD FR-XXX)` reference. |
| TDQG-004 | Dependency Validity | ERROR | No circular dependencies allowed. All `[depends: T-xxx]` references must point to valid, existing task IDs. Build a dependency DAG and verify it is acyclic. |
| TDQG-005 | XL Detection | WARNING | Flag any task tagged `[XL]`. XL tasks should be decomposed into smaller tasks. Suggest how to split each XL task. |
| TDQG-006 | Acceptance Criteria | WARNING | Every task should have at least 1 AC line. Flag tasks without acceptance criteria and count the total. |
| TDQG-007 | Phase Balance | WARNING | No phase should have more than 15 tasks or fewer than 2 tasks. Flag imbalanced phases and suggest merging or splitting. |
| TDQG-008 | Dependency Ordering | WARNING | Within each phase, tasks should be ordered so that dependencies come before dependents. Flag any case where a task depends on a later task within the same phase. |

## Gate Enforcement Procedure

1. After generating/receiving the task breakdown, scan for each gate (TDQG-001 through TDQG-008)
2. For ERROR gates: fix the issue inline before writing the final output
3. For WARNING gates: note in the Quality Gate Results section
4. Append Quality Gate Results table to the output document:

```markdown
## Quality Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| TDQG-001 PRD Coverage | PASS / FAIL | [FR mapping details] |
| TDQG-002 TRD Coverage | PASS / FAIL | [component mapping details] |
| TDQG-003 No Scope Creep | PASS / FAIL | [orphan task details if FAIL] |
| TDQG-004 Dependency Validity | PASS / FAIL | [circular dep details if FAIL] |
| TDQG-005 XL Detection | PASS / WARN | [XL task list if any] |
| TDQG-006 Acceptance Criteria | PASS / WARN | [count of tasks without AC] |
| TDQG-007 Phase Balance | PASS / WARN | [imbalanced phases if any] |
| TDQG-008 Dependency Ordering | PASS / WARN | [ordering violations if any] |
```

---

# PROJECT ARCHETYPES

Reference table of all supported archetypes with their detection signals and phase structure templates.

| Archetype | Detection Signals | Phase Template |
|-----------|-------------------|----------------|
| Full-stack web app | Frontend framework (React, Vue, Angular, Svelte) + backend API (Express, Fastify, Django, Rails) + database (PostgreSQL, MongoDB, MySQL) | Foundation → Feature slices → Testing → DevOps |
| Frontend-only (SPA) | No backend in TRD, or BaaS (Firebase, Supabase); heavy client-side state; design system focus | Foundation → UI feature groups → Testing → DevOps |
| API/Backend-only | No UI; API endpoints listed; microservices; REST/GraphQL/gRPC | Foundation → API domain groups → Testing → DevOps |
| CLI tool | Command-line, terminal, argv parsing; no web UI | Foundation → Command groups → Testing → DevOps |
| Mobile app | React Native, Flutter, Swift, Kotlin; app store deployment | Foundation → Screen/flow groups → Testing → DevOps |
| Data pipeline | ETL, batch processing, Airflow, Spark, analytics | Foundation → Pipeline stages → Testing → DevOps |
| Library/SDK | npm/pip/crate package; public API surface; semver versioning | Foundation → API surface groups → Testing → DevOps |
| Serverless/Event-driven | Lambda, Cloud Functions, EventBridge, SQS, event bus | Foundation → Event handler groups → Testing → DevOps |

**Fallback:** If signals are ambiguous or match multiple archetypes, default to "Full-stack web app" as the most common pattern.

---

# DEPENDENCY HANDLING

Tasks within and across phases should respect dependencies:

```
Good ordering (dependencies first):
- [ ] T-010 Create User model with email, password fields [M] (TRD 3.2, PRD FR-001)
  - AC: User table exists with all specified fields
  - [depends: none]

- [ ] T-011 Create Post model with title, body, user_id fields [M] (TRD 3.2, PRD FR-003)
  - AC: Post table exists with user_id foreign key
  - [depends: T-010]

- [ ] T-012 Add User -> Posts one-to-many relationship [S] (TRD 3.1, PRD FR-003)
  - AC: User.posts relation returns associated posts; cascade delete works
  - [depends: T-010, T-011]

Bad ordering (dependency violation):
- [ ] T-012 Add User -> Posts relationship [S] (Post doesn't exist yet!)
- [ ] T-010 Create User model
- [ ] T-011 Create Post model
```

Cross-phase dependencies are allowed and expected — feature slices often depend on foundation tasks.

---

# INTEGRATION

## Integration with Autonomous Development

The generated task document is designed to work with the `/autonomous-development` skill:

1. **Format Compatibility**: Uses the standard `- [ ]` checkbox format
2. **Phase Structure**: Phases can be executed sequentially
3. **Status Tracking**: Summary table tracks completion with expanded status model
4. **Traceability**: References enable context lookup during implementation
5. **Task IDs**: Provide stable references for commit messages and progress tracking

**Workflow:**
```
/prd <idea> → /trd → /to-do → /autonomous-development
```

**Update workflow:**
```
[Modify PRD/TRD] → /to-do --update → /autonomous-development
```

## Output

- **File**: `dev-docs/to-do.md`
- **Format**: Markdown with checkbox tasks, task IDs, and metadata
- **Traceability**: References to PRD/TRD sections on every task
- **Compatibility**: Works with /autonomous-development skill
- **Mode indicator**: Team-generated breakdowns include `> Mode: Team (Decomposer + Validator)` in header

---

# ERROR HANDLING

### PRD Not Found
```
If dev-docs/prd.md does not exist:
  1. Inform user that PRD is required
  2. Suggest running /prd first
  3. Cannot proceed without PRD
```

### TRD Not Found
```
If dev-docs/trd.md does not exist:
  1. Inform user that TRD is required
  2. Suggest running /trd first
  3. Cannot proceed without TRD
```

### Incomplete Documents
```
If PRD/TRD are missing critical sections:
  1. List the missing sections
  2. Explain what tasks cannot be generated
  3. Suggest updating the documents first
```

### Update Mode — No Existing To-Do
```
If dev-docs/to-do.md does not exist and --update is used:
  1. Inform user that --update requires existing to-do.md
  2. Fall back to solo mode for fresh generation
```

---

# EXAMPLE SESSION

## Solo Mode Example

```
User: /to-do
Assistant: I will read the PRD and TRD to generate a development task breakdown.

[Reads dev-docs/prd.md - water intake tracking app with 12 FRs]
[Reads dev-docs/trd.md - React Native + Node.js + PostgreSQL architecture]
[Detects archetype: Full-stack web app (mobile variant)]

Based on the documents, I will create a structured task list with vertical
feature slices organized by domain.

[Writes dev-docs/to-do.md with 7 phases and 64 tasks]
Assistant: I have created the task breakdown at dev-docs/to-do.md. Summary:

Archetype: Full-stack web app
Phase 0: Project Foundation - 8 tasks (S:5 M:3)
Phase 1: User Management — P0 - 10 tasks (S:3 M:5 L:2)
Phase 2: Water Tracking & Logging — P0 - 12 tasks (S:2 M:7 L:3)
Phase 3: Reminders & Notifications — P1 - 9 tasks (S:3 M:4 L:2)
Phase 4: Analytics & Reports — P2 - 7 tasks (S:1 M:4 L:2)
Phase 5: Testing & Quality - 10 tasks (S:2 M:6 L:2)
Phase 6: DevOps & Launch - 8 tasks (S:4 M:3 L:1)

Total: 64 tasks (S:20 M:32 L:12 XL:0)

Quality Gates: All 8 passed (0 errors, 0 warnings)
All 12 PRD FRs mapped to tasks. No scope creep detected.
You can now run /autonomous-development to begin executing tasks.
```

## Team Mode Example

```
User: /to-do --team
Assistant: I will use team mode for validated task decomposition.

[Reads PRD and TRD, detects archetype: API/Backend-only]
[Creates .todo-workspace/]
[Spawns Decomposer and Validator]

Decomposer: Draft ready — 78 tasks across 6 phases, API-domain grouping.
Validator: Review complete — 98% FR coverage, 2 critical issues
           (missing tasks for FR-014, circular dependency T-045↔T-048),
           3 suggestions.

[Lead reads draft + review, fixes critical issues, runs quality gates]

Created dev-docs/to-do.md:
Archetype: API/Backend-only
Total: 81 tasks (S:22 M:38 L:21 XL:0)
Quality Gates: All 8 passed after revision
Mode: Team (Decomposer + Validator)

[Shuts down teammates, deletes .todo-workspace/]
```

---

# SUCCESS CRITERIA

## Solo Mode

A successful solo task breakdown generation:
- Reads and analyzes both PRD and TRD
- Detects the correct project archetype
- Creates tasks at `dev-docs/to-do.md`
- Organizes tasks into vertical feature slices (not horizontal tech layers)
- Every task has a unique stable ID (T-xxx)
- Every task has a complexity tag ([S/M/L/XL])
- Every task has acceptance criteria (AC line)
- Every task has a dependency declaration ([depends: ...])
- Every task has traceability references (PRD FR-xxx, TRD X.X)
- Every PRD feature has corresponding tasks (TDQG-001)
- Every TRD component has corresponding tasks (TDQG-002)
- No tasks introduce features not in PRD (TDQG-003)
- No circular dependencies (TDQG-004)
- Summary table accurately counts tasks and complexity per phase
- Quality gate results table is included
- Format is compatible with /autonomous-development skill

## Team Mode

A successful team task breakdown generation:
- Detects archetype before spawning team
- Spawns 1 Decomposer + 1 Validator (lightest team model)
- Waits for Decomposer draft before starting validation
- Waits for Validator review before starting revision
- Lead performs revision directly (not delegated to subagent)
- All Critical validation issues addressed or explicitly rejected with rationale
- Passes all 8 quality gates (TDQG-001 through TDQG-008)
- Includes Quality Gate Results table
- Cleans up team after task breakdown is written (shutdown requests → confirmations → TeamDelete → workspace cleanup)

## Update Mode

A successful update:
- Preserves all existing task IDs (never reassigns)
- Preserves all existing task statuses ([x], [~], [!], [-])
- Adds new tasks for new PRD FRs or TRD components
- Marks removed-source tasks as `[-]` with note
- Updates descriptions/AC for modified sources
- Re-runs quality gates on the updated breakdown
- New tasks use the next sequential ID after the highest existing

---

# NOTES

- The skill requires both PRD and TRD to exist
- Tasks are designed for the /autonomous-development workflow
- Phase count varies based on project complexity and archetype
- Vertical slicing replaces the v1.0 horizontal layering approach
- Task IDs (T-xxx) are stable across updates — designed for long-lived projects
- Quality gates (TDQG-001 through TDQG-008) ensure coverage and consistency
- Team mode requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS to be enabled
- Team mode uses Decompose + Validate (lightest team model — 2 agents only)
- Team mode without specialist uses ~2-3x more tokens than solo mode
- If team mode fails (e.g., agent teams not available), falls back to solo mode
- Update mode (`--update`) preserves progress and adds/removes tasks incrementally
- Archetype detection is automatic but can default to "Full-stack web app" if ambiguous
- If a teammate goes idle without responding, send a direct message to prompt them
