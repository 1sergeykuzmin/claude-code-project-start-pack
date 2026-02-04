#!/bin/bash
# Auto-Invoke Agent
# Triggers AI-based security scan via /security-dialogs
# Falls back to initial-scan.sh if Claude not active
# Version: 2.0

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=================================="
echo "Auto-Invoke Security Agent"
echo "=================================="
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're in a Claude Code session
# This is heuristic - we check for common indicators
check_claude_session() {
    # Check for Claude session environment variable
    if [ -n "$CLAUDE_SESSION" ]; then
        return 0
    fi

    # Check for .claude/.last_session with active status
    if [ -f ".claude/.last_session" ]; then
        if grep -q '"status": "active"' .claude/.last_session 2>/dev/null; then
            return 0
        fi
    fi

    # Check for running Claude process (macOS/Linux)
    if pgrep -f "claude" > /dev/null 2>&1; then
        return 0
    fi

    return 1
}

# Main logic
if check_claude_session; then
    echo -e "${BLUE}Claude session detected.${NC}"
    echo ""
    echo "To run AI-based security scan, use the command:"
    echo ""
    echo -e "  ${GREEN}/security-dialogs${NC}"
    echo ""
    echo "This will perform:"
    echo "  1. Regex pre-scan for credential patterns"
    echo "  2. AI deep analysis for obfuscated secrets"
    echo "  3. Context-aware credential detection"
    echo "  4. Comprehensive security report"
    echo ""
    echo "The AI scan can detect:"
    echo "  - Split/concatenated credentials"
    echo "  - Base64-encoded secrets"
    echo "  - Credentials in comments"
    echo "  - Environment variable exposures"
    echo "  - Context-dependent secrets"
    echo ""

    # If running interactively, offer to show command
    if [ -t 0 ]; then
        echo "Run /security-dialogs now? (This script cannot invoke Claude commands)"
        echo "Copy and paste the command above into your Claude session."
    fi
else
    echo -e "${YELLOW}No active Claude session detected.${NC}"
    echo ""
    echo "Falling back to initial security scan..."
    echo ""

    # Run initial-scan.sh
    if [ -f "$SCRIPT_DIR/initial-scan.sh" ]; then
        chmod +x "$SCRIPT_DIR/initial-scan.sh"
        "$SCRIPT_DIR/initial-scan.sh"
        exit_code=$?

        echo ""
        echo "=================================="
        echo ""

        if [ $exit_code -eq 0 ]; then
            echo -e "${GREEN}Basic scan complete. No issues found.${NC}"
        else
            echo -e "${YELLOW}Issues found by basic scan.${NC}"
        fi

        echo ""
        echo "For deeper analysis, start a Claude session and run:"
        echo -e "  ${GREEN}/security-dialogs${NC}"

        exit $exit_code
    else
        echo -e "${RED}initial-scan.sh not found at $SCRIPT_DIR${NC}"
        echo ""
        echo "Please run from the project root:"
        echo "  ./security/auto-invoke-agent.sh"
        exit 1
    fi
fi
