# Release Command

Manage version releases with semantic versioning.

## Process

### Step 1: Pre-Release Checks

```bash
# Ensure clean working directory
git status

# Ensure on main branch
git branch --show-current

# Pull latest
git pull origin main

# Check for uncommitted changes
git diff --stat
```

**STOP if:**
- Working directory has uncommitted changes
- Not on main/master branch
- Behind remote

### Step 2: Analyze Changes Since Last Release

```bash
# Find last release tag
git describe --tags --abbrev=0

# See commits since last release
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Categorize by type
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s"
```

### Step 3: Determine Version Bump

**Semantic Versioning: MAJOR.MINOR.PATCH**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking changes | MAJOR | 1.0.0 → 2.0.0 |
| New features (backward compatible) | MINOR | 1.0.0 → 1.1.0 |
| Bug fixes, patches | PATCH | 1.0.0 → 1.0.1 |

**Commit Type Mapping:**
- `feat:` → MINOR
- `fix:` → PATCH
- `BREAKING CHANGE:` → MAJOR
- `docs:`, `style:`, `refactor:`, `test:`, `chore:` → PATCH

### Step 4: Update Version Numbers

Update version in relevant files:
- `package.json`
- `CLAUDE.md` (if version mentioned)
- Any version constants in code

### Step 5: Update Changelog

Add entry to `dev-docs/changelog.md`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description (PRD FR-XXX)

### Changed
- Modified behavior description

### Fixed
- Bug fix description (Fixes #123)

### Removed
- Removed feature description

### Security
- Security improvement description
```

### Step 6: Create Release Commit

```bash
git add -A
git commit -m "$(cat <<'EOF'
chore(release): bump version to X.Y.Z

Release highlights:
- Feature 1
- Feature 2
- Bug fix 1

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 7: Create Git Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### Step 8: Push Release

```bash
git push origin main
git push origin vX.Y.Z
```

### Step 9: Create GitHub Release (Optional)

```bash
gh release create vX.Y.Z \
  --title "Release vX.Y.Z" \
  --notes "$(cat <<'EOF'
## What's New

### Added
- Feature 1
- Feature 2

### Fixed
- Bug fix 1

### Changed
- Change 1

**Full Changelog**: https://github.com/user/repo/compare/vX.Y.Z-1...vX.Y.Z
EOF
)"
```

## Changelog Template

Create `dev-docs/changelog.md` if it doesn't exist:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Fixed
### Removed

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release
```

## Pre-Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version numbers updated
- [ ] Security audit passed (`/security`)
- [ ] No breaking changes undocumented
