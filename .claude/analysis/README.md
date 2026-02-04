# Analysis Documents

This directory contains architectural decision records and design documentation for the Claude Code Project Framework.

## Purpose

These documents serve to:
1. Record why decisions were made
2. Document trade-offs considered
3. Provide context for future contributors
4. Track framework evolution

## Documents

| Document | Description |
|----------|-------------|
| `execution-mode-decision.md` | Why we chose dual mode (verbose + silent) |
| `python-core-decision.md` | Why Python is required for parallel execution |
| `dialog-exporter-decision.md` | Why we implemented full TypeScript exporter |
| `preset-system-design.md` | How the preset system works |
| `silent-mode-philosophy.md` | The philosophy behind silent mode |
| `integration-retrospective.md` | Post-integration lessons learned |

## When to Add Documents

Add a new document when:
- Making a significant architectural decision
- Choosing between multiple viable approaches
- Implementing a major new feature
- Changing fundamental framework behavior

## Document Template

```markdown
# [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue? Why are we making this decision?]

## Decision
[What is the decision?]

## Options Considered
### Option A: [Name]
- Pros: ...
- Cons: ...

### Option B: [Name]
- Pros: ...
- Cons: ...

## Consequences
[What are the implications of this decision?]

## Related Decisions
[Links to related documents]
```

## Maintenance

- Documents should be updated when decisions change
- Deprecated decisions should be marked, not deleted
- Cross-references should be maintained
