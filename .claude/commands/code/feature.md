# Feature Command

Plan, document, and implement new features through a structured orchestration workflow that updates project documents and delegates execution to autonomous development.

## Usage

```
/feature <feature description>
```

## Overview

The `/feature` command orchestrates the complete feature lifecycle:

1. **Gathers context** from existing PRD, TRD, and to-do.md
2. **Asks clarifying questions** (up to 5) to fill gaps
3. **Updates PRD** with new requirements and security considerations
4. **Updates TRD** with technical approach and security review
5. **Adds tasks** to to-do.md with proper traceability
6. **Invokes /autonomous-development** to implement

This ensures all decisions are documented and traceable, not just implemented and forgotten.

## Prerequisites

Before running `/feature`, ensure these documents exist:

| Document | Path | Created By |
|----------|------|------------|
| PRD | `dev-docs/prd.md` | `/prd` skill |
| TRD | `dev-docs/trd.md` | `/trd` skill |
| Tasks | `dev-docs/to-do.md` | `/to-do` skill |

If any document is missing, the command will prompt you to create it first.

## The Process

### Phase 1: Context Gathering

Read all project documents to understand the current state.

```
1. Read dev-docs/prd.md
   - Extract existing features (FR-XXX numbering)
   - Extract existing user stories (US-XXX numbering)
   - Note product goals and constraints
   - Identify scope boundaries

2. Read dev-docs/trd.md
   - Note technology stack
   - Understand database schema
   - Review API design patterns
   - Check existing security measures
   - Understand auth approach

3. Read dev-docs/to-do.md
   - Identify phase structure
   - Find last FR/US numbers used
   - Note current task count
   - Understand existing phases
```

**Output:** Complete understanding of project context

**Error Handling:**
```
If dev-docs/prd.md missing:
  "PRD not found. Run /prd first to define product requirements."
  EXIT

If dev-docs/trd.md missing:
  "TRD not found. Run /trd first to define technical specifications."
  EXIT

If dev-docs/to-do.md missing:
  "Task list not found. Run /to-do first to create task structure."
  EXIT
```

### Phase 2: Gap Analysis

Identify what information is missing to fully specify the feature.

**Gap Categories:**

| Category | Questions to Consider |
|----------|----------------------|
| **Scope** | Is the boundary clear? What's explicitly out? Overlap with existing? |
| **Requirements** | What are acceptance criteria? Edge cases? Error states? |
| **Technical** | New API endpoints? Database changes? Service integrations? |
| **Security** | What data is handled? Authorization needed? Input validation? |
| **UX** | How does user interact? What feedback? What on failure? |

**Gap Severity:**

| Severity | Action |
|----------|--------|
| `MUST_ASK` | Information required to proceed (show-stopper) |
| `SHOULD_ASK` | Important for quality, but has reasonable defaults |
| `CAN_INFER` | Can make reasonable assumptions from context |

**Output:** List of gaps to address through questions

### Phase 3: Clarification

Ask up to 5 targeted questions using the AskUserQuestion tool.

**Question Limit:** Maximum 5 questions (not 10 like /prd or /trd)

**Rationale:** /feature is for discrete additions, not full specifications. If more than 5 questions are needed, the feature may need to be broken down or the PRD/TRD may need updates first.

**Question Priority Order:**

```
1. SCOPE (if unclear)
   "What specific functionality should [feature] include?"
   Options: [Minimal MVP] [Full feature] [Custom...]

2. TECHNICAL APPROACH (if multiple valid approaches)
   "How should [feature] be implemented?"
   Options: [Client-side] [Server-side] [Hybrid] [Custom...]

3. SECURITY/AUTH (if feature handles data or access)
   "What authorization level is required for [feature]?"
   Options: [Public] [Logged-in users] [Admin only] [Custom...]

4. UX/INTERACTION (if user-facing)
   "How should users interact with [feature]?"
   Options: [Modal dialog] [Inline/Embedded] [New page] [Custom...]

5. EDGE CASES (if complex scenarios exist)
   "How should [scenario] be handled?"
   Options: [Fail silently] [Show error] [Auto-retry] [Custom...]
```

**Skip Conditions:**
- Don't ask if PRD/TRD already specifies the answer
- Don't ask if a reasonable default exists
- Don't ask implementation details (save for coding phase)
- Batch related questions (max 4 per AskUserQuestion call)

**Output:** User answers integrated into feature specification

### Phase 4: Document Updates

Persist all decisions by updating the three core documents.

#### 4A: Update PRD (dev-docs/prd.md)

**Where to Add:**
- Section 4 (User Stories) - Add new US-XXX entries
- Section 5 (Features & Requirements) - Add new FR-XXX entry
- Section 5.3 (Non-Functional Requirements/Security) - Add security requirements

**Format for New Feature Requirement:**

```markdown
#### FR-XXX: [Feature Name]
- **Description**: [Detailed description from clarification]
- **Priority**: [P0/P1/P2]
- **User Stories**: US-XXX
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] [Criterion 3]
- **Security Considerations**:
  - [Security requirement 1]
  - [Security requirement 2]
- **Dependencies**: [Any dependencies]
```

**Format for New User Story:**

```markdown
| US-XXX | [user type] | [action/goal] | [benefit/value] | [P0/P1/P2] |
```

#### 4B: Update TRD (dev-docs/trd.md)

**Where to Add (as applicable):**
- Section 3 (Database Design) - If new models/fields needed
- Section 4 (API Design) - If new endpoints needed
- Section 5 (Authentication & Authorization) - If auth changes needed
- Section 14 (Security Considerations) - **ALWAYS** add security review

**Format for New API Endpoints:**

```markdown
#### [Feature Name] Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/[resource]/[action] | [Description] | Required |
| GET | /api/[resource]/[action] | [Description] | Required |
```

**Format for Database Changes:**

```markdown
#### [Table Name] (for [Feature])

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| [field] | [type] | [constraints] | [description] |
```

**Format for Security Review (ALWAYS ADD):**

```markdown
### Security Review: [Feature Name]

#### Input Validation
- [Field/Input]: [Validation rules, sanitization]

#### Authorization
- [Who can access]: [Permission level, checks required]

#### Data Protection
- [What data]: [How stored, transmitted, protected]

#### Attack Vectors Mitigated
- [ ] [Attack type]: [Mitigation strategy]
- [ ] [Attack type]: [Mitigation strategy]

#### Rate Limiting
- [Endpoint/Action]: [Limit per time period]
```

#### 4C: Update to-do.md (dev-docs/to-do.md)

**Strategy:**
1. If feature fits existing phase → Add tasks to that phase
2. If feature is standalone → Create new "Feature: [Name]" phase

**Format for Adding to Existing Phase:**

```markdown
### [Feature Name] (PRD FR-XXX)
- [ ] [Task 1] (PRD FR-XXX)
- [ ] [Task 2] (TRD X.X)
- [ ] [Task 3] (PRD FR-XXX, TRD X.X)
- [ ] Write tests for [feature] (TRD 11)
```

**Format for New Feature Phase:**

```markdown
---

## Phase N: Feature - [Feature Name]

Tasks to implement [brief description] per PRD FR-XXX.

### Database & Models
- [ ] Create [table/model] migration (TRD 3.X)
- [ ] Add [fields] to [model] (TRD 3.X)

### API Endpoints
- [ ] Implement [METHOD] /api/[endpoint] (TRD 4.X)
- [ ] Add request validation for [endpoint] (TRD 4.X)
- [ ] Add rate limiting to [endpoint] (TRD 14.X)

### Business Logic
- [ ] Create [service/function] for [logic] (PRD FR-XXX)
- [ ] Implement [specific behavior] (PRD FR-XXX)
- [ ] Handle [edge case] (PRD FR-XXX)

### UI Components (if applicable)
- [ ] Create [component] for [purpose] (PRD FR-XXX)
- [ ] Add [interaction] to [component] (PRD FR-XXX)

### Testing
- [ ] Write unit tests for [service/logic] (TRD 11.1)
- [ ] Write integration tests for [endpoint] (TRD 11.1)
- [ ] Write E2E tests for [user flow] (TRD 11.1)

---
```

**Update Summary Table:**

Add new phase to the summary table at the top of to-do.md:

```markdown
| N | Feature - [Name] | [task count] | ⬜ |
```

**Update Total:**

Increment the total task count in the summary.

**Output:** All three documents updated with feature specification

### Phase 5: Summary & Confirmation

Display what was added before executing.

**Output Format:**

```
## Feature Planning Complete: [Feature Name]

### PRD Updates (dev-docs/prd.md)
- Added FR-XXX: [Brief requirement description]
- Added US-XXX: [Brief user story]
- Security: [Key security considerations]

### TRD Updates (dev-docs/trd.md)
- API: [Endpoints added, if any]
- Database: [Schema changes, if any]
- Security Review: Added to Section 14

### Tasks Added (dev-docs/to-do.md)
- Phase [N]: [N] new tasks
- References: PRD FR-XXX, TRD X.X

### Execution
Invoking /autonomous-development to implement...
```

### Phase 6: Execution Handoff

Invoke `/autonomous-development` to implement the feature tasks.

```
Invoke using Skill tool:
- skill: "autonomous-dev"
```

The autonomous development skill will:
1. Read dev-docs/to-do.md
2. Find first unchecked task (the ones just added)
3. Look up PRD/TRD references for context
4. Implement each task
5. Run `/codex-review` after each task (MANDATORY)
6. Fix any review findings (up to 3 retries)
7. Commit on success
8. Continue until all feature tasks complete or blocked

**Output:** Feature implemented, reviewed, and committed

## Question Strategy

### Adaptive Questioning

The number and type of questions adapt to the feature description:

**Minimal Description** (just a feature name):
- Ask 4-5 questions covering scope, tech, security, UX

**Moderate Description** (feature + some context):
- Ask 2-3 questions focusing on gaps

**Detailed Description** (comprehensive request):
- Ask 0-1 clarifying questions or proceed directly

### Question Batching

Use AskUserQuestion efficiently:
- Group related questions (max 4 per call)
- Provide sensible defaults as first option with "(Recommended)"
- Include "Other" option for custom responses
- Use multiSelect: true only when choices aren't mutually exclusive

### Context-Driven Questions

Always derive questions from PRD/TRD context:
- If PRD mentions "user roles" → Ask about authorization level
- If TRD uses "REST API" → Frame questions around endpoints
- If existing auth is "JWT" → Don't ask about auth method
- If security section exists → Reference existing patterns

## Task Decomposition Guidelines

### Task Granularity

Each task should be:
- Completable in 1-4 hours of focused work
- Independently testable
- Clearly traceable to PRD/TRD

### Task Ordering

Order tasks by dependency:
```
1. Database/Schema changes (no dependencies)
2. Service/Business logic (depends on schema)
3. API endpoints (depends on services)
4. UI components (depends on API)
5. Tests (depends on implementation)
```

### Traceability Format

Every task must reference its source:
```
- [ ] Task description (PRD FR-XXX)     # References PRD requirement
- [ ] Task description (TRD X.X)        # References TRD section
- [ ] Task description (PRD FR-XXX, TRD X.X)  # References both
```

## Security Review Requirements

**Every feature MUST have a security review added to TRD Section 14.**

Even for "simple" features, document:
1. What inputs the feature accepts
2. Who can access the feature
3. What data is involved
4. What attack vectors are mitigated

This creates an audit trail and ensures security is considered upfront.

## Example Session

```
User: /feature Add password reset functionality

Claude: I'll help you add password reset functionality. Let me first
gather context from your existing documents.

[Reads prd.md - User authentication system, FR-001 to FR-011 exist]
[Reads trd.md - Next.js + PostgreSQL + JWT auth, has users table]
[Reads to-do.md - 9 phases, 87 tasks, Phase 3 is Authentication]

Based on your current authentication system (JWT-based, email/password login),
I have a few questions to ensure we implement password reset correctly:

┌────────────────────────────────────────────────────────────────────┐
│ Q1: Reset Method                                                   │
│ How should users request a password reset?                         │
│ ○ Email link only (Recommended) - Secure reset link sent to email  │
│ ○ Email + SMS - Choose between email link or SMS code              │
│ ○ Security questions - Answer preset questions to reset            │
├────────────────────────────────────────────────────────────────────┤
│ Q2: Token Expiration                                               │
│ How long should the reset link remain valid?                       │
│ ○ 1 hour (Recommended) - Balance of security and convenience       │
│ ○ 15 minutes - High security, may frustrate users                  │
│ ○ 24 hours - Convenient but longer exposure window                 │
├────────────────────────────────────────────────────────────────────┤
│ Q3: Rate Limiting                                                  │
│ How many reset requests allowed per email per hour?                │
│ ○ 3 requests/hour (Recommended) - Prevents abuse                   │
│ ○ 1 request/hour - Very strict                                     │
│ ○ 5 requests/hour - More lenient                                   │
└────────────────────────────────────────────────────────────────────┘

User: [Selects: Email link only, 1 hour, 3 requests/hour]

Claude: Perfect. Let me update your project documents and create
implementation tasks.

## Feature Planning Complete: Password Reset

### PRD Updates (dev-docs/prd.md)
- Added FR-012: Password Reset via Email Link
- Added US-016: As a user, I want to reset my forgotten password via email
- Security: Token expiration (1h), rate limiting (3/h), one-time use tokens

### TRD Updates (dev-docs/trd.md)
- API: POST /api/auth/forgot-password, POST /api/auth/reset-password
- Database: password_reset_tokens table (user_id, token_hash, expires_at)
- Security Review: Added comprehensive review to Section 14

### Tasks Added (dev-docs/to-do.md)
- Phase 3 (Authentication): 8 new tasks added
- References: PRD FR-012, TRD 3.2, TRD 4.2, TRD 5.1, TRD 14.1

### Execution
Invoking /autonomous-development to implement...

[/autonomous-development takes over]

=== Autonomous Development Session Started ===

[SCAN] Reading tasks document...
[FOUND] First incomplete task: Phase 3 > Password Reset > Create
        password_reset_tokens table migration (TRD 3.2)

[CONTEXT] Loading PRD FR-012 for acceptance criteria...
[CONTEXT] Loading TRD 3.2 for database conventions...

[EXECUTE] Creating migration for password_reset_tokens...
[EXECUTE] Task implementation complete

[REVIEW] Invoking /codex-review...
[REVIEW] Review complete - PASSED

[COMMIT] Creating commit...
feat(db): Add password_reset_tokens table migration

[STATUS] Updating task to [x]

[SCAN] Looking for next task...
[FOUND] Next task: Phase 3 > Password Reset > Implement token
        generation service (PRD FR-012)

... continues until all 8 tasks complete ...

=== Session Summary ===
Tasks completed: 8/8
Commits: 8
Review: All passed
Feature: Password Reset - COMPLETE
```

## Integration with Other Commands

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete Workflow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  New Project:                                                   │
│  /prd <idea> ──► /trd ──► /to-do ──► /autonomous-development   │
│                                                                 │
│  Add Feature to Existing Project:                               │
│  /feature <desc> ──► (updates PRD/TRD/to-do)                    │
│                  ──► /autonomous-development (auto-invoked)     │
│                                                                 │
│  Manual Development:                                            │
│  /feature <desc> ──► (updates docs) ──► Stop here              │
│  Later: /autonomous-development (run manually)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Error Handling

### Missing Documents
```
PRD missing: "Run /prd first to define product requirements."
TRD missing: "Run /trd first to define technical specifications."
to-do missing: "Run /to-do first to create task structure."
```

### Feature Too Large
```
If gap analysis reveals > 5 critical questions:
  "This feature may be too large for a single /feature command.
   Consider:
   1. Breaking it into smaller features
   2. Updating PRD/TRD with /prd or /trd first
   3. Providing more detail in the description"
```

### Duplicate Feature
```
If similar FR-XXX already exists:
  "A similar feature (FR-XXX: [name]) already exists.
   Did you mean to:
   1. Extend the existing feature?
   2. Add a new variant?
   3. Replace the existing feature?"
```

## Success Criteria

A successful /feature execution:
- [ ] Reads and analyzes PRD, TRD, and to-do.md
- [ ] Asks relevant clarifying questions (0-5)
- [ ] Updates PRD with new FR-XXX and US-XXX entries
- [ ] Updates TRD with technical details and security review
- [ ] Adds properly traced tasks to to-do.md
- [ ] Displays clear summary of all changes
- [ ] Invokes /autonomous-development for execution
- [ ] All tasks pass /codex-review
- [ ] Feature is committed and documented

## Notes

- Maximum 5 clarifying questions (feature should be focused)
- Security review is ALWAYS added to TRD (no exceptions)
- Tasks MUST have PRD/TRD traceability references
- /autonomous-development handles actual implementation
- All decisions are persisted in documents (not just implemented)
- Feature can be resumed if interrupted (tasks remain in to-do.md)
