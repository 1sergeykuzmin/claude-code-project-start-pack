#!/bin/bash
# Initial Security Scan
# Comprehensive credential and sensitive data detection
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
REPORTS_DIR="security/reports"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
REPORT_FILE="${REPORTS_DIR}/${TIMESTAMP}-initial-scan.txt"
JSON_REPORT="${REPORTS_DIR}/${TIMESTAMP}-initial-scan.json"

# Severity counters
CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0

# Create reports directory if it doesn't exist
mkdir -p "$REPORTS_DIR"

# Initialize JSON report
echo '{' > "$JSON_REPORT"
echo '  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",' >> "$JSON_REPORT"
echo '  "findings": [' >> "$JSON_REPORT"

FIRST_FINDING=true

add_finding() {
    local severity="$1"
    local category="$2"
    local file="$3"
    local description="$4"

    if [ "$FIRST_FINDING" = true ]; then
        FIRST_FINDING=false
    else
        echo ',' >> "$JSON_REPORT"
    fi

    echo '    {' >> "$JSON_REPORT"
    echo '      "severity": "'$severity'",' >> "$JSON_REPORT"
    echo '      "category": "'$category'",' >> "$JSON_REPORT"
    echo '      "file": "'$file'",' >> "$JSON_REPORT"
    echo '      "description": "'$description'"' >> "$JSON_REPORT"
    echo -n '    }' >> "$JSON_REPORT"
}

echo "=================================="
echo "Security Scan - $(date)"
echo "=================================="
echo ""

# Write to report file
echo "Security Scan Report" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "==================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# ---------------------------------------------
# 1. Scan for .env files
# ---------------------------------------------
echo "Scanning for .env files..."
echo "" >> "$REPORT_FILE"
echo "## .env Files" >> "$REPORT_FILE"

ENV_FILES=$(find . -name ".env" -o -name ".env.*" -o -name "*.env" 2>/dev/null | grep -v node_modules | grep -v ".env.example" | grep -v ".env.template" || true)

if [ -n "$ENV_FILES" ]; then
    echo -e "${RED}CRITICAL: .env files found${NC}"
    echo "CRITICAL: .env files found" >> "$REPORT_FILE"
    while IFS= read -r file; do
        echo "  - $file"
        echo "  - $file" >> "$REPORT_FILE"
        add_finding "CRITICAL" "env_file" "$file" ".env file detected"
        ((CRITICAL_COUNT++))
    done <<< "$ENV_FILES"
else
    echo -e "${GREEN}No .env files found${NC}"
    echo "No .env files found" >> "$REPORT_FILE"
fi

# ---------------------------------------------
# 2. Scan for credential files by name
# ---------------------------------------------
echo ""
echo "Scanning for credential files..."
echo "" >> "$REPORT_FILE"
echo "## Credential Files" >> "$REPORT_FILE"

CRED_PATTERNS=(
    "*credentials*"
    "*secret*"
    "*password*"
    "*.pem"
    "*.key"
    "*token*"
    "id_rsa"
    "id_dsa"
    "id_ecdsa"
    "id_ed25519"
    "*.p12"
    "*.pfx"
    "*.jks"
)

CRED_FILES=""
for pattern in "${CRED_PATTERNS[@]}"; do
    found=$(find . -iname "$pattern" -type f 2>/dev/null | grep -v node_modules | grep -v ".git" | grep -v "security/reports" || true)
    if [ -n "$found" ]; then
        CRED_FILES="$CRED_FILES$found"$'\n'
    fi
done

if [ -n "$CRED_FILES" ]; then
    echo -e "${RED}HIGH: Credential files found${NC}"
    echo "HIGH: Credential files found" >> "$REPORT_FILE"
    while IFS= read -r file; do
        if [ -n "$file" ]; then
            echo "  - $file"
            echo "  - $file" >> "$REPORT_FILE"
            add_finding "HIGH" "credential_file" "$file" "Potential credential file detected"
            ((HIGH_COUNT++))
        fi
    done <<< "$CRED_FILES"
else
    echo -e "${GREEN}No credential files found${NC}"
    echo "No credential files found" >> "$REPORT_FILE"
fi

# ---------------------------------------------
# 3. Scan for hardcoded secrets in code
# ---------------------------------------------
echo ""
echo "Scanning for hardcoded secrets..."
echo "" >> "$REPORT_FILE"
echo "## Hardcoded Secrets" >> "$REPORT_FILE"

SECRET_PATTERNS=(
    "password\s*[:=]\s*['\"][^'\"]+['\"]"
    "api_key\s*[:=]\s*['\"][^'\"]+['\"]"
    "apikey\s*[:=]\s*['\"][^'\"]+['\"]"
    "secret\s*[:=]\s*['\"][^'\"]+['\"]"
    "token\s*[:=]\s*['\"][^'\"]+['\"]"
    "access_key\s*[:=]\s*['\"][^'\"]+['\"]"
    "private_key\s*[:=]\s*['\"][^'\"]+['\"]"
    "aws_secret"
    "sk-[a-zA-Z0-9]{32,}"
    "sk_live_[a-zA-Z0-9]+"
    "ghp_[a-zA-Z0-9]{36}"
    "gho_[a-zA-Z0-9]{36}"
)

SECRETS_FOUND=false
for pattern in "${SECRET_PATTERNS[@]}"; do
    results=$(grep -r -i -E "$pattern" --include="*.js" --include="*.ts" --include="*.py" --include="*.java" --include="*.go" --include="*.rb" --include="*.php" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.xml" --include="*.conf" --include="*.config" . 2>/dev/null | grep -v node_modules | grep -v ".git" | grep -v "package-lock" | grep -v "security: ignore" || true)

    if [ -n "$results" ]; then
        if [ "$SECRETS_FOUND" = false ]; then
            echo -e "${RED}HIGH: Potential hardcoded secrets found${NC}"
            echo "HIGH: Potential hardcoded secrets found" >> "$REPORT_FILE"
            SECRETS_FOUND=true
        fi
        while IFS= read -r line; do
            file=$(echo "$line" | cut -d: -f1)
            echo "  - $file"
            echo "  - $line" >> "$REPORT_FILE"
            add_finding "HIGH" "hardcoded_secret" "$file" "Potential hardcoded secret matching: $pattern"
            ((HIGH_COUNT++))
        done <<< "$results"
    fi
done

if [ "$SECRETS_FOUND" = false ]; then
    echo -e "${GREEN}No hardcoded secrets found${NC}"
    echo "No hardcoded secrets found" >> "$REPORT_FILE"
fi

# ---------------------------------------------
# 4. Check .gitignore for security patterns
# ---------------------------------------------
echo ""
echo "Validating .gitignore..."
echo "" >> "$REPORT_FILE"
echo "## .gitignore Validation" >> "$REPORT_FILE"

REQUIRED_PATTERNS=(
    ".env"
    "*.pem"
    "*.key"
    "credentials"
    "secrets"
)

GITIGNORE_ISSUES=false
if [ -f ".gitignore" ]; then
    for pattern in "${REQUIRED_PATTERNS[@]}"; do
        if ! grep -q "$pattern" .gitignore 2>/dev/null; then
            if [ "$GITIGNORE_ISSUES" = false ]; then
                echo -e "${YELLOW}MEDIUM: Missing .gitignore patterns${NC}"
                echo "MEDIUM: Missing .gitignore patterns" >> "$REPORT_FILE"
                GITIGNORE_ISSUES=true
            fi
            echo "  - Missing: $pattern"
            echo "  - Missing: $pattern" >> "$REPORT_FILE"
            add_finding "MEDIUM" "gitignore_missing" ".gitignore" "Missing security pattern: $pattern"
            ((MEDIUM_COUNT++))
        fi
    done

    if [ "$GITIGNORE_ISSUES" = false ]; then
        echo -e "${GREEN}.gitignore has required security patterns${NC}"
        echo ".gitignore has required security patterns" >> "$REPORT_FILE"
    fi
else
    echo -e "${YELLOW}MEDIUM: No .gitignore file found${NC}"
    echo "MEDIUM: No .gitignore file found" >> "$REPORT_FILE"
    add_finding "MEDIUM" "gitignore_missing" ".gitignore" "No .gitignore file found"
    ((MEDIUM_COUNT++))
fi

# ---------------------------------------------
# 5. Finalize JSON report
# ---------------------------------------------
echo '' >> "$JSON_REPORT"
echo '  ],' >> "$JSON_REPORT"
echo '  "summary": {' >> "$JSON_REPORT"
echo '    "critical": '$CRITICAL_COUNT',' >> "$JSON_REPORT"
echo '    "high": '$HIGH_COUNT',' >> "$JSON_REPORT"
echo '    "medium": '$MEDIUM_COUNT >> "$JSON_REPORT"
echo '  }' >> "$JSON_REPORT"
echo '}' >> "$JSON_REPORT"

# ---------------------------------------------
# 6. Summary
# ---------------------------------------------
echo ""
echo "=================================="
echo "Summary"
echo "=================================="
echo "" >> "$REPORT_FILE"
echo "## Summary" >> "$REPORT_FILE"

TOTAL=$((CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT))

if [ $CRITICAL_COUNT -gt 0 ]; then
    echo -e "${RED}CRITICAL: $CRITICAL_COUNT${NC}"
fi
if [ $HIGH_COUNT -gt 0 ]; then
    echo -e "${RED}HIGH: $HIGH_COUNT${NC}"
fi
if [ $MEDIUM_COUNT -gt 0 ]; then
    echo -e "${YELLOW}MEDIUM: $MEDIUM_COUNT${NC}"
fi

echo "CRITICAL: $CRITICAL_COUNT" >> "$REPORT_FILE"
echo "HIGH: $HIGH_COUNT" >> "$REPORT_FILE"
echo "MEDIUM: $MEDIUM_COUNT" >> "$REPORT_FILE"

echo ""
echo "Reports saved to:"
echo "  - $REPORT_FILE"
echo "  - $JSON_REPORT"

# Exit with appropriate code
if [ $CRITICAL_COUNT -gt 0 ]; then
    echo ""
    echo -e "${RED}CRITICAL issues found. Address before committing.${NC}"
    exit 2
elif [ $HIGH_COUNT -gt 0 ]; then
    echo ""
    echo -e "${RED}HIGH severity issues found. Review before committing.${NC}"
    exit 1
elif [ $MEDIUM_COUNT -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}MEDIUM severity issues found. Consider addressing.${NC}"
    exit 3
else
    echo ""
    echo -e "${GREEN}No security issues found.${NC}"
    exit 0
fi
