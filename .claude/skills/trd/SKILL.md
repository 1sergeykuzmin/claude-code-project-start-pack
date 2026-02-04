---
name: trd
description: Generate a Technical Requirements Document (TRD) from the existing PRD. Use when asked to create a TRD, document technical specifications, or plan implementation architecture. Invoked as "/trd".
metadata:
  author: custom
  version: "1.0.0"
---

# Technical Requirements Document Generator

Generate comprehensive Technical Requirements Documents based on the Product Requirements Document (PRD). This skill analyzes the PRD, considers platform-specific best practices, and produces a detailed technical specification.

## Overview

When invoked with `/trd`, this skill:
1. Reads and analyzes the PRD from `dev-docs/prd.md`
2. Extracts technical implications from product requirements
3. Identifies gaps in technical context
4. Asks up to 10 targeted follow-up questions
5. Generates a comprehensive TRD at `dev-docs/trd.md`

## Input Format

```
/trd
```

No arguments required. The skill reads context from `dev-docs/prd.md`.

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

## Success Criteria

A successful TRD generation:
- Reads and analyzes the existing PRD from dev-docs/prd.md
- Asks relevant follow-up questions (up to 10) for technical clarity
- Creates a complete TRD at dev-docs/trd.md
- Covers all 16 main sections
- Aligns technical decisions with PRD requirements
- Applies platform-specific best practices
- Includes implementation phases with clear deliverables
- Documents architecture decisions with rationale

## Notes

- The skill requires dev-docs/prd.md to exist
- Questions adapt based on PRD completeness and technical context
- Platform-specific best practices are automatically applied
- The TRD maintains traceability back to PRD requirements
- Architecture Decision Records (ADRs) can be added to the appendix
- Revision history enables TRD evolution tracking alongside PRD changes
