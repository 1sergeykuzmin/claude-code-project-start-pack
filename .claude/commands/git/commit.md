# Git Commit Command

Create structured git commits following conventional commit standards.

## Process

### Step 1: Analyze Changes
```bash
git status
git diff --staged
git diff
git log --oneline -5
```

Review:
- What files have been modified
- What changes are staged vs unstaged
- Recent commit style for consistency

### Step 2: Security Check

**NEVER commit these files:**
- `.env`, `.env.*` (except `.env.example`)
- `*.key`, `*.pem`, `credentials.*`, `secrets.*`
- `node_modules/`, `dist/`, `build/`
- IDE settings (`.idea/`, `.vscode/` unless shared)

If user explicitly requests committing sensitive files, warn them about risks.

### Step 3: Stage Files Selectively

```bash
# Stage specific files, NOT git add .
git add path/to/file1
git add path/to/file2
```

Group related changes into logical commits.

### Step 4: Compose Commit Message

**Format:**
```
<type>(<scope>): <short summary>

<detailed explanation - what and why, not how>

<footer>
```

**Types:**
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting (no logic change) |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

**Examples:**
```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh to prevent session expiration.
Tokens are refreshed 5 minutes before expiry.

PRD FR-003
Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix(api): handle null response from payment provider

Payment API occasionally returns null instead of error object.
Added defensive check to prevent runtime crash.

Fixes #123
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 5: Execute Commit

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <summary>

<body>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Verify

```bash
git log -1 --stat
git status
```

## Pre-Commit Checklist

- [ ] No sensitive data in committed files
- [ ] Code review passed (`/codex-review`)
- [ ] Tests pass (if applicable)
- [ ] Commit message follows convention
- [ ] Changes are logically grouped

## Restrictions

- **NO** `git add .` or `git add -A`
- **NO** `--no-verify` without explicit user request
- **NO** committing `.env` files
- **NO** vague messages like "fix", "update", "changes"
- **NO** commented-out code in commits
