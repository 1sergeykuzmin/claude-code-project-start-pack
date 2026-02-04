# Bug Reporting Command

Manage framework error reporting settings.

## Usage

```
/bug-reporting [enable|disable|status|test]
```

## Modes

### Enable

```
/bug-reporting enable
```

Activates anonymous error logging:
- Logs Cold Start and Completion protocol errors
- Stores logs in `.claude/logs/`
- Optionally submits critical errors for analysis

**What's collected:**
- Protocol step that failed
- Error message (sanitized)
- Framework version
- Anonymized project ID

**What's NOT collected:**
- Source code
- File contents
- API keys or credentials
- Personal information
- Project name or path

### Disable

```
/bug-reporting disable
```

Turns off all logging:
- Stops error collection
- Existing logs preserved in `.claude/logs/`
- No data submission

### Status

```
/bug-reporting status
```

Shows current configuration:

```
Bug Reporting Status
────────────────────
Enabled: Yes
Version: 1.0.0
Project ID: a1b2c3 (anonymized)

Logs:
  Cold Start: 3 entries
  Completion: 2 entries
  Last error: 2024-01-14 10:30:00

Storage: .claude/logs/
```

### Test

```
/bug-reporting test
```

Generates a sample report without submitting:

```markdown
## Sample Bug Report

### Environment
- Framework: 1.0.0
- Project ID: a1b2c3

### Error
- Protocol: cold-start
- Step: 2 (Load Context)
- Message: File not found: dev-docs/snapshot.md

### Context
- Previous step: Success
- Session state: active

[This is a TEST report - not submitted]
```

## Configuration

Settings stored in `.claude/.framework-config`:

```json
{
  "bugReporting": {
    "enabled": true,
    "projectId": "a1b2c3d4",
    "consentDate": "2024-01-15",
    "submitCritical": false
  }
}
```

## Log Storage

Logs are stored locally:

```
.claude/logs/
├── cold-start/
│   ├── 2024-01-15-error.json
│   └── 2024-01-14-error.json
├── completion/
│   └── 2024-01-15-error.json
└── reports/
    └── submitted/
```

## Privacy Guarantees

### Data Anonymization

Before any logging:
1. File paths stripped to relative
2. Project name replaced with hash
3. Credentials patterns redacted
4. User-specific info removed

### Local-First

- All logs stay in `.claude/logs/`
- Logs are gitignored
- Manual deletion always available

### Opt-In Only

- Disabled by default
- Explicit consent required
- Can disable anytime

## Manual Log Management

```bash
# View logs
ls -la .claude/logs/

# Read specific log
cat .claude/logs/cold-start/2024-01-15-error.json

# Clear all logs
rm -rf .claude/logs/*

# Clear old logs (keep last 7 days)
find .claude/logs -type f -mtime +7 -delete
```

## When to Enable

Consider enabling if:
- You want to help improve the framework
- You're experiencing repeated issues
- You're comfortable with anonymous telemetry

Consider keeping disabled if:
- Working on sensitive projects
- Strict privacy requirements
- Offline environment

## Error Categories

| Category | Logged | Example |
|----------|--------|---------|
| Protocol failure | Yes | Cold start step 3 failed |
| File not found | Yes | snapshot.md missing |
| Git error | Yes | Commit failed |
| User action | No | User chose to skip |
| Code error | No | Application bugs |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/bug-reporting` | Manage settings (this command) |
| `/analyze-bugs` | Analyze collected reports |
| `/upgrade-framework` | Update to fix known bugs |
