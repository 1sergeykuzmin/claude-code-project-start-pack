#!/bin/bash
# Check Security Triggers
# Verifies all security layers are properly configured
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "=================================="
echo "Security Layer Check"
echo "=================================="
echo ""

ISSUES=0

# ---------------------------------------------
# Layer 1: .gitignore
# ---------------------------------------------
echo "Layer 1: .gitignore"

if [ -f ".gitignore" ]; then
    REQUIRED_PATTERNS=(".env" "*.pem" "*.key" "credentials" "node_modules")
    MISSING=0

    for pattern in "${REQUIRED_PATTERNS[@]}"; do
        if ! grep -q "$pattern" .gitignore 2>/dev/null; then
            ((MISSING++))
        fi
    done

    if [ $MISSING -eq 0 ]; then
        echo -e "  ${GREEN}✓ .gitignore has security patterns${NC}"
    else
        echo -e "  ${YELLOW}⚠ .gitignore missing $MISSING security patterns${NC}"
        ((ISSUES++))
    fi
else
    echo -e "  ${RED}✗ .gitignore not found${NC}"
    ((ISSUES++))
fi

# ---------------------------------------------
# Layer 2: COMMIT_POLICY.md
# ---------------------------------------------
echo ""
echo "Layer 2: COMMIT_POLICY.md"

if [ -f ".claude/COMMIT_POLICY.md" ]; then
    echo -e "  ${GREEN}✓ COMMIT_POLICY.md exists${NC}"

    # Check for NEVER section
    if grep -q "NEVER" .claude/COMMIT_POLICY.md 2>/dev/null; then
        echo -e "  ${GREEN}✓ Contains NEVER patterns${NC}"
    else
        echo -e "  ${YELLOW}⚠ NEVER patterns section not found${NC}"
        ((ISSUES++))
    fi
else
    echo -e "  ${RED}✗ COMMIT_POLICY.md not found${NC}"
    ((ISSUES++))
fi

# ---------------------------------------------
# Layer 3: Pre-commit hook
# ---------------------------------------------
echo ""
echo "Layer 3: Pre-commit hook"

if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "  ${GREEN}✓ Pre-commit hook exists${NC}"

    if [ -x ".git/hooks/pre-commit" ]; then
        echo -e "  ${GREEN}✓ Pre-commit hook is executable${NC}"
    else
        echo -e "  ${YELLOW}⚠ Pre-commit hook not executable${NC}"
        echo "    Fix: chmod +x .git/hooks/pre-commit"
        ((ISSUES++))
    fi

    # Check if it has security patterns
    if grep -q "FORBIDDEN_PATTERNS\|blocked\|\.env" .git/hooks/pre-commit 2>/dev/null; then
        echo -e "  ${GREEN}✓ Pre-commit hook has security checks${NC}"
    else
        echo -e "  ${YELLOW}⚠ Pre-commit hook may not have security patterns${NC}"
        ((ISSUES++))
    fi
else
    echo -e "  ${RED}✗ Pre-commit hook not installed${NC}"
    echo "    Fix: .claude/scripts/install-git-hooks.sh"
    ((ISSUES++))
fi

# ---------------------------------------------
# Layer 4: /security-dialogs command
# ---------------------------------------------
echo ""
echo "Layer 4: /security-dialogs command"

if [ -f ".claude/commands/quality/security-dialogs.md" ]; then
    echo -e "  ${GREEN}✓ /security-dialogs command exists${NC}"
else
    echo -e "  ${RED}✗ /security-dialogs command not found${NC}"
    ((ISSUES++))
fi

# ---------------------------------------------
# Layer 5: /codex-review (mandatory)
# ---------------------------------------------
echo ""
echo "Layer 5: /codex-review"

if [ -f ".claude/skills/codex-review/SKILL.md" ]; then
    echo -e "  ${GREEN}✓ /codex-review skill exists${NC}"
else
    echo -e "  ${RED}✗ /codex-review skill not found${NC}"
    ((ISSUES++))
fi

# Check settings.json for compulsory review
if [ -f ".claude/settings.json" ]; then
    if grep -q '"compulsory": true' .claude/settings.json 2>/dev/null; then
        echo -e "  ${GREEN}✓ Review is set as compulsory${NC}"
    else
        echo -e "  ${YELLOW}⚠ Review may not be compulsory in settings${NC}"
        ((ISSUES++))
    fi
fi

# ---------------------------------------------
# Layer 6: /security command
# ---------------------------------------------
echo ""
echo "Layer 6: /security command"

if [ -f ".claude/commands/quality/security.md" ]; then
    echo -e "  ${GREEN}✓ /security command exists${NC}"
else
    echo -e "  ${RED}✗ /security command not found${NC}"
    ((ISSUES++))
fi

# ---------------------------------------------
# Settings validation
# ---------------------------------------------
echo ""
echo "Settings Validation:"

if [ -f ".claude/settings.json" ]; then
    # Check credentialScan
    if grep -q '"credentialScan": true' .claude/settings.json 2>/dev/null; then
        echo -e "  ${GREEN}✓ Credential scanning enabled${NC}"
    else
        echo -e "  ${YELLOW}⚠ Credential scanning may be disabled${NC}"
        ((ISSUES++))
    fi

    # Check preCommitCheck
    if grep -q '"preCommitCheck": true' .claude/settings.json 2>/dev/null; then
        echo -e "  ${GREEN}✓ Pre-commit check enabled${NC}"
    else
        echo -e "  ${YELLOW}⚠ Pre-commit check may be disabled${NC}"
        ((ISSUES++))
    fi
else
    echo -e "  ${RED}✗ settings.json not found${NC}"
    ((ISSUES++))
fi

# ---------------------------------------------
# Summary
# ---------------------------------------------
echo ""
echo "=================================="
echo "Summary"
echo "=================================="

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}All 6 security layers are properly configured.${NC}"
    exit 0
else
    echo -e "${YELLOW}$ISSUES issue(s) found.${NC}"
    echo ""
    echo "Recommended actions:"
    echo "  1. Run: .claude/scripts/install-git-hooks.sh"
    echo "  2. Review .gitignore patterns"
    echo "  3. Check settings.json security settings"
    exit 1
fi
