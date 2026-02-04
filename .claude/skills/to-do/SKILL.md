---
name: to-do
description: Generate a development task breakdown from the existing PRD and TRD. Use when asked to create a task list, plan development work, or break down implementation into phases. Invoked as "/to-do".
metadata:
  author: custom
  version: "1.0.0"
---

# Development Task Breakdown Generator

Generate structured development task lists based on the Product Requirements Document (PRD) and Technical Requirements Document (TRD). This skill decomposes the implementation into actionable tasks organized by phases.

## Overview

When invoked with `/to-do`, this skill:
1. Reads and analyzes the PRD from `dev-docs/prd.md`
2. Reads and analyzes the TRD from `dev-docs/trd.md`
3. Decomposes requirements into actionable development tasks
4. Organizes tasks into logical phases
5. Generates a task document at `dev-docs/to-do.md`

## Input Format

```
/to-do
```

No arguments required. The skill reads context from PRD and TRD.

## Prerequisites

Before running, ensure:
- PRD exists at `dev-docs/prd.md`
- TRD exists at `dev-docs/trd.md`

If either document is missing, the skill will prompt for the missing information or suggest running `/prd` or `/trd` first.

## Core Principles

**CRITICAL**: This skill must adhere to the following principles:

1. **No New Features**: Tasks must only implement what is defined in PRD/TRD
2. **No Contradictions**: Tasks must align with both PRD and TRD specifications
3. **Traceability**: Each task should trace back to a PRD feature or TRD component
4. **Completeness**: All PRD features and TRD components must have corresponding tasks
5. **Actionability**: Each task must be specific enough to implement
6. **Testability**: Each task should have implicit or explicit acceptance criteria

## The Process

### Step 1: Read and Parse Documents

Read both documents and extract key information:

**From PRD (`dev-docs/prd.md`):**
```
1. Product name and overview
2. User stories (US-XXX) with priorities (P0/P1/P2)
3. Functional requirements (FR-XXX)
4. Non-functional requirements
5. Features with priorities
6. Scope boundaries (in/out of scope)
7. Success metrics
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
```

### Step 2: Map Requirements to Tasks

Create a mapping between PRD/TRD elements and development tasks:

| Source | Task Category |
|--------|---------------|
| TRD: Technology Stack | Phase 1: Project Setup |
| TRD: Database Design | Phase 2: Database & Data Layer |
| TRD: Auth Strategy | Phase 3: Authentication |
| TRD: API Design | Phase 4: API Development |
| PRD: P0 Features | Phase 5: Core Features |
| PRD: P1 Features | Phase 6: Extended Features |
| TRD: Testing Strategy | Phase 7: Testing |
| TRD: Infrastructure | Phase 8: DevOps & Deployment |
| PRD: P2 Features | Phase 9: Polish & Optimization |

### Step 3: Generate Task Breakdown

For each phase, create granular tasks following these guidelines:

**Task Granularity Rules:**
- Each task should be completable in 1-4 hours of focused work
- Complex features should be broken into multiple tasks
- Tasks should be independent where possible
- Dependencies should be reflected in task ordering

**Task Naming Convention:**
- Start with action verb (Create, Implement, Add, Configure, Set up, Write, etc.)
- Be specific about what is being done
- Include component/file name when relevant
- Avoid vague terms like "handle", "manage", "process"

**Good Task Examples:**
```
- [ ] Create User model with email, password_hash, and created_at fields
- [ ] Implement POST /api/auth/register endpoint with validation
- [ ] Add password strength validation (min 8 chars, 1 uppercase, 1 number)
- [ ] Configure GitHub Actions workflow for CI
- [ ] Write unit tests for UserService.createUser()
```

**Bad Task Examples (avoid):**
```
- [ ] Handle user authentication (too vague)
- [ ] Set up the database (not specific enough)
- [ ] Make things work (meaningless)
- [ ] Implement everything for users (too broad)
```

### Step 4: Validate Against PRD/TRD

Before finalizing, verify:

```
Checklist:
[ ] Every P0 feature from PRD has corresponding tasks
[ ] Every P1 feature from PRD has corresponding tasks
[ ] Every API endpoint from TRD has implementation task
[ ] Every database model from TRD has creation task
[ ] Authentication approach from TRD is reflected in tasks
[ ] Testing strategy from TRD has corresponding test tasks
[ ] No tasks introduce features not in PRD
[ ] No tasks contradict TRD architecture decisions
[ ] Task order respects dependencies
[ ] All scope items are covered
```

### Step 5: Generate the Document

Create the task document at `dev-docs/to-do.md` with the following structure:

```markdown
# Development Tasks: [Product Name]

> Generated: [Date]
> Based on PRD: v[version]
> Based on TRD: v[version]
> Total Tasks: [count]
> Status: Not Started

## Summary

| Phase | Description | Tasks | Status |
|-------|-------------|-------|--------|
| 1 | Project Setup | [N] | ⬜ |
| 2 | Database & Data Layer | [N] | ⬜ |
| 3 | Authentication & Authorization | [N] | ⬜ |
| 4 | API Development | [N] | ⬜ |
| 5 | Core Features (P0) | [N] | ⬜ |
| 6 | Extended Features (P1) | [N] | ⬜ |
| 7 | Testing | [N] | ⬜ |
| 8 | DevOps & Deployment | [N] | ⬜ |
| 9 | Polish & Optimization (P2) | [N] | ⬜ |
| **Total** | | **[N]** | |

---

## Phase 1: Project Setup

Tasks to initialize the project with the technology stack defined in TRD.

### Environment Setup
- [ ] Initialize project with [framework] (TRD 2.1)
- [ ] Configure TypeScript with strict mode (TRD 2.5)
- [ ] Set up ESLint and Prettier configuration (TRD 2.5)
- [ ] Configure path aliases for imports (TRD 2.5)

### Dependencies
- [ ] Install and configure [database ORM] (TRD 2.2)
- [ ] Install and configure [auth library] (TRD 5.1)
- [ ] Install UI component dependencies (TRD 2.1)
- [ ] Install testing dependencies (TRD 11.1)

### Configuration
- [ ] Create environment variable schema (.env.example)
- [ ] Set up configuration module for environment-based settings
- [ ] Configure logging based on TRD 12.1 strategy

---

## Phase 2: Database & Data Layer

Tasks to implement the database schema defined in TRD Section 3.

### Database Setup
- [ ] Set up [database] connection and configuration (TRD 2.3)
- [ ] Create database migration infrastructure (TRD 3.4)

### Models
- [ ] Create [Model1] model with fields: [fields] (TRD 3.2)
- [ ] Create [Model2] model with fields: [fields] (TRD 3.2)
- [ ] Create [Model3] model with fields: [fields] (TRD 3.2)

### Relationships
- [ ] Implement [Model1] -> [Model2] relationship (TRD 3.1)
- [ ] Add foreign key constraints and cascades (TRD 3.1)

### Indexes
- [ ] Create indexes per TRD 3.3 indexing strategy
- [ ] Add unique constraints where specified (TRD 3.2)

### Seeding
- [ ] Create database seed script for development data
- [ ] Create seed script for test fixtures

---

## Phase 3: Authentication & Authorization

Tasks to implement auth per TRD Section 5.

### Authentication
- [ ] Implement [auth strategy] authentication (TRD 5.1)
- [ ] Create login endpoint POST /api/auth/login (TRD 4.2)
- [ ] Create registration endpoint POST /api/auth/register (TRD 4.2)
- [ ] Create logout endpoint POST /api/auth/logout (TRD 4.2)
- [ ] Implement token refresh mechanism (TRD 5.1)

### Authorization
- [ ] Implement role-based access control per TRD 5.2
- [ ] Create authorization middleware
- [ ] Add permission checks to protected routes

### Security
- [ ] Implement password hashing with [algorithm] (TRD 5.3)
- [ ] Add rate limiting to auth endpoints (TRD 4.4)
- [ ] Implement account lockout after failed attempts (TRD 5.3)

---

## Phase 4: API Development

Tasks to implement API endpoints per TRD Section 4.

### Core Endpoints
- [ ] Implement GET /api/[resource] - List (TRD 4.2)
- [ ] Implement POST /api/[resource] - Create (TRD 4.2)
- [ ] Implement GET /api/[resource]/:id - Read (TRD 4.2)
- [ ] Implement PATCH /api/[resource]/:id - Update (TRD 4.2)
- [ ] Implement DELETE /api/[resource]/:id - Delete (TRD 4.2)

### Request Handling
- [ ] Implement request validation with [validation library]
- [ ] Create standard error response format (TRD 4.3)
- [ ] Create standard success response format (TRD 4.3)

### Middleware
- [ ] Create authentication middleware
- [ ] Create request logging middleware (TRD 12.1)
- [ ] Create error handling middleware (TRD 13.1)

---

## Phase 5: Core Features (P0)

Tasks to implement P0 priority features from PRD Section 5.

### [Feature 1 Name] (PRD FR-001)
- [ ] [Specific implementation task 1]
- [ ] [Specific implementation task 2]
- [ ] [Specific implementation task 3]

### [Feature 2 Name] (PRD FR-002)
- [ ] [Specific implementation task 1]
- [ ] [Specific implementation task 2]

[Continue for all P0 features...]

---

## Phase 6: Extended Features (P1)

Tasks to implement P1 priority features from PRD Section 5.

### [Feature Name] (PRD FR-XXX)
- [ ] [Specific implementation task]

[Continue for all P1 features...]

---

## Phase 7: Testing

Tasks to implement testing strategy per TRD Section 11.

### Unit Tests
- [ ] Write unit tests for [Service1] (target: [X]% coverage)
- [ ] Write unit tests for [Service2] (target: [X]% coverage)
- [ ] Write unit tests for utility functions

### Integration Tests
- [ ] Write integration tests for authentication flow
- [ ] Write integration tests for [Resource] CRUD operations
- [ ] Set up test database and fixtures

### E2E Tests
- [ ] Configure [E2E framework] (TRD 11.1)
- [ ] Write E2E tests for critical user flows (PRD 4.2)
- [ ] Write E2E tests for [User Journey 1]

---

## Phase 8: DevOps & Deployment

Tasks to implement infrastructure per TRD Sections 8-9.

### CI/CD
- [ ] Create CI pipeline configuration (TRD 8.2)
- [ ] Add linting step to CI
- [ ] Add test step to CI
- [ ] Add build step to CI
- [ ] Configure deployment to staging (TRD 8.1)
- [ ] Configure deployment to production (TRD 8.1)

### Infrastructure
- [ ] Set up [hosting provider] project (TRD 2.4)
- [ ] Configure environment variables for each environment
- [ ] Set up database for staging/production

### Monitoring
- [ ] Configure error tracking with [tool] (TRD 12.4)
- [ ] Set up logging infrastructure (TRD 12.1)
- [ ] Configure alerting rules (TRD 12.3)

---

## Phase 9: Polish & Optimization (P2)

Tasks for P2 features and optimization per PRD and TRD Section 6.

### P2 Features
- [ ] [P2 Feature implementation tasks...]

### Performance Optimization
- [ ] Implement caching strategy per TRD 6.3
- [ ] Optimize database queries per TRD 6.4
- [ ] Implement lazy loading where applicable

### Security Hardening
- [ ] Complete security checklist (TRD 14.1)
- [ ] Configure security headers (TRD 14.1)
- [ ] Run dependency vulnerability scan

### Documentation
- [ ] Update API documentation
- [ ] Create deployment documentation
- [ ] Update README with setup instructions

---

## Completion Checklist

Before marking the project complete, verify:

- [ ] All P0 features implemented and tested (PRD 5.1)
- [ ] All P1 features implemented and tested (PRD 5.1)
- [ ] All API endpoints functional (TRD 4.2)
- [ ] Authentication working as specified (TRD 5)
- [ ] Test coverage meets targets (TRD 11)
- [ ] CI/CD pipeline operational (TRD 8.2)
- [ ] Monitoring and alerting configured (TRD 12)
- [ ] Security checklist complete (TRD 14.1)
- [ ] Performance requirements met (TRD 6.1)

---

## Notes

- Tasks reference PRD/TRD sections in parentheses for traceability
- Mark tasks with [x] when complete
- Update phase status (⬜ → ✅) when all tasks in phase are done
- If blocked, add a note under the task explaining the blocker
```

## Phase Structure

The standard phase structure is:

| Phase | Focus | Source |
|-------|-------|--------|
| 1. Project Setup | Initialize project, install dependencies | TRD Sections 2, 10 |
| 2. Database & Data Layer | Schema, models, migrations | TRD Section 3 |
| 3. Authentication & Authorization | Auth system, permissions | TRD Section 5 |
| 4. API Development | Endpoints, middleware | TRD Section 4 |
| 5. Core Features (P0) | Must-have functionality | PRD P0 features |
| 6. Extended Features (P1) | Important functionality | PRD P1 features |
| 7. Testing | Unit, integration, E2E | TRD Section 11 |
| 8. DevOps & Deployment | CI/CD, infrastructure | TRD Sections 8, 9, 12 |
| 9. Polish & Optimization | P2 features, performance | PRD P2, TRD Section 6 |

**Phase Customization:**
- Phases can be merged if project is small
- Phases can be split if project is large
- Phase order should respect dependencies
- Additional phases can be added for complex projects

## Task Categories by Phase

### Phase 1: Project Setup
- Environment initialization
- Dependency installation
- Configuration files
- Development tooling
- Project structure

### Phase 2: Database & Data Layer
- Database connection
- Schema migrations
- Model definitions
- Relationships
- Indexes and constraints
- Seed data

### Phase 3: Authentication & Authorization
- Auth provider setup
- Login/register/logout
- Token management
- Role definitions
- Permission middleware
- Security measures

### Phase 4: API Development
- Route definitions
- Controllers/handlers
- Request validation
- Response formatting
- Error handling
- Middleware

### Phase 5-6: Feature Implementation
- UI components
- Business logic
- Data operations
- User interactions
- Feature-specific APIs

### Phase 7: Testing
- Test setup
- Unit tests
- Integration tests
- E2E tests
- Test fixtures
- Coverage reporting

### Phase 8: DevOps & Deployment
- CI pipeline
- CD pipeline
- Environment config
- Infrastructure setup
- Monitoring setup
- Alerting rules

### Phase 9: Polish & Optimization
- Performance tuning
- Security hardening
- P2 features
- Documentation
- Code cleanup

## Traceability Format

Each task should reference its source:

```
- [ ] Task description (PRD X.X) - references PRD section
- [ ] Task description (TRD X.X) - references TRD section
- [ ] Task description (PRD FR-XXX) - references specific requirement
- [ ] Task description (PRD US-XXX) - references user story
```

## Dependency Handling

Tasks within a phase should be ordered by dependency:

```
Good ordering (dependencies first):
- [ ] Create User model (no dependencies)
- [ ] Create Post model with user_id foreign key (depends on User)
- [ ] Add User -> Posts relationship (depends on both models)

Bad ordering (dependency violation):
- [ ] Add User -> Posts relationship (Post doesn't exist yet!)
- [ ] Create User model
- [ ] Create Post model
```

## Task Estimation Guidelines

While the skill doesn't provide time estimates, tasks should be sized appropriately:

| Task Size | Characteristics | Examples |
|-----------|-----------------|----------|
| Small | Single file change, straightforward | Add field to model, write one test |
| Medium | Multiple files, some complexity | Implement endpoint, create component |
| Large | Should be broken down | Full feature, major refactor |

**If a task feels "large", break it into smaller tasks.**

## Error Handling

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

## Integration with Autonomous Development

The generated task document is designed to work with the `/autonomous-development` skill:

1. **Format Compatibility**: Uses the same checkbox format
2. **Phase Structure**: Phases can be executed sequentially
3. **Status Tracking**: Summary table tracks completion
4. **Traceability**: References enable context lookup

**Workflow:**
```
/prd <idea> → /trd → /to-do → /autonomous-development
```

## Output

- **File**: `dev-docs/to-do.md`
- **Format**: Markdown with checkbox tasks
- **Traceability**: References to PRD/TRD sections
- **Compatibility**: Works with /autonomous-development skill

## Example Session

```
User: /to-do
Assistant: I will read the PRD and TRD to generate a development task breakdown.

[Reads dev-docs/prd.md - water intake tracking app with 12 user stories]
[Reads dev-docs/trd.md - React Native + Node.js + PostgreSQL architecture]

Based on the documents, I will create a structured task list organized by phases.

[Writes dev-docs/to-do.md with 9 phases and 87 tasks]
Assistant: I have created the task breakdown at dev-docs/to-do.md. Summary:

Phase 1: Project Setup - 12 tasks
Phase 2: Database and Data Layer - 9 tasks
Phase 3: Authentication - 8 tasks
Phase 4: API Development - 15 tasks
Phase 5: Core Features (P0) - 18 tasks
Phase 6: Extended Features (P1) - 10 tasks
Phase 7: Testing - 8 tasks
Phase 8: DevOps and Deployment - 5 tasks
Phase 9: Polish and Optimization - 2 tasks

Total: 87 tasks

All tasks trace back to PRD features or TRD specifications. No new features were introduced.
You can now run /autonomous-development to begin executing tasks.
```

## Success Criteria

A successful task breakdown generation:
- Reads and analyzes both PRD and TRD
- Creates tasks at dev-docs/to-do.md
- Organizes tasks into logical phases
- Every PRD feature has corresponding tasks
- Every TRD component has corresponding tasks
- No tasks introduce features not in PRD
- No tasks contradict TRD decisions
- Task order respects dependencies
- Tasks are specific and actionable
- All tasks have PRD/TRD traceability references
- Summary table accurately counts tasks per phase
- Format is compatible with /autonomous-development skill

## Validation Checklist

Before finalizing the task document, verify:

### PRD Coverage
- [ ] All P0 features have implementation tasks
- [ ] All P1 features have implementation tasks
- [ ] All P2 features have implementation tasks (in Phase 9)
- [ ] All user stories are addressed
- [ ] All functional requirements are covered
- [ ] Non-functional requirements have corresponding tasks

### TRD Coverage
- [ ] Technology stack setup tasks exist
- [ ] All database models have creation tasks
- [ ] All API endpoints have implementation tasks
- [ ] Authentication approach is implemented
- [ ] Authorization model is implemented
- [ ] Testing strategy is reflected
- [ ] CI/CD pipeline is set up
- [ ] Monitoring is configured

### Task Quality
- [ ] Each task starts with action verb
- [ ] Each task is specific (not vague)
- [ ] Each task is independently completable
- [ ] Large tasks are broken down
- [ ] Dependencies are ordered correctly
- [ ] Traceability references are accurate

### No Scope Creep
- [ ] No features beyond PRD scope
- [ ] No technologies beyond TRD decisions
- [ ] No "nice to have" additions
- [ ] Deferred items remain deferred

## Notes

- The skill requires both PRD and TRD to exist
- Tasks are designed for the /autonomous-development workflow
- Phase count can vary based on project complexity
- Task granularity targets 1-4 hours of work per task
- Traceability enables context lookup during implementation
- Summary table enables progress tracking
