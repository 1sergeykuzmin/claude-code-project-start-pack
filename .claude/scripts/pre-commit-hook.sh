#!/bin/bash

# Pre-commit hook for Claude Code Project Framework
# Blocks commits containing sensitive or forbidden files
# Install with: .claude/scripts/install-git-hooks.sh

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running pre-commit checks...${NC}"

# Forbidden patterns (NEVER commit)
FORBIDDEN_PATTERNS=(
    '\.env$'
    '\.env\.'
    '\.key$'
    '\.pem$'
    '\.p12$'
    '\.pfx$'
    'credentials\.'
    'secrets\.'
    '/secrets/'
    '/credentials/'
    'dialog/.*\.md$'
    'dialog/.*\.json$'
    '\.claude/logs/'
    '\.claude/\.last_session'
    '\.claude/\.framework-config'
    'node_modules/'
    '\.idea/'
    '\.vscode/settings\.json'
    '\.vscode/launch\.json'
)

# Exceptions (allowed even if matching above)
EXCEPTIONS=(
    '\.env\.example$'
    '\.env\.template$'
    'dialog/README\.md$'
    'dialog/\.gitignore$'
)

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}No files staged for commit.${NC}"
    exit 0
fi

BLOCKED_FILES=()
WARNED_FILES=()

# Check each staged file
for file in $STAGED_FILES; do
    # Skip if file matches exception
    is_exception=false
    for exception in "${EXCEPTIONS[@]}"; do
        if [[ "$file" =~ $exception ]]; then
            is_exception=true
            break
        fi
    done

    if $is_exception; then
        continue
    fi

    # Check against forbidden patterns
    for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
        if [[ "$file" =~ $pattern ]]; then
            BLOCKED_FILES+=("$file")
            break
        fi
    done

    # Check for potentially sensitive file names (warning only)
    if [[ "$file" =~ (password|secret|token|private|credential) ]] && \
       [[ ! " ${BLOCKED_FILES[@]} " =~ " ${file} " ]]; then
        WARNED_FILES+=("$file")
    fi

    # Check for large files (> 1000 lines)
    if [ -f "$file" ]; then
        line_count=$(wc -l < "$file" 2>/dev/null || echo "0")
        if [ "$line_count" -gt 1000 ]; then
            WARNED_FILES+=("$file (${line_count} lines)")
        fi
    fi
done

# Report blocked files
if [ ${#BLOCKED_FILES[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}🚫 COMMIT BLOCKED${NC}"
    echo ""
    echo -e "${RED}Forbidden files detected:${NC}"
    for file in "${BLOCKED_FILES[@]}"; do
        echo -e "  ${RED}✗${NC} $file"
    done
    echo ""
    echo "These files match patterns in .claude/COMMIT_POLICY.md"
    echo ""
    echo "To remove from staging:"
    echo -e "  ${YELLOW}git reset HEAD${NC} ${BLOCKED_FILES[*]}"
    echo ""
    echo "To bypass this check (not recommended):"
    echo -e "  ${YELLOW}git commit --no-verify${NC}"
    echo ""
    exit 1
fi

# Report warned files (but allow commit)
if [ ${#WARNED_FILES[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Files flagged for review:${NC}"
    for file in "${WARNED_FILES[@]}"; do
        echo -e "  ${YELLOW}!${NC} $file"
    done
    echo ""
    echo "Proceeding with commit. Review these files for sensitive content."
    echo ""
fi

# Check for potential secrets in file contents
echo "Scanning for potential secrets..."
SECRET_PATTERNS=(
    'password\s*=\s*["\047][^"\047]+'
    'api[_-]?key\s*=\s*["\047][^"\047]+'
    'secret\s*=\s*["\047][^"\047]+'
    'token\s*=\s*["\047][^"\047]+'
    'PRIVATE KEY'
    'BEGIN RSA PRIVATE KEY'
    'BEGIN EC PRIVATE KEY'
    'BEGIN OPENSSH PRIVATE KEY'
)

SECRETS_FOUND=false
for file in $STAGED_FILES; do
    if [ -f "$file" ] && [[ ! "$file" =~ (\.md|\.lock|package-lock\.json)$ ]]; then
        for pattern in "${SECRET_PATTERNS[@]}"; do
            if grep -qE "$pattern" "$file" 2>/dev/null; then
                if ! $SECRETS_FOUND; then
                    echo ""
                    echo -e "${RED}🔐 Potential secrets detected:${NC}"
                    SECRETS_FOUND=true
                fi
                echo -e "  ${RED}✗${NC} $file - matches: $pattern"
                break
            fi
        done
    fi
done

if $SECRETS_FOUND; then
    echo ""
    echo -e "${RED}Review these files before committing.${NC}"
    echo "If these are false positives, you can proceed with:"
    echo -e "  ${YELLOW}git commit --no-verify${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-commit checks passed${NC}"
exit 0
