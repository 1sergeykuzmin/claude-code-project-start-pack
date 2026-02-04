# Review Command

Perform comprehensive manual code review with structured checklist.

## Usage

```
/review [file-or-pattern]
```

If no file specified, reviews all uncommitted changes.

## Review Process

### Step 1: Identify Changes

```bash
# If no file specified
git diff --name-only
git diff --staged --name-only

# If file/pattern specified
# Review those specific files
```

### Step 2: Review Each File

For each changed file, evaluate against all categories below.

---

## Review Categories

### 1. Security (Critical)

| Check | Description |
|-------|-------------|
| Input Validation | All user input validated server-side |
| Authorization | Permission checks on protected operations |
| SQL Injection | Parameterized queries, no string concatenation |
| XSS Prevention | No `dangerouslySetInnerHTML` with user data |
| CSRF Protection | State-changing operations protected |
| Secret Exposure | No hardcoded credentials, API keys |
| Error Messages | Don't leak internal details |

**Questions to ask:**
- Could an attacker exploit this code?
- Is user input trusted without validation?
- Are there authorization bypass possibilities?

### 2. Code Quality

| Check | Description |
|-------|-------------|
| TypeScript | Strict types, no `any` without justification |
| Naming | Clear, descriptive variable/function names |
| Comments | Complex logic documented |
| DRY | No unnecessary duplication |
| KISS | Simple solutions preferred |
| Dead Code | No commented-out or unused code |

**Questions to ask:**
- Would a new developer understand this code?
- Is there a simpler way to do this?
- Are names self-documenting?

### 3. Architecture

| Check | Description |
|-------|-------------|
| Patterns | Follows project's established patterns |
| Separation | Client/Server components properly separated |
| Dependencies | No circular dependencies |
| Modularity | Single responsibility principle |
| Abstraction | Right level of abstraction |

**Questions to ask:**
- Does this fit the existing architecture?
- Is this the right place for this code?
- Are concerns properly separated?

### 4. Performance

| Check | Description |
|-------|-------------|
| Re-renders | No unnecessary React re-renders |
| Memoization | Expensive computations memoized |
| Database | Queries optimized, N+1 avoided |
| Bundle Size | No unnecessary imports |
| Blocking | No blocking operations in render |

**Questions to ask:**
- Will this scale with more data/users?
- Are there obvious optimization opportunities?
- Could this cause performance issues?

### 5. Error Handling

| Check | Description |
|-------|-------------|
| Try/Catch | Errors properly caught and handled |
| User Feedback | Errors communicated appropriately |
| Logging | Errors logged for debugging |
| Recovery | Graceful degradation where possible |
| Edge Cases | Boundary conditions handled |

**Questions to ask:**
- What happens when this fails?
- Are all error paths handled?
- Will users understand what went wrong?

### 6. Testing

| Check | Description |
|-------|-------------|
| Coverage | New code has tests |
| Edge Cases | Tests cover boundary conditions |
| Mocking | External dependencies properly mocked |
| Assertions | Tests verify correct behavior |

**Questions to ask:**
- How would I test this?
- What could break that isn't tested?
- Are tests testing behavior, not implementation?

---

## Output Format

For each file reviewed, provide:

```markdown
## [filename]

### ✅ Strengths
- [What's done well]

### ⚠️ Suggestions
- [Improvement with code example if helpful]

### ❌ Issues (Must Fix)
- [Critical problem requiring change]
```

## Summary Format

After reviewing all files:

```markdown
## Review Summary

### Overall Assessment
[APPROVE / APPROVE WITH SUGGESTIONS / REQUEST CHANGES]

### Statistics
- Files reviewed: [N]
- Issues found: [N] critical, [N] suggestions
- Security concerns: [Yes/No]

### Top 3 Action Items
1. [Most important fix]
2. [Second priority]
3. [Third priority]

### Positive Highlights
- [Something done particularly well]
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ❌ Critical | Security issue, bug, or major problem | Must fix before merge |
| ⚠️ Suggestion | Improvement opportunity | Should consider |
| 💡 Note | Minor observation | Optional |

## Quick Checklist

Before approving any code:

- [ ] No security vulnerabilities
- [ ] TypeScript types complete
- [ ] Error handling present
- [ ] No console.log left in code
- [ ] No TODO comments for critical items
- [ ] Tests added for new functionality
- [ ] Existing tests still pass
- [ ] Code follows project conventions

## Difference from /codex-review

| /review | /codex-review |
|---------|---------------|
| Manual checklist-based | Automated via Codex CLI |
| Comprehensive analysis | Quick automated scan |
| Use for thorough review | Use after every task (mandatory) |
| Generates discussion | Generates pass/fail |

**Recommendation:** Use both - `/codex-review` for quick validation, `/review` for thorough analysis before major merges.
