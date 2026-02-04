# Upgrade Framework Command

Upgrade the Claude Code Project Framework to a newer version.

## Usage

```
/upgrade-framework
```

## Purpose

Updates framework components while preserving:
- Your project documents (prd.md, trd.md, to-do.md)
- Your configuration (settings.json)
- Your custom modifications
- Git history

## Process

### Step 0: Pre-flight Checks

```
Checking upgrade prerequisites...

✓ Git repository detected
✓ Working directory clean
✓ Current version: 1.0.0
✓ Framework files located

Checking for updates...
```

If uncommitted changes exist:
```
⚠️ Uncommitted changes detected.
Please commit or stash changes before upgrading.

git stash
# or
git commit -m "WIP: before framework upgrade"
```

### Step 1: Version Detection

```
Current Framework Version: 1.0.0
Latest Available Version: 1.1.0

Changes in 1.1.0:
- New /feature command
- Improved crash recovery
- Bug fixes in completion protocol
```

If already latest:
```
✓ Framework is up to date (v1.0.0)
No upgrade needed.
```

### Step 2: Backup Current Files

```
Creating backup...
├── .claude/backup-1.0.0/
│   ├── commands/
│   ├── protocols/
│   ├── settings.json
│   └── COMMIT_POLICY.md
└── CLAUDE.md.backup

Backup complete. Can restore if needed.
```

### Step 3: Download Updates

```
Downloading framework v1.1.0...
├── commands/ (12 files)
├── protocols/ (3 files)
├── scripts/ (5 files)
├── settings.schema.json
└── CLAUDE.md

Download complete.
```

### Step 4: Merge Configuration

```
Merging configuration...

settings.json:
  ✓ Preserved: Your custom settings
  + Added: New configuration options
  ~ Updated: Default values for new features

COMMIT_POLICY.md:
  ✓ Preserved: Your custom rules
  + Added: New default patterns
```

### Step 5: Update Files

```
Updating framework files...

Updated:
  ✓ .claude/commands/code/feature.md (new)
  ✓ .claude/commands/framework/fi.md (updated)
  ✓ .claude/protocols/cold-start.md (updated)
  ✓ .claude/protocols/completion.md (updated)
  ✓ CLAUDE.md (updated)

Preserved (not modified):
  • dev-docs/prd.md
  • dev-docs/trd.md
  • dev-docs/to-do.md
  • dev-docs/snapshot.md
  • .claude/settings.json (merged)
```

### Step 6: Run Migrations

If version jump requires migrations:

```
Running migrations...

v1.0.0 → v1.1.0:
  ✓ Added crash recovery file format
  ✓ Updated settings schema
  ✓ Migrated command structure

Migrations complete.
```

### Step 7: Verify Installation

```
Verifying upgrade...

Checking files:
  ✓ CLAUDE.md exists and valid
  ✓ All commands present
  ✓ Protocols intact
  ✓ Settings valid
  ✓ Git hooks functional

Framework v1.1.0 installed successfully!
```

### Step 8: Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ Upgrade Complete                                                │
├─────────────────────────────────────────────────────────────────┤
│ Previous version: 1.0.0                                         │
│ New version: 1.1.0                                              │
│                                                                  │
│ What's New:                                                      │
│ • /feature command for planning features                        │
│ • Improved crash recovery in cold-start                         │
│ • Better credential scanning                                    │
│                                                                  │
│ Backup location: .claude/backup-1.0.0/                          │
│                                                                  │
│ Next steps:                                                      │
│ 1. Review CHANGELOG for full details                            │
│ 2. Test new features                                            │
│ 3. Remove backup when satisfied                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Rollback

If issues occur after upgrade:

```bash
# Restore from backup
cp -r .claude/backup-1.0.0/* .claude/
cp CLAUDE.md.backup CLAUDE.md

# Or use git
git checkout HEAD~1 -- .claude/ CLAUDE.md
```

## Version Compatibility

| From | To | Automatic |
|------|-----|-----------|
| 1.0.x | 1.0.y | Yes |
| 1.0.x | 1.1.x | Yes |
| 1.x.x | 2.0.0 | With prompts |

Major version upgrades may require manual steps.

## Offline Upgrade

If no internet access:

```
1. Download release from GitHub
2. Extract to temporary directory
3. Run: /upgrade-framework --local /path/to/release
```

## Configuration Preserved

These are **never** overwritten:
- `dev-docs/*` (your project docs)
- `.claude/settings.json` (merged, not replaced)
- Custom patterns in `COMMIT_POLICY.md`
- `dialog/*` (your exports)

## Force Upgrade

To reinstall even if current:

```
/upgrade-framework --force
```

**Warning:** This overwrites all framework files. Your documents are still preserved.

## Related Commands

| Command | Purpose |
|---------|---------|
| `/upgrade-framework` | Update framework (this command) |
| `/migrate-legacy` | Initial framework installation |
| `/bug-reporting` | Report issues after upgrade |
| `/analyze-bugs` | Check for known issues |
