# Pull Request Command

Create well-structured pull requests using GitHub CLI.

## Process

### Step 1: Analyze Branch State

```bash
# Check current branch and status
git branch --show-current
git status

# See all commits since diverging from main
git log main..HEAD --oneline

# Review all changes
git diff main...HEAD --stat
```

### Step 2: Identify Base Branch

Typically `main` or `master`. Verify:
```bash
git remote show origin | grep "HEAD branch"
```

### Step 3: Review ALL Changes

**CRITICAL:** Analyze ALL commits, not just the latest one.

```bash
# Full diff against base
git diff main...HEAD

# List all changed files
git diff main...HEAD --name-only
```

### Step 4: Ensure Branch is Pushed

```bash
# Check if tracking remote
git status -sb

# Push if needed
git push -u origin $(git branch --show-current)
```

### Step 5: Create PR

```bash
gh pr create --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary

[2-3 bullet points describing what this PR does]

## Why

[Motivation for this change - what problem does it solve?]

## What Changed

### Added
- [New feature/file]

### Changed
- [Modified behavior]

### Fixed
- [Bug fix]

## Technical Details

[Any important implementation notes]

## Test Plan

- [ ] [How to test this change]
- [ ] [Edge cases to verify]

## Screenshots

[If UI changes, include before/after]

## Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] `/codex-review` passed

## Related

- PRD: [Reference if applicable]
- TRD: [Reference if applicable]
- Fixes #[issue number]

---
Generated with [Claude Code](https://claude.ai/claude-code)
EOF
)"
```

### Step 6: Verify

```bash
gh pr view --web
```

## PR Title Convention

| Prefix | Use For |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `refactor:` | Code restructuring |
| `test:` | Test additions |
| `chore:` | Maintenance |

## Security Checklist

Before creating PR, verify:
- [ ] No secrets in code
- [ ] Input validation present
- [ ] SQL queries parameterized
- [ ] Auth checks in place
- [ ] Error messages don't leak info

## Tips

### Large PRs
Break into smaller, focused PRs when possible.

### Draft PRs
```bash
gh pr create --draft --title "WIP: feature name"
```

### Assign Reviewers
```bash
gh pr create --reviewer username1,username2
```

### Link to Issue
Include `Fixes #123` or `Closes #123` in description.
