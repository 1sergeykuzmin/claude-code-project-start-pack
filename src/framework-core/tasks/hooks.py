"""
Git hooks management tasks.

Handles installation and verification of git hooks.
"""

import os
import stat
from pathlib import Path
from typing import Dict, Optional

# Hook directory
HOOKS_DIR = Path(".git/hooks")

# Hook templates
HOOK_TEMPLATES = {
    "pre-commit": '''#!/bin/bash
# Pre-commit hook for Claude Code Project Framework
# Runs security scan before each commit

set -e

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
NC='\\033[0m'

echo "Running pre-commit security checks..."

# Check for blocked patterns
BLOCKED_PATTERNS=(
    "\\.env$"
    "\\.pem$"
    "\\.key$"
    "credentials\\.json$"
    "secrets\\.yaml$"
    "id_rsa$"
)

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

for file in $STAGED_FILES; do
    for pattern in "${BLOCKED_PATTERNS[@]}"; do
        if echo "$file" | grep -qE "$pattern"; then
            echo -e "${RED}BLOCKED: $file matches blocked pattern: $pattern${NC}"
            echo "Remove this file from staging with: git reset HEAD $file"
            exit 1
        fi
    done
done

# Run security scan if available
if [ -f "security/initial-scan.sh" ]; then
    ./security/initial-scan.sh --pre-commit
    if [ $? -eq 2 ]; then
        echo -e "${RED}CRITICAL security issues found. Commit blocked.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Pre-commit checks passed.${NC}"
exit 0
''',
    "post-commit": '''#!/bin/bash
# Post-commit hook for Claude Code Project Framework
# Updates session state after commit

COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --format=%s)

# Update .last_session if it exists
if [ -f ".claude/.last_session" ]; then
    # Simple update - just note the commit
    echo "Last commit: $COMMIT_HASH" >> .claude/.framework-log
fi

exit 0
''',
}


def is_hook_installed(hook_name: str) -> bool:
    """
    Check if a git hook is installed.

    Args:
        hook_name: Name of the hook (e.g., "pre-commit")

    Returns:
        True if hook exists and is executable
    """
    hook_path = HOOKS_DIR / hook_name

    if not hook_path.exists():
        return False

    # Check if executable
    return os.access(hook_path, os.X_OK)


def install_hook(hook_name: str, script_path: Optional[str] = None) -> bool:
    """
    Install a git hook.

    Args:
        hook_name: Name of the hook
        script_path: Path to custom script (uses template if None)

    Returns:
        True if installation successful
    """
    if not HOOKS_DIR.exists():
        return False  # Not a git repo

    hook_path = HOOKS_DIR / hook_name

    try:
        if script_path:
            # Copy from provided script
            with open(script_path, "r") as f:
                content = f.read()
        elif hook_name in HOOK_TEMPLATES:
            # Use built-in template
            content = HOOK_TEMPLATES[hook_name]
        else:
            return False  # Unknown hook

        # Write hook file
        with open(hook_path, "w") as f:
            f.write(content)

        # Make executable
        hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        return True

    except IOError:
        return False


def uninstall_hook(hook_name: str) -> bool:
    """
    Remove a git hook.

    Args:
        hook_name: Name of the hook to remove

    Returns:
        True if removal successful
    """
    hook_path = HOOKS_DIR / hook_name

    if not hook_path.exists():
        return True  # Already not installed

    try:
        # Rename to .bak instead of deleting
        backup_path = hook_path.with_suffix(".bak")
        hook_path.rename(backup_path)
        return True
    except IOError:
        return False


def verify_all_hooks() -> Dict[str, bool]:
    """
    Verify all required hooks are installed.

    Returns:
        Dictionary mapping hook names to installation status
    """
    required_hooks = ["pre-commit", "post-commit"]

    return {
        hook: is_hook_installed(hook)
        for hook in required_hooks
    }


def install_all_hooks() -> Dict[str, bool]:
    """
    Install all required hooks.

    Returns:
        Dictionary mapping hook names to installation success
    """
    required_hooks = ["pre-commit", "post-commit"]
    results = {}

    for hook in required_hooks:
        if not is_hook_installed(hook):
            results[hook] = install_hook(hook)
        else:
            results[hook] = True  # Already installed

    return results


def get_hook_content(hook_name: str) -> Optional[str]:
    """
    Get the content of an installed hook.

    Args:
        hook_name: Name of the hook

    Returns:
        Hook content or None if not installed
    """
    hook_path = HOOKS_DIR / hook_name

    if not hook_path.exists():
        return None

    try:
        with open(hook_path, "r") as f:
            return f.read()
    except IOError:
        return None


def hook_has_security_patterns(hook_name: str = "pre-commit") -> bool:
    """
    Check if a hook contains security-related patterns.

    Args:
        hook_name: Name of the hook to check

    Returns:
        True if hook has security patterns
    """
    content = get_hook_content(hook_name)
    if not content:
        return False

    security_indicators = [
        "BLOCKED_PATTERNS",
        "security",
        ".env",
        "credentials",
        "initial-scan",
    ]

    return any(indicator in content for indicator in security_indicators)
