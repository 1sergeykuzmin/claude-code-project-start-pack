# Commit Policy

> Rules for what can and cannot be committed to the repository.
> Enforced by the Completion Protocol and pre-commit hook.

## Overview

This policy defines three categories of files:
1. **NEVER** - Automatically blocked, never commit
2. **ALWAYS** - Safe to commit without prompting
3. **ASK** - Requires user confirmation

---

## NEVER Commit (Auto-blocked)

These files are automatically blocked by the pre-commit hook and Completion Protocol.

### Credentials & Secrets
```
.env
.env.*
!.env.example
!.env.template
*.key
*.pem
*.p12
*.pfx
credentials.*
secrets.*
**/secrets/**
**/credentials/**
```

### Dialog Exports (May Contain Secrets)
```
dialog/*.md
dialog/*.json
dialog/*.txt
.claude/logs/**
```

### Development Artifacts
```
node_modules/
dist/
build/
.next/
out/
coverage/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

### IDE & System Files
```
.idea/
.vscode/settings.json
.vscode/launch.json
*.swp
*.swo
.DS_Store
Thumbs.db
```

### Framework Internal Files
```
.claude/.last_session
.claude/.framework-config
.claude/logs/**
```

---

## ALWAYS Safe to Commit

These files can be committed without prompting.

### Source Code
```
src/**/*.ts
src/**/*.tsx
src/**/*.js
src/**/*.jsx
src/**/*.css
src/**/*.scss
src/**/*.json
```

### Tests
```
tests/**
__tests__/**
*.test.ts
*.test.tsx
*.spec.ts
*.spec.tsx
```

### Configuration (Non-sensitive)
```
package.json
package-lock.json
tsconfig.json
next.config.js
next.config.mjs
tailwind.config.js
postcss.config.js
eslint.config.*
.eslintrc.*
.prettierrc
jest.config.*
vitest.config.*
```

### Documentation
```
README.md
CHANGELOG.md
LICENSE
docs/**/*.md
```

### Project Documents
```
dev-docs/prd.md
dev-docs/trd.md
dev-docs/to-do.md
dev-docs/architecture.md
dev-docs/snapshot.md
```

### Framework Configuration
```
CLAUDE.md
.claude/settings.json
.claude/commands/**/*.md
.claude/protocols/**/*.md
.claude/skills/**/*.md
.claude/COMMIT_POLICY.md
```

### Public Assets
```
public/**
static/**
assets/**
```

### Git Configuration
```
.gitignore
.gitattributes
```

---

## ASK Before Commit (User Confirmation Required)

These patterns require explicit user approval.

### New Directories
```
# Any new top-level directory
# Prompt: "New directory [name] - include in commit?"
```

### Potentially Sensitive Names
```
*config*.json
*secret*
*password*
*token*
*auth*
*key*
```

### Large Files
```
# Files > 1000 lines
# Prompt: "Large file [name] ([lines] lines) - include in commit?"
```

### Binary Files
```
*.png
*.jpg
*.gif
*.ico
*.woff
*.woff2
*.ttf
*.eot
# Prompt: "Binary file [name] - include in commit?"
```

---

## Enforcement

### Pre-commit Hook
The hook at `.claude/scripts/pre-commit-hook.sh` will:
1. Check staged files against NEVER patterns
2. Block commit if violations found
3. List violating files
4. Suggest removal command

### Completion Protocol
During `/fi` or "done", the protocol will:
1. Read this policy file
2. Check all modified files
3. Auto-stage ALWAYS files
4. Prompt for ASK files
5. Skip NEVER files (with warning)

### Manual Override
If you MUST commit a blocked file:
```bash
git commit --no-verify -m "message"
```
**Warning:** Use sparingly. Consider why the file is blocked.

---

## Customization

### Project-Specific Rules
Add patterns to this file for your project:

```markdown
## Project-Specific Rules

### Additional NEVER patterns
- `my-secrets-folder/**`

### Additional ALWAYS patterns
- `my-custom-folder/**/*.ts`
```

### Sync with .gitignore
Ensure NEVER patterns are also in `.gitignore`:
```bash
# Review differences
diff .gitignore .claude/COMMIT_POLICY.md
```

---

## Examples

### Blocked Commit
```
$ git commit -m "Add feature"
🚫 COMMIT BLOCKED by pre-commit hook

Forbidden files detected:
  - .env (credentials)
  - dialog/2024-01-15.md (may contain secrets)

Remove with:
  git reset HEAD .env dialog/2024-01-15.md

Or bypass (not recommended):
  git commit --no-verify
```

### Prompted Commit
```
$ git commit -m "Add feature"
⚠️ Files requiring confirmation:

  [1] config/database.json (sensitive name)
  [2] assets/logo.png (binary file)

Include these files? [y/N/select]:
```

---

## Security Rationale

### Why block dialog exports?
Dialogs may contain:
- Passwords mentioned during debugging
- API keys shown in error messages
- SSH keys pasted for help
- Tokens visible in logs

### Why block .env files?
Even .env.local or .env.development may contain:
- Database credentials
- Third-party API keys
- Internal service URLs
- Authentication secrets

### Why warn on new directories?
New directories might be:
- Accidentally created
- Contain unexpected content
- Break project structure

---

*Last updated: 2024*
*Sync with: .gitignore, pre-commit hook*
