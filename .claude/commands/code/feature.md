# Feature Command

Plan and implement new features with a structured 6-phase workflow.

## Usage

```
/feature <feature description>
```

## Process

### Phase 1: Requirements Analysis

Clarify what needs to be built:

```
1. Parse the feature description
2. Identify:
   - Core functionality required
   - User-facing behavior expected
   - Edge cases and error scenarios
   - Integration points with existing code
3. Check against PRD (dev-docs/prd.md):
   - Does this align with product requirements?
   - Which user stories does it address?
4. Ask clarifying questions if needed
```

**Output:** Clear understanding of what to build

### Phase 2: Technical Planning

Determine how to implement:

```
1. Review TRD (dev-docs/trd.md) for:
   - Architecture patterns to follow
   - Technology stack constraints
   - API design guidelines
   - Database schema implications

2. Identify required changes:
   - New files to create
   - Existing files to modify
   - API endpoints needed
   - Database migrations required
   - External dependencies

3. Consider:
   - Performance implications
   - Scalability concerns
   - Backward compatibility
```

**Output:** Implementation plan with file list

### Phase 3: Security Review

Evaluate security implications:

```
1. Input validation requirements
   - What user input does this feature accept?
   - How should it be validated and sanitized?

2. Authorization requirements
   - Who should access this feature?
   - What permission checks are needed?

3. Data protection
   - What sensitive data is involved?
   - How should it be stored/transmitted?

4. Attack surface
   - Could this introduce vulnerabilities?
   - SQL injection, XSS, CSRF considerations?
```

**Output:** Security checklist for implementation

### Phase 4: Task Breakdown

Divide into manageable steps:

```
1. Break feature into discrete tasks
2. Order tasks by dependency
3. Estimate complexity (S/M/L)
4. Identify parallelizable work

Format:
| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | Create database migration | S | None |
| 2 | Add API endpoint | M | 1 |
| 3 | Implement service logic | L | 2 |
| 4 | Create UI component | M | 3 |
| 5 | Add tests | M | 3, 4 |
```

**Output:** Ordered task list

### Phase 5: Implementation

Execute the plan:

```
For each task:
1. Read relevant existing code
2. Implement following project patterns
3. Apply best practices:
   - /vercel-react-best-practices (for React)
   - /web-design-guidelines (for UI)
4. Add inline documentation for complex logic
5. Ensure TypeScript types are complete

Code Standards:
- Follow existing code style
- Use meaningful variable names
- Handle errors appropriately
- Consider edge cases
```

**Output:** Working implementation

### Phase 6: Validation

Verify the implementation:

```
1. Manual Testing
   - Does it work as expected?
   - Do edge cases work?
   - Is error handling correct?

2. Code Review
   - Run /codex-review (MANDATORY)
   - Fix any findings
   - Re-run until passing

3. Test Coverage
   - Add unit tests for logic
   - Add integration tests for API
   - Add component tests for UI

4. Documentation
   - Update API docs if needed
   - Update README if needed
```

**Output:** Validated, reviewed, tested feature

## Feature Planning Template

When starting a feature, create this mental model:

```markdown
## Feature: [Name]

### What
[One-sentence description]

### Why
[Business value / user benefit]

### How
[High-level technical approach]

### Scope
**In Scope:**
- [Item 1]
- [Item 2]

**Out of Scope:**
- [Explicitly excluded item]

### Tasks
1. [ ] Task 1
2. [ ] Task 2
3. [ ] Task 3

### Risks
- [Potential issue and mitigation]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## Integration with Project Documents

```
/feature connects to:

┌─────────────┐     ┌─────────────┐
│   prd.md    │────▶│  Feature    │
│ (what users │     │  Planning   │
│    need)    │     │             │
└─────────────┘     └──────┬──────┘
                           │
┌─────────────┐            │
│   trd.md    │────────────┤
│   (how to   │            │
│   build)    │            ▼
└─────────────┘     ┌─────────────┐
                    │Implementation│
┌─────────────┐     │             │
│  to-do.md   │◀────│  (creates   │
│  (if adding │     │   tasks)    │
│   tasks)    │     └─────────────┘
└─────────────┘
```

## Example Session

```
User: /feature Add password reset functionality