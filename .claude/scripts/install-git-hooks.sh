#!/bin/bash

# Install git hooks for Claude Code Project Framework
# Run this script to enable automatic pre-commit checks

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

echo -e "${GREEN}Installing Git hooks for Claude Code Project Framework${NC}"
echo ""

# Check if we're in a git repository
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    echo "Run 'git init' first or navigate to a git repository."
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Install pre-commit hook
PRE_COMMIT_SOURCE="$SCRIPT_DIR/pre-commit-hook.sh"
PRE_COMMIT_TARGET="$HOOKS_DIR/pre-commit"

if [ -f "$PRE_COMMIT_SOURCE" ]; then
    # Check if hook already exists
    if [ -f "$PRE_COMMIT_TARGET" ]; then
        echo -e "${YELLOW}Pre-commit hook already exists.${NC}"
        read -p "Overwrite? [y/N]: " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping pre-commit hook installation."
        else
            cp "$PRE_COMMIT_SOURCE" "$PRE_COMMIT_TARGET"
            chmod +x "$PRE_COMMIT_TARGET"
            echo -e "${GREEN}✓ Pre-commit hook updated${NC}"
        fi
    else
        cp "$PRE_COMMIT_SOURCE" "$PRE_COMMIT_TARGET"
        chmod +x "$PRE_COMMIT_TARGET"
        echo -e "${GREEN}✓ Pre-commit hook installed${NC}"
    fi
else
    echo -e "${RED}Error: pre-commit-hook.sh not found${NC}"
    exit 1
fi

# Summary
echo ""
echo -e "${GREEN}Git hooks installation complete!${NC}"
echo ""
echo "Installed hooks:"
echo "  • pre-commit - Blocks commits with sensitive files"
echo ""
echo "To bypass hooks for a single commit (not recommended):"
echo -e "  ${YELLOW}git commit --no-verify${NC}"
echo ""
echo "To uninstall hooks:"
echo -e "  ${YELLOW}rm $HOOKS_DIR/pre-commit${NC}"
echo ""
