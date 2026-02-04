# Security Dialogs Command

Deep AI-based credential scanning for dialog exports and recent changes.

## Usage

```
/security-dialogs
```

## Purpose

This command performs Layer 4 security scanning - AI-based analysis that catches secrets traditional regex patterns miss:

- **Obfuscated credentials** - `password = chars.join('')`
- **Split credentials** - Password split across multiple lines
- **Context-dependent secrets** - "The API key I mentioned earlier"
- **Encoded credentials** - Base64 or hex-encoded secrets
- **Composite secrets** - Username + password combined

## Scanning Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: .gitignore              (Prevents tracking)           │
├─────────────────────────────────────────────────────────────────┤
│ Layer 2: COMMIT_POLICY.md        (Blocks staging)              │
├─────────────────────────────────────────────────────────────────┤
│ Layer 3: Pre-commit hook         (Regex patterns)              │
├─────────────────────────────────────────────────────────────────┤
│ Layer 4: /security-dialogs       (AI deep scan) ← THIS COMMAND │
└─────────────────────────────────────────────────────────────────┘
```

## Process

### Step 1: Identify Scope

Scan only recent/relevant content:
```
- Most recent dialog export (if exists)
- Uncommitted changes (git diff)
- Recently modified files (last 5 commits)
```

**NOT scanned** (too expensive):
- Entire codebase
- All historical dialogs
- node_modules, build artifacts

### Step 2: Regex Pre-scan

Run quick pattern matching first:
```
Patterns:
- password\s*=\s*["'][^"']+
- api[_-]?key\s*=\s*["'][^"']+
- secret\s*=\s*["'][^"']+
- token\s*=\s*["'][^"']+
- PRIVATE KEY
- Bearer [A-Za-z0-9-_]+
```

Report findings immediately (1-2 seconds).

### Step 3: AI Deep Analysis

For content that passed regex but may contain secrets:

**Analyze for:**
1. **Character array joins**
   ```javascript
   const p = ['p','a','s','s'].join('');
   ```

2. **Split-line credentials**
   ```javascript
   const part1 = "abc";
   const part2 = "xyz";
   const secret = part1 + part2;
   ```

3. **Context references**
   ```
   "Use the same key we discussed"
   "The password from the config"
   ```

4. **Encoded values**
   ```javascript
   const secret = atob("c2VjcmV0MTIz");
   ```

5. **Environment variable shadows**
   ```javascript
   // Hardcoded fallback
   const key = process.env.API_KEY || "sk-1234567890";
   ```

### Step 4: Report Findings

```markdown
## Security Scan Results

### Scan Scope
- Dialog: dialog/2024-01-15-abc123.md
- Changed files: 5
- Lines analyzed: 342

### Findings

#### 🔴 Critical (Must Fix)
1. **Hardcoded API key fallback**
   - File: src/lib/api.ts:45
   - Pattern: Environment variable with hardcoded default
   - Fix: Remove hardcoded fallback

#### 🟡 Warning (Review)
2. **Potential password reference**
   - File: dialog/2024-01-15.md:123
   - Context: "the password is..."
   - Action: Verify this dialog is gitignored

### Recommendations
1. Remove hardcoded fallback in api.ts
2. Ensure dialog/ is in .gitignore
3. Run /commit only after fixes
```

## When to Run

**Automatically triggered by:**
- Completion Protocol (if high-risk changes detected)
- Pre-commit hook (on failure, suggests this scan)

**Manually run when:**
- Before pushing to remote
- After debugging session with credentials
- Before sharing code
- When onboarding new team members

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Confirmed credential exposure | Must fix before commit |
| 🟡 Warning | Potential secret reference | Review and confirm safe |
| 🟢 Info | Pattern matched but likely safe | Acknowledge only |

## Integration with Workflow

```
Development Session:
│
├─► Make changes
├─► /codex-review (code quality)
├─► /security-dialogs (if prompted or manual)
├─► /commit (if all clear)
└─► /fi (end session)
```

## Performance

| Step | Time |
|------|------|
| Scope identification | ~1s |
| Regex pre-scan | ~2s |
| AI deep analysis | ~1-2 min |
| Report generation | ~1s |

**Total:** 1-3 minutes depending on scope

## False Positive Handling

If the scan flags something incorrectly:

```
1. Review the finding
2. If truly safe, acknowledge
3. Consider adding to allowlist in COMMIT_POLICY.md
4. Proceed with commit
```

## Configuration

In `.claude/settings.json`:
```json
{
  "security": {
    "credentialScan": true,
    "deepScanOnCompletion": "auto",  // auto, always, never
    "scanDialogs": true,
    "scanChangedFiles": true
  }
}
```
