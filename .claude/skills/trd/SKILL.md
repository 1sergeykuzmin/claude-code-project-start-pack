---
name: trd
description: Generate a Technical Requirements Document (TRD) from the existing PRD. Use when asked to create a TRD, document technical specifications, or plan implementation architecture. Invoked as "/trd". Supports --team flag for multi-perspective generation using architect + reviewer agents with optional domain specialists.
metadata:
  author: custom
  version: "2.0.0"
  argument-hint: [--team]
---

# Technical Requirements Document Generator

Generate comprehensive Technical Requirements Documents based on the Product Requirements Document (PRD). This skill analyzes the PRD, considers platform-specific best practices, and produces a detailed technical specification.

Supports two modes:
- **Solo mode** (default): Single-agent TRD generation with adaptive questioning
- **Team mode** (`--team`): Draft + Review model using a Lead Architect who writes the full TRD, reviewed by 1-2 role-specific Reviewers, plus optional domain specialists (Security Reviewer, Database Architect, Performance Engineer)

## Input Format

```
/trd                # Solo mode (default)
/trd --team         # Team mode (draft + review)
```

No other arguments required. The skill reads context from `dev-docs/prd.md`.

## Mode Selection

### Detecting Mode

1. If the input contains `--team`, use **Team Mode**
2. Otherwise, use **Solo Mode**

### When to Suggest Team Mode

If solo mode is invoked but the idea meets ANY of these criteria, **suggest** (don't force) team mode:
- Complex system with multiple integration points
- Microservices or distributed architecture likely needed
- Security-critical or compliance-heavy product
- Multi-platform product (web + mobile + API)
- PRD has 10+ functional requirements

Suggestion format:
```
This project could benefit from multi-perspective technical review.
Would you like to use team mode (/trd --team) for a more
comprehensive TRD with architectural review from specialized roles?
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

---

# SOLO MODE

The default TRD generation process using a single agent.

## Overview

When invoked with `/trd`, this skill:
1. Reads and analyzes the PRD from `dev-docs/prd.md`
2. Extracts technical implications from product requirements
3. Identifies gaps in technical context
4. Asks up to 10 targeted follow-up questions
5. Generates a comprehensive TRD at `dev-docs/trd.md`

## Prerequisites

Before running, ensure:
- PRD exists at `dev-docs/prd.md`
- PRD contains sufficient product context (problem, users, features, requirements)

If the PRD is missing or incomplete, the skill will prompt for the missing information.

## The Process

### Step 1: Read and Analyze PRD

Read `dev-docs/prd.md` and extract:

```
1. Product Overview
   - What is being built?
   - Who are the users?
   - What problem does it solve?

2. Functional Requirements
   - Core features and capabilities
   - User stories and use cases
   - Priority levels (P0/P1/P2)

3. Non-Functional Requirements
   - Performance expectations
   - Security requirements
   - Scalability needs
   - Accessibility requirements

4. Technical Context (if present)
   - Platform preferences
   - Integration requirements
   - Technology constraints

5. Scope Boundaries
   - What's in v1 scope
   - What's deferred to future versions
```

### Step 2: Identify Technical Gaps

Map PRD content against TRD requirements to identify missing technical details:

| PRD Section | TRD Implication | Gap Assessment |
|-------------|-----------------|----------------|
| Target Users | Client platform decisions | Mobile/Web/Desktop? |
| Features | API design, data models | Entity relationships? |
| Integrations | External API contracts | Authentication methods? |
| Scale expectations | Infrastructure sizing | Expected load? |
| Security requirements | Auth architecture | Compliance needs? |

### Step 3: Ask Follow-up Questions

Use the AskUserQuestion tool to gather missing technical information. Ask **up to 10 questions** to complete the picture.

**Question Categories (prioritized):**

| Priority | Category | Purpose |
|----------|----------|---------|
| 1 | Platform & Stack | What technologies to use? |
| 2 | Architecture Style | Monolith vs microservices? Serverless? |
| 3 | Data Architecture | Database type? Data relationships? |
| 4 | Authentication & Security | Auth provider? Compliance requirements? |
| 5 | Infrastructure | Cloud provider? Hosting model? |
| 6 | Integrations | Third-party services? API contracts? |
| 7 | Performance | Response time SLAs? Caching strategy? |
| 8 | Development Workflow | Git strategy? CI/CD preferences? |
| 9 | Monitoring & Operations | Observability tools? Alerting needs? |
| 10 | Constraints | Budget? Team expertise? Timeline? |

**Example Question Patterns:**

```
Platform & Stack:
- "What is your preferred technology stack? (React/Next.js, Vue/Nuxt, etc.)"
- "Which database type fits your needs? (PostgreSQL, MongoDB, etc.)"

Architecture Style:
- "Should this be a monolithic application or microservices?"
- "Are you considering serverless architecture (Vercel, AWS Lambda)?"

Data Architecture:
- "What are the main data entities and their relationships?"
- "Do you need real-time data sync or eventual consistency is OK?"

Authentication & Security:
- "How should users authenticate? (Email/password, OAuth, SSO)"
- "Are there compliance requirements? (GDPR, HIPAA, SOC2)"

Infrastructure:
- "What's your preferred cloud provider? (AWS, GCP, Vercel, etc.)"
- "Do you need multi-region deployment?"

Integrations:
- "Which third-party services must be integrated?"
- "Do you need webhook support for external systems?"

Performance:
- "What are acceptable response times for key operations?"
- "How many concurrent users should the system support?"

Development Workflow:
- "What Git branching strategy do you prefer? (GitFlow, trunk-based)"
- "Do you have existing CI/CD infrastructure?"
```

### Step 4: Apply Platform-Specific Best Practices

Based on the identified platform, apply relevant best practices:

**Web Application (Next.js/React):**
- Reference `.claude/skills/vercel-react-best-practices/` for optimization patterns
- Server Components vs Client Components decisions
- Bundle optimization strategies
- Image and font optimization
- API route design patterns

**Mobile Application (React Native/Flutter):**
- Offline-first architecture considerations
- Push notification infrastructure
- Deep linking strategy
- App store deployment requirements
- Platform-specific UI/UX patterns

**Backend API (Node.js/Python/Go):**
- RESTful vs GraphQL design
- Rate limiting and throttling
- Caching layers (Redis, CDN)
- Background job processing
- Database connection pooling

**Serverless:**
- Cold start optimization
- Function composition patterns
- State management strategies
- Cost optimization patterns

### Step 5: Generate the TRD

After gathering information, create a comprehensive TRD at `dev-docs/trd.md` with the following structure:

```markdown
# Technical Requirements Document: [Product Name]

> Generated: [Date]
> Status: Draft
> Version: 1.0
> Based on PRD: v[PRD Version]

## Executive Summary

[2-3 sentence technical overview: architecture style, key technologies, deployment model]

---

## 1. System Architecture

### 1.1 Architecture Overview
[High-level description of the system architecture]

### 1.2 Architecture Diagram
```
[ASCII or description of component diagram]
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API/BFF   │────▶│  Database   │
│  (Web/App)  │     │   Server    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  External   │
                    │  Services   │
                    └─────────────┘
```

### 1.3 Component Breakdown

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| [Component 1] | [What it does] | [Tech stack] |

### 1.4 Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice made] | [Why] |

---

## 2. Technology Stack

### 2.1 Frontend
- **Framework**: [e.g., Next.js 14+ with App Router]
- **Language**: [e.g., TypeScript 5.x]
- **Styling**: [e.g., Tailwind CSS]
- **State Management**: [e.g., Zustand, React Context]
- **Form Handling**: [e.g., React Hook Form + Zod]
- **Animation**: [e.g., Framer Motion]

### 2.2 Backend
- **Runtime**: [e.g., Node.js 20 LTS]
- **Framework**: [e.g., Next.js API Routes / Express / Fastify]
- **Language**: [e.g., TypeScript]
- **ORM/Query Builder**: [e.g., Prisma / Drizzle]

### 2.3 Database
- **Primary Database**: [e.g., PostgreSQL 15]
- **Caching Layer**: [e.g., Redis / Upstash]
- **Search**: [e.g., Elasticsearch / Algolia] (if needed)

### 2.4 Infrastructure
- **Hosting**: [e.g., Vercel / AWS / GCP]
- **CDN**: [e.g., Vercel Edge / CloudFlare]
- **File Storage**: [e.g., S3 / Cloudflare R2]
- **Email Service**: [e.g., Resend / SendGrid]

### 2.5 Development Tools
- **Package Manager**: [e.g., pnpm]
- **Linting**: [e.g., ESLint + Prettier]
- **Testing**: [e.g., Vitest + Playwright]
- **CI/CD**: [e.g., GitHub Actions]

---

## 3. Database Design

### 3.1 Entity Relationship Diagram
```
[ERD in ASCII or description]
┌──────────────┐       ┌──────────────┐
│    User      │       │    Entity    │
├──────────────┤       ├──────────────┤
│ id (PK)      │──────▶│ id (PK)      │
│ email        │       │ user_id (FK) │
│ created_at   │       │ data         │
└──────────────┘       └──────────────┘
```

### 3.2 Data Models

#### User
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |

[Additional models...]

### 3.3 Indexing Strategy
- [Index 1]: [Purpose and columns]
- [Index 2]: [Purpose and columns]

### 3.4 Data Migration Strategy
[Approach for schema changes and data migrations]

---

## 4. API Design

### 4.1 API Style
[REST / GraphQL / tRPC - with rationale]

### 4.2 API Endpoints

#### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/login | User login | Public |
| POST | /api/auth/register | User registration | Public |
| POST | /api/auth/logout | User logout | Required |

#### [Resource Name]
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/[resource] | List resources | Required |
| POST | /api/[resource] | Create resource | Required |
| GET | /api/[resource]/:id | Get resource | Required |
| PATCH | /api/[resource]/:id | Update resource | Required |
| DELETE | /api/[resource]/:id | Delete resource | Required |

### 4.3 Request/Response Formats

#### Standard Success Response
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

#### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }
  }
}
```

### 4.4 Rate Limiting
[Rate limiting strategy and limits per endpoint type]

---

## 5. Authentication & Authorization

### 5.1 Authentication Strategy
[JWT / Session-based / OAuth - with implementation details]

### 5.2 Authorization Model
[RBAC / ABAC / Simple roles - with permission matrix]

| Role | Permissions |
|------|-------------|
| Admin | Full access |
| User | Read/Write own data |
| Guest | Read-only public data |

### 5.3 Security Measures
- [ ] Password hashing (bcrypt/argon2)
- [ ] JWT token rotation
- [ ] CSRF protection
- [ ] XSS prevention
- [ ] SQL injection prevention
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts

### 5.4 Compliance Requirements
[GDPR, HIPAA, SOC2 requirements if applicable]

---

## 6. Performance Requirements

### 6.1 Response Time SLAs

| Operation Type | Target | Maximum |
|---------------|--------|---------|
| Page Load (initial) | < 1.5s | < 3s |
| API Response | < 200ms | < 500ms |
| Search | < 300ms | < 1s |
| File Upload | < 2s | < 5s |

### 6.2 Throughput Requirements
- Concurrent users: [Expected number]
- Requests per second: [Target RPS]
- Peak load handling: [Strategy]

### 6.3 Caching Strategy

| Cache Layer | Technology | TTL | Use Case |
|-------------|------------|-----|----------|
| Browser | HTTP headers | 1h | Static assets |
| CDN | Vercel Edge | 5m | API responses |
| Application | Redis | 15m | Session data |
| Database | Query cache | 1m | Frequent queries |

### 6.4 Optimization Patterns
[Reference to vercel-react-best-practices if applicable]

---

## 7. Scalability Strategy

### 7.1 Scaling Model
[Horizontal / Vertical / Serverless auto-scaling]

### 7.2 Bottleneck Mitigation

| Potential Bottleneck | Mitigation Strategy |
|---------------------|---------------------|
| Database connections | Connection pooling |
| API throughput | Horizontal scaling, caching |
| File storage | CDN, object storage |
| Background jobs | Queue-based processing |

### 7.3 Growth Projections

| Metric | Current | 6 months | 12 months |
|--------|---------|----------|-----------|
| Users | [N] | [N*X] | [N*Y] |
| Data volume | [GB] | [GB] | [GB] |
| API calls/day | [N] | [N] | [N] |

---

## 8. Infrastructure & DevOps

### 8.1 Environment Strategy

| Environment | Purpose | URL Pattern |
|-------------|---------|-------------|
| Development | Local development | localhost:3000 |
| Preview | PR previews | pr-*.preview.domain.com |
| Staging | Pre-production testing | staging.domain.com |
| Production | Live environment | domain.com |

### 8.2 CI/CD Pipeline

```
[Commit] → [Lint/Type Check] → [Test] → [Build] → [Deploy Preview]
                                                         │
                                              [Merge to main]
                                                         │
                                              [Deploy Staging]
                                                         │
                                              [Manual Approval]
                                                         │
                                              [Deploy Production]
```

### 8.3 Infrastructure as Code
[Terraform / Pulumi / CDK approach if applicable]

### 8.4 Secrets Management
[Environment variables, vault, etc.]

---

## 9. Integration Architecture

### 9.1 Third-Party Services

| Service | Purpose | Integration Method |
|---------|---------|-------------------|
| [Service 1] | [Purpose] | REST API / SDK |
| [Service 2] | [Purpose] | Webhook |

### 9.2 Webhook Design
[Incoming/outgoing webhook patterns]

### 9.3 API Contracts
[OpenAPI/Swagger specs location]

---

## 10. Development Standards

### 10.1 Code Style
- ESLint configuration
- Prettier configuration
- TypeScript strict mode

### 10.2 Git Workflow
- Branch naming: `feature/`, `fix/`, `chore/`
- Commit format: Conventional Commits
- PR requirements: Tests pass, review approval

### 10.3 Code Review Guidelines
- [ ] Type safety verified
- [ ] Tests included
- [ ] No console.logs
- [ ] Error handling complete
- [ ] Performance considered

### 10.4 Documentation Requirements
- README for each package/module
- JSDoc for public APIs
- Architecture Decision Records (ADRs)

---

## 11. Testing Strategy

### 11.1 Testing Pyramid

| Level | Coverage Target | Tools |
|-------|----------------|-------|
| Unit Tests | 80% | Vitest |
| Integration Tests | Key flows | Vitest + MSW |
| E2E Tests | Critical paths | Playwright |

### 11.2 Test Requirements by Priority

| Priority | Test Requirement |
|----------|-----------------|
| P0 Features | Unit + Integration + E2E |
| P1 Features | Unit + Integration |
| P2 Features | Unit |

### 11.3 Testing Standards
- Tests must pass before merge
- No skipped tests in main branch
- Mocking strategy for external services

---

## 12. Monitoring & Observability

### 12.1 Logging Strategy

| Log Level | Use Case | Retention |
|-----------|----------|-----------|
| ERROR | Exceptions, failures | 90 days |
| WARN | Degraded operations | 30 days |
| INFO | Business events | 14 days |
| DEBUG | Development only | 1 day |

### 12.2 Metrics & KPIs

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Error rate | < 0.1% | > 1% |
| P99 latency | < 500ms | > 1000ms |
| Uptime | 99.9% | < 99.5% |

### 12.3 Alerting Rules
[PagerDuty / Slack / Email escalation]

### 12.4 Observability Stack
- **Logging**: [e.g., Vercel Logs / Datadog]
- **Metrics**: [e.g., Vercel Analytics / Prometheus]
- **Tracing**: [e.g., OpenTelemetry]
- **Error Tracking**: [e.g., Sentry]

---

## 13. Error Handling & Recovery

### 13.1 Error Categories

| Category | Handling Strategy | User Message |
|----------|------------------|--------------|
| Validation | Return 400 | Specific field errors |
| Authentication | Return 401 | "Please log in" |
| Authorization | Return 403 | "Access denied" |
| Not Found | Return 404 | "Resource not found" |
| Server Error | Return 500, log, alert | "Something went wrong" |

### 13.2 Retry Strategy
- Exponential backoff for external services
- Circuit breaker pattern for dependencies
- Dead letter queue for failed jobs

### 13.3 Graceful Degradation
[Fallback strategies when dependencies fail]

---

## 14. Security Considerations

### 14.1 Security Checklist
- [ ] HTTPS enforced
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Input validation on all endpoints
- [ ] Output encoding for XSS prevention
- [ ] SQL parameterization
- [ ] File upload validation
- [ ] Dependency vulnerability scanning
- [ ] Secrets not in code

### 14.2 Data Protection
- Encryption at rest: [Strategy]
- Encryption in transit: TLS 1.3
- PII handling: [Strategy]
- Data retention: [Policy]

### 14.3 Security Audit Schedule
[Penetration testing, dependency audits]

---

## 15. Technical Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Strategy] |

---

## 16. Implementation Phases

### Phase 1: Foundation
- [ ] Project setup and configuration
- [ ] Database schema and migrations
- [ ] Authentication system
- [ ] Basic API structure

### Phase 2: Core Features
- [ ] [P0 Feature 1]
- [ ] [P0 Feature 2]
- [ ] [P0 Feature 3]

### Phase 3: Extended Features
- [ ] [P1 Feature 1]
- [ ] [P1 Feature 2]

### Phase 4: Polish & Optimization
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Monitoring setup

---

## Appendix

### A. Glossary
[Technical terms and definitions]

### B. References
- PRD: `dev-docs/prd.md`
- Best Practices: `.claude/skills/vercel-react-best-practices/`
- Design Guidelines: `.claude/skills/web-design-guidelines/`

### C. ADR Log
[Architecture Decision Records]

### D. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

### Step 6: Review and Validate

After generating the TRD:

1. **PRD Alignment Check**: Verify all PRD requirements have technical coverage
2. **Completeness Check**: Ensure all sections have meaningful content
3. **Consistency Check**: Verify technology choices are compatible
4. **Best Practices Check**: Apply platform-specific optimizations
5. **Gap Identification**: Note any remaining technical decisions

## Question Strategy

### Adaptive Questioning

Adjust questions based on PRD completeness:

**PRD Missing Technical Context:**
- Ask 8-10 questions covering all technical areas
- Start with platform/stack decisions

**PRD Has Partial Technical Info:**
- Ask 4-6 questions focusing on gaps
- Skip areas already specified in PRD

**PRD Has Detailed Technical Section:**
- Ask 2-3 clarifying questions
- Focus on implementation specifics

### Question Batching

Use the AskUserQuestion tool efficiently:
- Group related questions (max 4 per call)
- Provide multiple-choice for common patterns
- Use "Other" for custom specifications

### PRD-Driven Questions

Always derive questions from PRD content:
- If PRD mentions "mobile app" → Ask about iOS/Android/both
- If PRD mentions "user accounts" → Ask about auth providers
- If PRD mentions "file uploads" → Ask about storage requirements
- If PRD mentions "real-time" → Ask about WebSocket vs polling

## Best Practices Applied

This skill follows industry-standard TRD best practices:

1. **PRD-Aligned**: Every technical decision traces back to a product requirement
2. **Opinionated Defaults**: Provide sensible defaults based on platform
3. **Scalability-First**: Design for growth from the start
4. **Security-Integrated**: Security is built-in, not bolted-on
5. **Testable**: Architecture supports comprehensive testing
6. **Observable**: Built-in monitoring and debugging capabilities
7. **Documented**: Clear decisions with rationale
8. **Phased**: Implementation broken into manageable phases

## Platform-Specific References

When generating TRD for specific platforms, reference:

| Platform | Reference |
|----------|-----------|
| Next.js/React | `.claude/skills/vercel-react-best-practices/` |
| Web UI | `.claude/skills/web-design-guidelines/` |

## Output

- **File**: `dev-docs/trd.md`
- **Format**: Markdown with clear section hierarchy
- **Traceability**: Links back to PRD sections

## Error Handling

### PRD Not Found
```
If dev-docs/prd.md does not exist:
  1. Inform user that PRD is required
  2. Suggest running /prd first
  3. Offer to create a basic PRD if user provides product description
```

### PRD Incomplete
```
If PRD is missing critical sections:
  1. List the missing sections
  2. Ask user to provide the missing information
  3. Alternatively, ask follow-up questions to fill gaps
```

## Example Session

```
User: /trd
Assistant: I will read the PRD and generate a Technical Requirements Document.

[Reads dev-docs/prd.md - analyzes water intake tracking mobile app PRD]

Based on the PRD, I need to ask a few technical questions to complete the TRD.

[Uses AskUserQuestion tool with questions about:]
- Technology stack preference (React Native vs Flutter vs Native)
- Backend preference (Node.js/Express, Python/FastAPI, serverless)
- Database choice (PostgreSQL, MongoDB, SQLite for mobile)
- Authentication method (Firebase Auth, Auth0, custom JWT)

User: [Answers questions - chooses React Native, Node.js API, PostgreSQL, Firebase Auth]
Assistant: Based on your answers, I will now generate a comprehensive TRD.

[Writes dev-docs/trd.md with all sections based on PRD and technical decisions]
Assistant: I have created the TRD at dev-docs/trd.md. The document includes:
- System architecture with React Native mobile app and Node.js API
- PostgreSQL database schema with User, WaterLog, and Reminder tables
- RESTful API design with 15 endpoints
- Firebase Authentication integration
- Push notification architecture
- Performance requirements and caching strategy
- CI/CD pipeline for mobile app deployment
- Testing strategy with unit, integration, and E2E tests
```

---

# TEAM MODE

Draft + Review TRD generation using agent teams. Spawns 1 Lead Architect who writes the full TRD draft, reviewed by 1-2 role-specific Reviewers, plus optional domain specialists who provide focused reviews. The Lead Architect revises based on all feedback.

**How this differs from PRD team mode:**
- 1 writer + reviewers (not 3 parallel researchers producing independent findings)
- 1 review cycle (not research + debate rounds)
- No synthesis from scratch — the Lead Architect revises the existing draft
- Smaller specialist pool: 3 specialists (vs PRD's 7)

## Team Process Overview

```
Lead: Read PRD + ask 2-3 questions
  ↓
Lead: Detect project type & specialist need
  ↓
Lead: Spawn 1 Lead Architect + 1-2 Reviewers + 0-2 Specialists
  ↓
Lead Architect: Writes FULL TRD draft → .trd-workspace/trd-draft.md
  ↓
Reviewers + Specialists: Review draft → .trd-workspace/{role}-review.md
  ↓
Lead: Reads reviews + revises draft → .trd-workspace/trd-final.md
  ↓
Lead: Quality gates + write dev-docs/trd.md + cleanup
```

## Team Step 1: Lead Intake

The lead asks **2-3 scoping questions only**. The PRD provides most context already, so keep intake brief.

Focus on:
- Architecture preferences (monolith vs microservices, serverless vs traditional)
- Technology constraints or preferences not in the PRD
- Infrastructure constraints (cloud provider, budget limits)

Use AskUserQuestion tool. Batch into 1 tool call (2-3 questions max).

**Do NOT ask detailed questions about features or product requirements** — those are in the PRD. Focus only on technical preferences not already specified.

## Team Step 1.5: Specialist Detection

After scoping questions are answered, run the **Detection Logic** from the Conditional Specialists section:

1. Scan PRD content + user answers for trigger keywords
2. Apply contextual inference if signal is weak
3. If a specialist is recommended, ask the user via AskUserQuestion
4. If user declines or no match found, proceed with core team only

Record the result: `specialist = {name}` or `specialist = none`

## Team Step 1.9: Create Workspace

Create a temporary workspace directory for intermediate artifacts:

```bash
mkdir -p .trd-workspace
```

This directory stores the TRD draft, reviews, and final revision as persistent files, ensuring they survive context compaction and message delivery issues. The workspace is cleaned up in Team Step 8.

**File naming convention:**
- Draft: `.trd-workspace/trd-draft.md`
- Reviews: `.trd-workspace/{role}-review.md` (e.g., `backend-review.md`, `frontend-review.md`, `infra-review.md`)
- Specialist reviews: `.trd-workspace/{specialist}-review.md` (e.g., `security-review.md`, `database-review.md`, `performance-review.md`)
- Final revision: `.trd-workspace/trd-final.md`

Also add `.trd-workspace/` to `.gitignore` if not already present.

**Why files instead of messages:** SendMessage content is ephemeral — if the lead's context compacts or messages are consumed before rendering, the data is lost. Files persist on disk and can be re-read at any time.

## Team Step 2: Detect Project Type & Assign Roles

Analyze the PRD to determine the project type and assign roles accordingly.

### Project Type Detection

Scan the PRD for signals:

| Signal | Project Type |
|--------|-------------|
| Frontend framework + backend API + database | Full-stack web app |
| SPA, heavy UI, client-side state, design system | Frontend-heavy (SPA) |
| API endpoints, microservices, no UI or minimal UI | Backend/API-only |
| CI/CD, deployment, monitoring, cloud infrastructure | Infra-heavy |
| Mixed signals or unclear | Default (full-stack) |

### Role Assignment

| Project Type | Lead Architect | Reviewer 1 | Reviewer 2 |
|---|---|---|---|
| Full-stack web app | Backend Architect | Frontend Architect | Infra/DevOps Engineer |
| Frontend-heavy (SPA) | Frontend Architect | Backend Architect | (optional) |
| Backend/API-only | Backend Architect | Infra/DevOps Engineer | (optional) |
| Infra-heavy | Infra/DevOps Engineer | Backend Architect | (optional) |
| Default | Backend Architect | Frontend Architect | Infra/DevOps Engineer |

**Core roles:**

| Role | Expertise |
|------|-----------|
| Backend Architect | API design, database schema, caching, authentication, server-side logic, data flows |
| Frontend Architect | Component architecture, state management, rendering strategy, client-side performance, UX patterns |
| Infra/DevOps Engineer | Deployment, CI/CD pipelines, monitoring, cloud infrastructure, secrets management, cost optimization |

## Team Step 3: Spawn Team

Create an agent team with 1 Lead Architect + 1-2 Reviewers + 0-2 Specialists. Use the spawn prompts below.

| Teammate | Name | Role | Always? |
|----------|------|------|---------|
| 1 | Lead Architect | Writes the full TRD draft (role varies by project type) | Yes |
| 2 | Reviewer 1 | Reviews draft from their domain perspective | Yes |
| 3 | Reviewer 2 | Reviews draft from their domain perspective | If project type warrants |
| 4-5 | [Specialists] | Domain-specific review (Security / Database / Performance) | If activated (max 2) |

**Spawn configuration:**
- Require plan approval: NO (teammates should work freely)
- Use delegate mode: YES (lead should not implement, only coordinate)
- Model for teammates: Use the same model as the lead session

### Lead Architect Spawn Prompt — Backend Architect Variant

```
You are the Lead Architect (Backend focus) for a TRD team. Your job is to write
a COMPLETE Technical Requirements Document covering ALL 16 sections of the TRD
template, based on the PRD and the user's technical preferences.

PRODUCT: [insert product name from PRD]
PRD LOCATION: dev-docs/prd.md
USER PREFERENCES: [insert lead Q&A answers]

INSTRUCTIONS:

1. Read dev-docs/prd.md thoroughly — especially any Technical Considerations
   section (Section 7/8 depending on PRD version). If the PRD includes technical
   architecture suggestions, ADOPT and REFINE them rather than starting from scratch.

2. Write a COMPLETE TRD draft covering ALL 16 sections plus appendix.
   Your draft must cover the full system — not just your specialty area.

3. YOUR DEPTH AREAS (write with extra detail):
   - API design (endpoints, request/response formats, versioning)
   - Database schema (entity relationships, indexing, migrations)
   - Caching strategy (layers, TTLs, invalidation)
   - Authentication & authorization architecture
   - Server-side data flows and business logic
   - Error handling and retry patterns

4. OTHER AREAS (write with solid coverage, reviewers will enhance):
   - Frontend architecture (component strategy, state management)
   - Infrastructure & deployment (CI/CD, environments, monitoring)

5. For EVERY technical decision, provide rationale.
   Architecture Decisions table must have at least 5 rows.

6. Ensure every PRD Functional Requirement (FR-xxx) has technical coverage
   somewhere in the TRD. Map FRs to the relevant TRD sections.

OUTPUT INSTRUCTIONS:
1. Write your complete TRD draft to: .trd-workspace/trd-draft.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your draft is ready.
   Do NOT include the full draft in the message — just confirm
   the file is written and give a 3-5 sentence summary of key decisions.
```

### Lead Architect Spawn Prompt — Frontend Architect Variant

```
You are the Lead Architect (Frontend focus) for a TRD team. Your job is to write
a COMPLETE Technical Requirements Document covering ALL 16 sections of the TRD
template, based on the PRD and the user's technical preferences.

PRODUCT: [insert product name from PRD]
PRD LOCATION: dev-docs/prd.md
USER PREFERENCES: [insert lead Q&A answers]

INSTRUCTIONS:

1. Read dev-docs/prd.md thoroughly — especially any Technical Considerations
   section (Section 7/8 depending on PRD version). If the PRD includes technical
   architecture suggestions, ADOPT and REFINE them rather than starting from scratch.

2. Write a COMPLETE TRD draft covering ALL 16 sections plus appendix.
   Your draft must cover the full system — not just your specialty area.

3. YOUR DEPTH AREAS (write with extra detail):
   - Component architecture (hierarchy, composition patterns)
   - Rendering strategy (SSR, SSG, CSR, ISR decisions per route)
   - State management (global vs local, server state, client state)
   - Client-side performance (bundle size, code splitting, lazy loading)
   - UI/UX technical patterns (forms, navigation, animations)
   - Accessibility implementation (ARIA, keyboard nav, screen readers)

4. OTHER AREAS (write with solid coverage, reviewers will enhance):
   - Backend architecture (API design, database, authentication)
   - Infrastructure & deployment (CI/CD, environments, monitoring)

5. For EVERY technical decision, provide rationale.
   Architecture Decisions table must have at least 5 rows.

6. Ensure every PRD Functional Requirement (FR-xxx) has technical coverage
   somewhere in the TRD. Map FRs to the relevant TRD sections.

OUTPUT INSTRUCTIONS:
1. Write your complete TRD draft to: .trd-workspace/trd-draft.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your draft is ready.
   Do NOT include the full draft in the message — just confirm
   the file is written and give a 3-5 sentence summary of key decisions.
```

### Lead Architect Spawn Prompt — Infra/DevOps Engineer Variant

```
You are the Lead Architect (Infra/DevOps focus) for a TRD team. Your job is to
write a COMPLETE Technical Requirements Document covering ALL 16 sections of the
TRD template, based on the PRD and the user's technical preferences.

PRODUCT: [insert product name from PRD]
PRD LOCATION: dev-docs/prd.md
USER PREFERENCES: [insert lead Q&A answers]

INSTRUCTIONS:

1. Read dev-docs/prd.md thoroughly — especially any Technical Considerations
   section (Section 7/8 depending on PRD version). If the PRD includes technical
   architecture suggestions, ADOPT and REFINE them rather than starting from scratch.

2. Write a COMPLETE TRD draft covering ALL 16 sections plus appendix.
   Your draft must cover the full system — not just your specialty area.

3. YOUR DEPTH AREAS (write with extra detail):
   - Deployment architecture (environments, blue/green, canary)
   - CI/CD pipeline (stages, gates, rollback strategy)
   - Monitoring & observability (logging, metrics, tracing, alerting)
   - Cloud infrastructure (services, networking, scaling)
   - Secrets management and security infrastructure
   - Cost optimization and resource planning
   - Disaster recovery and backup strategy

4. OTHER AREAS (write with solid coverage, reviewers will enhance):
   - Frontend architecture (component strategy, state management)
   - Backend architecture (API design, database, authentication)

5. For EVERY technical decision, provide rationale.
   Architecture Decisions table must have at least 5 rows.

6. Ensure every PRD Functional Requirement (FR-xxx) has technical coverage
   somewhere in the TRD. Map FRs to the relevant TRD sections.

OUTPUT INSTRUCTIONS:
1. Write your complete TRD draft to: .trd-workspace/trd-draft.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your draft is ready.
   Do NOT include the full draft in the message — just confirm
   the file is written and give a 3-5 sentence summary of key decisions.
```

### Reviewer Spawn Prompt (Generic — parameterized by role)

```
You are a TRD Reviewer ({ROLE_NAME}) for a TRD team. Your job is to review
the Lead Architect's TRD draft from your domain perspective and provide
structured feedback.

ROLE: {ROLE_NAME}
PRD LOCATION: dev-docs/prd.md
TRD DRAFT LOCATION: .trd-workspace/trd-draft.md

INSTRUCTIONS:

1. Read dev-docs/prd.md first to understand the product requirements.
2. Read .trd-workspace/trd-draft.md — this is the Lead Architect's draft.
3. Review the draft with this universal checklist:

UNIVERSAL REVIEW CHECKLIST:
- PRD Alignment: Does every PRD FR have technical coverage in the TRD?
- Internal Consistency: Are all technology choices compatible with each other?
- Completeness: Are any TRD sections empty or insufficient?
- Implementability: Could a developer build from this spec without guessing?
- Security: Are auth, authz, validation, secrets, and HTTPS all addressed?

4. Then apply YOUR ROLE-SPECIFIC REVIEW FOCUS:

{ROLE_SPECIFIC_FOCUS}

5. Write your review in this format:

## Review by {ROLE_NAME}

### Summary
[2-3 sentence overall assessment of the draft]

### Critical Issues (must fix before finalizing)
- [Issue]: [What's wrong] → [Suggested fix]
- [Issue]: [What's wrong] → [Suggested fix]

### Important Issues (should fix)
- [Issue]: [What's wrong] → [Suggested fix]

### Suggestions (nice to have)
- [Suggestion]: [Rationale]

### What Works Well
- [Strength 1]
- [Strength 2]

OUTPUT INSTRUCTIONS:
1. Write your complete review to: .trd-workspace/{ROLE_SLUG}-review.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your review is ready.
   Do NOT include the full review in the message — just confirm
   the file is written and summarize your top 2-3 findings.
```

**Role-specific focus areas (insert into {ROLE_SPECIFIC_FOCUS}):**

**Backend Architect reviewer:**
```
YOUR REVIEW FOCUS:
- API design: Are endpoints RESTful/consistent? Are request/response schemas complete?
- Database: Is the schema normalized appropriately? Are indexes justified?
- Data flows: Are all data paths documented (create/read/update/delete)?
- Authentication: Is the auth flow complete (signup, login, token refresh, logout)?
- Error handling: Are error codes and retry strategies comprehensive?
- Caching: Are cache invalidation strategies defined?
```

**Frontend Architect reviewer:**
```
YOUR REVIEW FOCUS:
- UI Architecture: Is the component hierarchy well-defined?
- State management: Is the boundary between server/client state clear?
- Performance: Are bundle splitting, lazy loading, and rendering strategies addressed?
- Accessibility: Are WCAG requirements specified at the technical level?
- API integration: Do the API contracts support the UI requirements efficiently?
- Error states: Are loading, error, and empty states covered for each view?
```

**Infra/DevOps Engineer reviewer:**
```
YOUR REVIEW FOCUS:
- Deployment: Are all environments defined with clear promotion paths?
- CI/CD: Is the pipeline complete (lint → test → build → deploy → verify)?
- Monitoring: Are logging, metrics, tracing, and alerting all specified?
- Cost: Are there any cost concerns with the proposed infrastructure?
- Security infra: Are WAF, DDoS protection, and network isolation addressed?
- Scalability: Does the scaling strategy match the growth projections?
```

## Team Step 4: Draft Phase

**CRITICAL LEAD INSTRUCTION:** Wait for the Lead Architect to complete the TRD draft before proceeding. Do NOT start the review phase until the Lead Architect has confirmed the draft is written to `.trd-workspace/trd-draft.md`.

**Lead behavior during draft phase:**
- Wait for the Lead Architect to finish
- If the Lead Architect goes idle without sending a notification, send a direct message prompting them
- When the Lead Architect confirms the draft is ready, verify the file exists by reading `.trd-workspace/trd-draft.md`
- If the file is missing or empty after confirmation, send them a direct message asking them to rewrite it
- Do NOT start writing the TRD yourself
- Only proceed to Team Step 5 when the draft file exists and is non-empty

## Team Step 5: Review Phase

Once the draft is confirmed, broadcast a review instruction to all Reviewers and Specialists:

```
The Lead Architect has completed the TRD draft. Please review it now.

Read these files using the Read tool:
- PRD: dev-docs/prd.md
- TRD Draft: .trd-workspace/trd-draft.md

Write your review to: .trd-workspace/{your-role}-review.md

After writing, send a SHORT notification to the team lead confirming
your review is ready. Do NOT include the full review in the message —
just confirm the file is written and summarize your top 2-3 findings.
```

**Lead behavior during review phase:**
- Wait for ALL reviewers (and specialists, if activated) to complete their reviews
- Monitor task list for all review tasks to reach `completed`
- If a reviewer goes idle without sending a notification, send them a direct message prompting them
- Only proceed to Team Step 6 when ALL expected review files exist and are non-empty

## Team Step 6: Revision Phase (Lead performs revision)

**IMPORTANT**: The lead performs the revision directly — NOT the Lead Architect agent.

**Why the lead does the revision:**
The revision task requires reading the full TRD draft (~50-80KB) plus all review files (~10-15KB each)
plus writing a revised TRD that is even larger. This total context (~150-250KB) exceeds what a
subagent can reliably hold. The lead already has full conversation context from the draft and review
phases, making it the natural performer for revision.

**Lead revision procedure:**

1. Read `.trd-workspace/trd-draft.md` (the original draft)
2. Read all review files: `.trd-workspace/{role}-review.md` for each reviewer/specialist
3. For each review finding:
   - Critical Issues: MUST address — fix the issue or provide explicit rationale for why not
   - Important Issues: SHOULD address — fix or add a note
   - Suggestions: MAY incorporate if they improve the document
4. Apply revisions to the draft using Edit tool (copy draft to `trd-final.md` first, then edit)
5. Add a section at the end: "## 15A. Resolved Review Issues" with a table documenting each
   Critical/Important issue and how it was resolved:
   ```
   | # | Issue | Reviewer | Resolution | Section Updated |
   |---|-------|----------|------------|----------------|
   ```
6. Verify `.trd-workspace/trd-final.md` exists and is non-empty
7. Proceed to Team Step 7

## Team Step 7: Synthesis & Quality Gates

The lead reads `.trd-workspace/trd-final.md` and performs quality gate validation.

1. Read the final TRD from `.trd-workspace/trd-final.md`
2. Run ALL quality gates (see Quality Gates section)
3. Fix any ERROR-level issues inline
4. Note WARNING-level issues
5. Add team mode enhancements to the TRD:
   - Enhanced Architecture Decisions table with "Reviewed by" column
   - Resolved Review Issues section (15A)
   - Review Sources appendix
   - Quality Gate Results table
6. Add the team mode header:
   ```
   > Generated: [Date]
   > Status: Draft
   > Version: 1.0
   > Based on PRD: v[PRD Version]
   > Mode: Team (Lead: {Lead Role} + Reviewers: {Reviewer Roles} + Specialists: {Specialist Names or "none"})
   ```
7. Write the final TRD to `dev-docs/trd.md`

## Team Step 8: Cleanup

After the TRD is written and quality gates pass:
1. Send shutdown requests to all teammates (Lead Architect + Reviewers + Specialists)
2. Wait for all shutdown confirmations
3. Clean up the team (TeamDelete)
4. Delete the workspace: remove `.trd-workspace/` directory
5. Report results to user (include quality gate summary and review highlights)

---

# CONDITIONAL SPECIALISTS

Specialists are optional domain experts that JOIN the review team as additional reviewers when the project matches their domain. They ADD specialized review perspectives — they never replace core reviewers.

## Architecture

```
Core team: 1 Lead Architect + 1-2 Reviewers
Specialist: 0-2 (max 2)
Total specialist pool: 3 (Security Reviewer, Database Architect, Performance Engineer)
Detection: keyword scan → contextual inference → user confirmation
Activation: Lead SUGGESTS, user APPROVES — never auto-spawned
```

## Detection Taxonomy

| Category | Trigger Keywords | Default Specialist |
|----------|-----------------|-------------------|
| Security-critical | authentication, OAuth, JWT, RBAC, encryption, PII, HIPAA, GDPR, SOC2, compliance, fintech, healthcare, payments, multi-tenant | Security Reviewer |
| Data-heavy | PostgreSQL, MongoDB, complex queries, data warehouse, analytics, ETL, migration, sharding, replication, time-series, graph database, full-text search | Database Architect |
| Performance-sensitive | real-time, WebSocket, streaming, high-throughput, low-latency, CDN, caching, load balancing, auto-scaling, concurrent users >10K, sub-100ms | Performance Engineer |

## Detection Logic

Run during Team Step 1.5 (after scoping questions, before spawning):

```
THREE-STEP DETECTION:

Step 1 — Keyword Scan:
  Scan PRD content + user answers for trigger keywords from the taxonomy.
  If 3+ keywords match a single category → strong signal.
  If 1-2 keywords → weak signal, proceed to Step 2.
  If 0 keywords → skip to Step 3 (no specialist).

Step 2 — Contextual Inference:
  Consider the product holistically:
  - Is the domain expertise CORE to the system's reliability?
  - Would the core reviewers miss critical domain-specific issues?
  If yes to both → recommend specialist.

Step 3 — User Confirmation:
  Present recommendation via AskUserQuestion:

  "Based on the PRD, this project has significant [domain] concerns.
   I recommend adding a [Specialist Name] to the review team for
   domain-specific feedback on the TRD."

  Options:
  1. "Add [Specialist] (Recommended)" — adds as additional reviewer
  2. "Add [Alternative Specialist] instead" — different specialist
  3. "Skip specialist — core team only" — no specialist
  4. "Add both: [Specialist 1] + [Specialist 2]" — max 2 specialists

  Never auto-add more than 2 specialists.
  If no category matches, skip this step entirely (no specialist).
```

## Specialist Roster

### 1. Security Reviewer

**Activates for**: Authentication-heavy systems, multi-tenant, compliance-required, payments, healthcare, fintech

```
You are the Security Reviewer specialist for a TRD team. Your job is to
review the Lead Architect's TRD draft from a security perspective and
provide structured feedback.

PRD LOCATION: dev-docs/prd.md
TRD DRAFT LOCATION: .trd-workspace/trd-draft.md

INSTRUCTIONS:

1. Read dev-docs/prd.md to understand security-relevant requirements.
2. Read .trd-workspace/trd-draft.md — this is the Lead Architect's draft.
3. Review with this SECURITY-SPECIFIC FOCUS:

REVIEW FOCUS:
- Authentication flow: Is the complete auth lifecycle specified (signup,
  login, token refresh, logout, password reset, MFA)?
- Authorization: Is the RBAC/ABAC model complete with permission matrix?
- OWASP Top 10: Are mitigations specified for each applicable threat?
- Data protection: Encryption at rest AND in transit? PII handling?
- Secrets management: Are secrets stored securely? No hardcoded credentials?
- Input validation: Is validation specified for all entry points?
- API security: Rate limiting, CORS, CSP headers, JWT validation?
- Compliance: Are regulatory requirements (GDPR, HIPAA, etc.) technically addressed?
- Supply chain: Dependency scanning, SBOM, update policy?
- Incident response: Is there a security incident procedure?

4. Write your review in the standard review format:

## Security Review

### Summary
[2-3 sentence security assessment]

### Critical Issues (must fix)
- [Issue]: [Security risk] → [Remediation]

### Important Issues (should fix)
- [Issue]: [Security risk] → [Remediation]

### Suggestions
- [Suggestion]: [Security rationale]

### What Works Well
- [Security strength 1]

OUTPUT INSTRUCTIONS:
1. Write your complete review to: .trd-workspace/security-review.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your review is ready.
   Do NOT include the full review in the message — just confirm
   the file is written and summarize your top 2-3 findings.
```

### 2. Database Architect

**Activates for**: Complex data models, multiple entity relationships, analytics/reporting features, data migration needs, search functionality

```
You are the Database Architect specialist for a TRD team. Your job is to
review the Lead Architect's TRD draft from a data architecture perspective
and provide structured feedback.

PRD LOCATION: dev-docs/prd.md
TRD DRAFT LOCATION: .trd-workspace/trd-draft.md

INSTRUCTIONS:

1. Read dev-docs/prd.md to understand data-relevant requirements.
2. Read .trd-workspace/trd-draft.md — this is the Lead Architect's draft.
3. Review with this DATABASE-SPECIFIC FOCUS:

REVIEW FOCUS:
- Schema completeness: Does the schema cover ALL entities implied by the PRD?
- Normalization: Is the schema appropriately normalized (not over or under)?
- Indexing: Are indexes defined for all query patterns? Are they justified?
- Query patterns: Are the main query patterns documented? Will they perform?
- Relationships: Are all foreign keys, cascades, and constraints defined?
- Migration strategy: Is the migration approach production-safe (zero-downtime)?
- Data integrity: Are constraints, validations, and transactions specified?
- Search: If full-text search is needed, is the approach specified?
- Backup & recovery: Is the backup strategy and RTO/RPO defined?
- Scaling: Is the data partitioning/sharding strategy appropriate for growth?
- Connection management: Is connection pooling configured appropriately?

4. Write your review in the standard review format:

## Database Architecture Review

### Summary
[2-3 sentence data architecture assessment]

### Critical Issues (must fix)
- [Issue]: [Data risk] → [Fix]

### Important Issues (should fix)
- [Issue]: [Data concern] → [Improvement]

### Suggestions
- [Suggestion]: [Data rationale]

### What Works Well
- [Data architecture strength 1]

OUTPUT INSTRUCTIONS:
1. Write your complete review to: .trd-workspace/database-review.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your review is ready.
   Do NOT include the full review in the message — just confirm
   the file is written and summarize your top 2-3 findings.
```

### 3. Performance Engineer

**Activates for**: Real-time features, high-throughput systems, latency-sensitive applications, large-scale deployments

```
You are the Performance Engineer specialist for a TRD team. Your job is to
review the Lead Architect's TRD draft from a performance perspective and
provide structured feedback.

PRD LOCATION: dev-docs/prd.md
TRD DRAFT LOCATION: .trd-workspace/trd-draft.md

INSTRUCTIONS:

1. Read dev-docs/prd.md to understand performance-relevant requirements.
2. Read .trd-workspace/trd-draft.md — this is the Lead Architect's draft.
3. Review with this PERFORMANCE-SPECIFIC FOCUS:

REVIEW FOCUS:
- Latency targets: Are response time targets specified per endpoint tier
  (P50, P95, P99)? Are they realistic for the architecture?
- Throughput: Can the proposed architecture handle the projected load?
- Caching: Are cache layers, TTLs, and invalidation strategies well-designed?
- Bundle/asset performance: Is code splitting, lazy loading, and asset
  optimization specified? Are Core Web Vitals targets set?
- Database performance: Are N+1 queries, missing indexes, or expensive
  joins identified and mitigated?
- Real-time: If WebSocket/SSE is used, is connection management specified?
- CDN strategy: Is edge caching configured for the right content types?
- Background processing: Are long-running tasks properly offloaded?
- Load testing: Is there a load testing strategy with target thresholds?
- Cost-performance tradeoff: Are the performance targets achievable within
  the infrastructure budget?
- Auto-scaling: Are scaling triggers and limits defined?

4. Write your review in the standard review format:

## Performance Review

### Summary
[2-3 sentence performance assessment]

### Critical Issues (must fix)
- [Issue]: [Performance risk] → [Optimization]

### Important Issues (should fix)
- [Issue]: [Performance concern] → [Improvement]

### Suggestions
- [Suggestion]: [Performance rationale]

### What Works Well
- [Performance strength 1]

OUTPUT INSTRUCTIONS:
1. Write your complete review to: .trd-workspace/performance-review.md
2. After writing the file, send a SHORT notification to the team lead
   via SendMessage confirming your review is ready.
   Do NOT include the full review in the message — just confirm
   the file is written and summarize your top 2-3 findings.
```

---

# QUALITY GATES

## Universal Quality Gates

Applied to EVERY TRD (solo and team mode).

| Gate | Name | Severity | Detection Logic |
|------|------|----------|-----------------|
| TQG-001 | PRD Coverage | ERROR | Every PRD Functional Requirement (FR-xxx) must have technical coverage somewhere in the TRD. List each FR and the TRD section(s) that address it. Flag any FR without coverage. |
| TQG-002 | Tech Consistency | ERROR | All technology choices must be compatible. Verify: frontend framework works with chosen backend, ORM supports chosen database, hosting supports chosen runtime, etc. Flag contradictions (e.g., "SQLite" in database section but "horizontal sharding" in scalability). |
| TQG-003 | Schema-API Alignment | ERROR | Every API endpoint that reads/writes data must correspond to a defined table/collection. Every table must be reachable via at least one endpoint. Flag orphan tables (no endpoint) and ghost endpoints (no backing table). |
| TQG-004 | Security Coverage | ERROR | ALL of the following must be specified: authentication method, authorization model, input validation strategy, secrets management approach, HTTPS enforcement. If any is missing, flag as ERROR. |
| TQG-005 | Performance Targets | WARNING | Every performance requirement from the PRD must have a corresponding target in the TRD. If PRD specifies "fast search" but TRD has no search performance target, flag it. |
| TQG-006 | Infra Completeness | WARNING | TRD must define: at least 2 environments (dev + prod minimum), CI/CD pipeline, monitoring approach, and secrets management. Flag any missing element. |
| TQG-007 | Phase Alignment | WARNING | TRD implementation phases must align with PRD scope. Phase 1 should cover P0 features, Phase 2 should cover P1, etc. Flag misalignment. |
| TQG-008 | Reviewer Integration | WARNING | (Team mode only) All Critical review issues must be either addressed in the revision OR explicitly rejected with rationale in the Resolved Review Issues section. Flag any unresolved Critical issue. Solo mode: mark N/A. |

## Specialist Quality Gates

Applied ONLY when the corresponding specialist is activated.

| Gate | Specialist | Severity | Detection Logic |
|------|-----------|----------|-----------------|
| TQG-SEC-1 | Security Reviewer | ERROR | Auth flow must be fully specified: signup, login, token refresh, logout, password reset. OWASP Top 10 mitigations must be listed for each applicable threat. |
| TQG-SEC-2 | Security Reviewer | WARNING | Data protection must include: encryption at rest strategy, PII classification, data retention policy, and incident response outline. |
| TQG-DB-1 | Database Architect | ERROR | Schema must be complete: every entity from the PRD must have a data model with fields, types, constraints. Indexes must be defined for documented query patterns. |
| TQG-DB-2 | Database Architect | WARNING | Query patterns should be documented with expected complexity (O(1), O(log n), O(n)). Migration strategy should specify zero-downtime approach. |
| TQG-PERF-1 | Performance Engineer | ERROR | Latency targets must be specified per endpoint tier: API endpoints (P95), page loads (LCP), and search (if applicable). |
| TQG-PERF-2 | Performance Engineer | WARNING | Load testing strategy should define: tool, target throughput, success criteria, and when to run (pre-release, continuous). |

## Gate Enforcement Procedure

1. After generating/receiving the TRD, scan for each universal gate (TQG-001 through TQG-008)
2. If specialist was activated, also scan specialist-specific gates
3. For ERROR gates: fix the issue inline before presenting
4. For WARNING gates: add a note in the Quality Gate Results section
5. Append a Quality Gate Results table:

```markdown
## Quality Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| TQG-001 PRD Coverage | PASS / FAIL | [FR mapping details] |
| TQG-002 Tech Consistency | PASS / FAIL | [conflict details if FAIL] |
| TQG-003 Schema-API Alignment | PASS / FAIL | [orphan/ghost details if FAIL] |
| TQG-004 Security Coverage | PASS / FAIL | [missing elements if FAIL] |
| TQG-005 Performance Targets | PASS / WARN | [missing targets] |
| TQG-006 Infra Completeness | PASS / WARN | [missing elements] |
| TQG-007 Phase Alignment | PASS / WARN | [misalignment details] |
| TQG-008 Reviewer Integration | PASS / WARN / N/A | [unresolved issues or N/A for solo] |
| [TQG-XXX-N Specialist Gates] | PASS / FAIL / WARN | [if specialist activated] |
```

---

# TRD TEMPLATE ADDITIONS (Team Mode)

Team mode TRDs include all sections from the solo template, PLUS these additions:

### Enhancement: Architecture Decisions (Reviewed by column)

```markdown
### 1.4 Architecture Decisions

| Decision | Choice | Rationale | Reviewed by |
|----------|--------|-----------|-------------|
| [Decision 1] | [Choice] | [Why] | [Reviewer role(s) who validated] |
| [Decision 2] | [Choice] | [Why] | [Reviewer role(s) who validated] |
```

### Addition: Resolved Review Issues (Section 15A)

```markdown
---

## 15A. Resolved Review Issues

| # | Issue | Reviewer | Resolution | Section Updated |
|---|-------|----------|------------|----------------|
| 1 | [Issue description] | [Reviewer role] | [How it was resolved] | [§N.N] |
| 2 | [Issue description] | [Reviewer role] | [Rejected — rationale: ...] | — |
```

### Addition: Review Sources (Appendix)

```markdown
### E. Review Sources

This TRD was generated using team review:
- **Lead Architect** ({role}): [1-2 sentence summary of approach]
- **Reviewer** ({role}): [1-2 sentence summary of key findings]
- **Reviewer** ({role}): [1-2 sentence summary of key findings] (if 2nd reviewer)
- **Specialist** ({name}): [1-2 sentence summary of key findings] (if activated)
```

---

# SUCCESS CRITERIA

## Solo Mode

A successful solo TRD generation:
- Reads and analyzes the existing PRD from dev-docs/prd.md
- Asks relevant follow-up questions (up to 10) for technical clarity
- Creates a complete TRD at dev-docs/trd.md
- Covers all 16 main sections
- Aligns technical decisions with PRD requirements
- Applies platform-specific best practices
- Includes implementation phases with clear deliverables
- Documents architecture decisions with rationale

## Team Mode

A successful team TRD generation:
- Asks 2-3 scoping questions (not 10)
- Detects project type and assigns appropriate Lead Architect role
- Runs specialist detection (keyword scan → inference → user confirmation)
- Spawns 1 Lead Architect + 1-2 Reviewers + 0-2 Specialists
- Waits for Lead Architect draft before starting reviews
- Collects all reviews before starting revision
- Lead performs revision directly (not delegated to Lead Architect — avoids context overload)
- All Critical review issues addressed or explicitly rejected with rationale
- Architecture decisions annotated with reviewer validation
- Includes Resolved Review Issues section (15A)
- Passes all universal quality gates (TQG-001 through TQG-008)
- If specialist activated: passes specialist-specific quality gates
- Includes Quality Gate Results table
- Cleans up team after TRD is written (shutdown requests → confirmations → TeamDelete → workspace cleanup)

---

# NOTES

- The skill requires dev-docs/prd.md to exist
- Questions adapt based on PRD completeness and technical context
- Platform-specific best practices are automatically applied
- The TRD maintains traceability back to PRD requirements
- Architecture Decision Records (ADRs) can be added to the appendix
- Revision history enables TRD evolution tracking alongside PRD changes
- Team mode requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS to be enabled
- Team mode uses Draft + Review (not Research + Debate like PRD team mode)
- Revision is performed by the lead (not the Lead Architect agent) to avoid context overload — the revision requires reading the full draft (~50-80KB) plus all reviews (~40-60KB total) plus writing an even larger revised document, which exceeds subagent context limits for large TRDs
- Core team always includes: 1 Lead Architect + 1-2 Reviewers
- Lead Architect role is assigned based on project type detection
- Team mode without specialist uses ~3-5x more tokens than solo mode
- Team mode with 1-2 specialists uses ~4-7x more tokens than solo mode
- If team mode fails (e.g., agent teams not available), falls back to solo mode
- Specialists are additive — they provide additional review perspective
- Max 2 specialists per TRD generation to keep reviews focused
- Available specialists: Security Reviewer, Database Architect, Performance Engineer
- Specialist detection is suggestive, not automatic — user always confirms
- If a teammate goes idle without responding, send a direct message to prompt them
