# Analyze Bugs Command

Analyze collected bug reports and error patterns.

## Usage

```
/analyze-bugs
```

## Purpose

Reviews locally collected error logs to:
- Identify recurring issues
- Find patterns in failures
- Suggest fixes or workarounds
- Help improve workflow

## Process

### Step 1: Check for Logs

```
Looking for logs in .claude/logs/
├── cold-start/ (3 files)
├── completion/ (2 files)
└── reports/ (0 files)

Total: 5 error logs found
```

If no logs:
```
No error logs found.

Error logging may be disabled. Enable with:
/bug-reporting enable
```

### Step 2: Parse Logs

Extract from each log:
- Timestamp
- Protocol (cold-start/completion)
- Step that failed
- Error message
- Context information

### Step 3: Pattern Analysis

```markdown
## Error Pattern Analysis

### By Protocol
| Protocol | Count | Percentage |
|----------|-------|------------|
| Cold Start | 3 | 60% |
| Completion | 2 | 40% |

### By Step
| Step | Count | Description |
|------|-------|-------------|
| Load Context | 2 | File reading failures |
| Git Commit | 2 | Git operation errors |
| Update Snapshot | 1 | Write permission issue |

### By Error Type
| Type | Count | Example |
|------|-------|---------|
| File Not Found | 2 | snapshot.md missing |
| Git Error | 2 | Nothing to commit |
| Permission | 1 | Cannot write to file |
```

### Step 4: Generate Report

```markdown
## Bug Analysis Report
Generated: 2024-01-15 10:30:00

### Summary
- Total errors: 5
- Date range: 2024-01-10 to 2024-01-15
- Most common: File Not Found (40%)

### Top Issues

#### 1. Missing snapshot.md (2 occurrences)
**When:** Cold Start protocol, Step 2
**Cause:** New project without initialization
**Fix:** Run /migrate-legacy or create dev-docs/snapshot.md

#### 2. Git commit failures (2 occurrences)
**When:** Completion protocol, Step 4
**Cause:** No changes to commit
**Fix:** Protocol should check for changes first

#### 3. Write permission error (1 occurrence)
**When:** Completion protocol, Step 3
**Cause:** File locked or permission issue
**Fix:** Check file permissions, close editors

### Recommendations

1. **Run /migrate-legacy** for new projects
   This creates all required framework files.

2. **Check git status** before commits
   Avoid committing when no changes exist.

3. **Verify file permissions**
   Ensure dev-docs/ is writable.

### Health Score
Framework health: 7/10
- Core functionality: Working
- Some edge cases need handling
```

### Step 5: Suggested Actions

Based on analysis, suggest:
- Configuration changes
- Commands to run
- Files to create
- Framework updates

## Output Locations

Reports are saved to:
```
.claude/logs/analysis/
└── 2024-01-15-analysis.md
```

## Integration with Bug Reporting

If bug reporting is enabled, analysis can:
1. Identify your top issues
2. Check if known fixes exist
3. Suggest relevant updates

## Manual Analysis

You can also review logs manually:

```bash
# List all error logs
find .claude/logs -name "*.json" -type f

# View recent errors
cat .claude/logs/cold-start/*.json | jq '.error'

# Count errors by type
grep -r "error" .claude/logs --include="*.json" | wc -l
```

## When to Run

Run `/analyze-bugs` when:
- Experiencing repeated issues
- Before reporting problems
- After upgrading framework
- Periodic health check

## Related Commands

| Command | Purpose |
|---------|---------|
| `/analyze-bugs` | Analyze patterns (this command) |
| `/bug-reporting` | Enable/disable logging |
| `/upgrade-framework` | Update framework |
| `/migrate-legacy` | Fix missing files |
