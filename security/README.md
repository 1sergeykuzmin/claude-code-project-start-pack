# Security Scripts

This directory contains standalone security scripts for the Claude Code Project Framework.

## Purpose

These scripts provide security scanning capabilities that can run:
- During migration (`/migrate-legacy`)
- Before commits (pre-commit hook integration)
- On-demand via command line
- In CI/CD pipelines

## Scripts

| Script | Purpose |
|--------|---------|
| `initial-scan.sh` | Comprehensive security audit for credentials |
| `auto-invoke-agent.sh` | Trigger AI-based deep credential scan |
| `check-triggers.sh` | Verify all security layers are active |
| `cleanup-dialogs.sh` | Redact credentials from exported dialogs |

## Usage

### initial-scan.sh

Full security scan for credentials and sensitive data:

```bash
./security/initial-scan.sh
```

**Exit Codes:**
- `0` - Clean, no issues found
- `1` - HIGH severity findings
- `2` - CRITICAL severity findings
- `3` - MEDIUM severity findings

**What it scans:**
- `.env` files (untracked)
- Credential files by name pattern
- Hardcoded secrets in source code
- Config files with exposed keys
- `.gitignore` validation

### check-triggers.sh

Verify security infrastructure:

```bash
./security/check-triggers.sh
```

**Checks:**
- Pre-commit hook installed
- `.gitignore` has security patterns
- `COMMIT_POLICY.md` exists
- Security settings enabled

### cleanup-dialogs.sh

Redact credentials from dialog exports:

```bash
./security/cleanup-dialogs.sh [--dry-run]
```

**Options:**
- `--dry-run` - Show what would be redacted without changing files

### auto-invoke-agent.sh

Trigger AI-based deep scan via `/security-dialogs`:

```bash
./security/auto-invoke-agent.sh
```

**Behavior:**
- If Claude session active → triggers `/security-dialogs`
- If not active → runs `initial-scan.sh` as fallback

## Reports

Scan results are saved to `security/reports/`:

```
security/reports/
├── 2026-02-04-initial-scan.json
├── 2026-02-04-initial-scan.txt
└── ...
```

Reports are gitignored to prevent accidentally committing findings.

## Integration

### Pre-commit Hook

The pre-commit hook at `.git/hooks/pre-commit` calls these scripts:

```bash
# In pre-commit hook
./security/initial-scan.sh --pre-commit
```

### CI/CD

Add to your pipeline:

```yaml
# GitHub Actions example
- name: Security Scan
  run: |
    chmod +x security/initial-scan.sh
    ./security/initial-scan.sh
```

### Migration

During `/migrate-legacy`, security scan runs automatically:

```
Step 2: Security Scan (Mandatory)

Running security/initial-scan.sh...
[scan results]
```

## Patterns Detected

### Credential Patterns

| Pattern | Example |
|---------|---------|
| `.env` files | `.env`, `.env.local`, `.env.production` |
| Key files | `*.pem`, `*.key`, `id_rsa` |
| Credential files | `credentials.json`, `secrets.yaml` |
| Token files | `token.txt`, `api_token` |

### Hardcoded Secret Patterns

```regex
password\s*[:=]\s*["'][^"']+["']
api_key\s*[:=]\s*["'][^"']+["']
secret\s*[:=]\s*["'][^"']+["']
token\s*[:=]\s*["'][^"']+["']
access_key\s*[:=]\s*["'][^"']+["']
private_key\s*[:=]\s*["'][^"']+["']
```

### Allowed Exceptions

Files that are NOT flagged:
- `.env.example`
- `.env.template`
- `*.example`
- Test fixtures with fake credentials

## Configuration

Security settings in `.claude/settings.json`:

```json
{
  "security": {
    "credentialScan": true,
    "preCommitCheck": true,
    "runSecurityScripts": true,
    "blockedPatterns": [...],
    "allowedPatterns": [...]
  }
}
```

## Troubleshooting

### Script not executable

```bash
chmod +x security/*.sh
```

### Reports directory missing

```bash
mkdir -p security/reports
```

### False positives

Add patterns to `allowedPatterns` in settings.json or use inline comments:

```python
# security: ignore - test fixture
API_KEY = "fake-key-for-testing"
```

## Security Layers

These scripts are part of the 6-layer security model:

```
Layer 1: .gitignore           → Prevents tracking
Layer 2: COMMIT_POLICY.md     → Blocks staging
Layer 3: Pre-commit hook      → Runs these scripts
Layer 4: /security-dialogs    → AI deep scan
Layer 5: /codex-review        → Code quality check
Layer 6: /security            → OWASP audit
```
