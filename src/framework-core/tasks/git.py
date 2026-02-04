"""
Git operations tasks.

Handles git status, diff, commit, and history operations.
"""

import subprocess
import json
from typing import Dict, List, Optional, Any


def _run_git_command(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """
    Run a git command and return the result.

    Args:
        args: Command arguments (without 'git')
        check: Raise exception on non-zero exit

    Returns:
        CompletedProcess result
    """
    return subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=check
    )


def is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    try:
        result = _run_git_command(["rev-parse", "--is-inside-work-tree"], check=False)
        return result.returncode == 0 and result.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def get_status() -> Dict[str, List[str]]:
    """
    Get git status as a structured dictionary.

    Returns:
        Dictionary with 'staged', 'unstaged', and 'untracked' file lists
    """
    status = {
        "staged": [],
        "unstaged": [],
        "untracked": [],
    }

    if not is_git_repo():
        return status

    try:
        result = _run_git_command(["status", "--porcelain", "-z"])
        if not result.stdout:
            return status

        # Parse porcelain output (null-separated)
        entries = result.stdout.split("\0")
        for entry in entries:
            if not entry or len(entry) < 3:
                continue

            index_status = entry[0]
            worktree_status = entry[1]
            filename = entry[3:]

            # Staged changes (index has changes)
            if index_status in ("M", "A", "D", "R", "C"):
                status["staged"].append(filename)

            # Unstaged changes (worktree has changes)
            if worktree_status in ("M", "D"):
                status["unstaged"].append(filename)

            # Untracked files
            if index_status == "?" and worktree_status == "?":
                status["untracked"].append(filename)

    except subprocess.CalledProcessError:
        pass

    return status


def get_diff_stat() -> Dict[str, Any]:
    """
    Get diff statistics for staged and unstaged changes.

    Returns:
        Dictionary with files changed, insertions, deletions
    """
    stat = {
        "files": 0,
        "insertions": 0,
        "deletions": 0,
        "staged": {"files": 0, "insertions": 0, "deletions": 0},
        "unstaged": {"files": 0, "insertions": 0, "deletions": 0},
    }

    if not is_git_repo():
        return stat

    def parse_numstat(output: str) -> Dict[str, int]:
        """Parse --numstat output."""
        result = {"files": 0, "insertions": 0, "deletions": 0}
        for line in output.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                result["files"] += 1
                try:
                    if parts[0] != "-":
                        result["insertions"] += int(parts[0])
                    if parts[1] != "-":
                        result["deletions"] += int(parts[1])
                except ValueError:
                    pass
        return result

    try:
        # Staged changes
        staged_result = _run_git_command(["diff", "--cached", "--numstat"], check=False)
        if staged_result.returncode == 0:
            stat["staged"] = parse_numstat(staged_result.stdout)

        # Unstaged changes
        unstaged_result = _run_git_command(["diff", "--numstat"], check=False)
        if unstaged_result.returncode == 0:
            stat["unstaged"] = parse_numstat(unstaged_result.stdout)

        # Total
        stat["files"] = stat["staged"]["files"] + stat["unstaged"]["files"]
        stat["insertions"] = stat["staged"]["insertions"] + stat["unstaged"]["insertions"]
        stat["deletions"] = stat["staged"]["deletions"] + stat["unstaged"]["deletions"]

    except subprocess.CalledProcessError:
        pass

    return stat


def commit(message: str, add_all: bool = False) -> Optional[str]:
    """
    Create a git commit.

    Args:
        message: Commit message
        add_all: Add all changes before committing

    Returns:
        Commit hash if successful, None otherwise
    """
    if not is_git_repo():
        return None

    try:
        if add_all:
            _run_git_command(["add", "-A"])

        # Check if there's anything to commit
        status = get_status()
        if not status["staged"]:
            return None  # Nothing to commit

        # Create commit with co-author
        full_message = f"{message}\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
        _run_git_command(["commit", "-m", full_message])

        # Get commit hash
        result = _run_git_command(["rev-parse", "HEAD"])
        return result.stdout.strip()

    except subprocess.CalledProcessError:
        return None


def get_recent_commits(n: int = 5) -> List[Dict[str, str]]:
    """
    Get recent commits.

    Args:
        n: Number of commits to retrieve

    Returns:
        List of commit dictionaries with hash, message, author, date
    """
    commits = []

    if not is_git_repo():
        return commits

    try:
        # Use a custom format for easy parsing
        format_str = "%H|%s|%an|%ai"
        result = _run_git_command([
            "log",
            f"-{n}",
            f"--format={format_str}"
        ])

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|", 3)
            if len(parts) >= 4:
                commits.append({
                    "hash": parts[0],
                    "message": parts[1],
                    "author": parts[2],
                    "date": parts[3],
                })

    except subprocess.CalledProcessError:
        pass

    return commits


def get_current_branch() -> Optional[str]:
    """Get the current branch name."""
    if not is_git_repo():
        return None

    try:
        result = _run_git_command(["branch", "--show-current"])
        return result.stdout.strip() or None
    except subprocess.CalledProcessError:
        return None


def has_uncommitted_changes() -> bool:
    """Check if there are any uncommitted changes."""
    status = get_status()
    return bool(status["staged"] or status["unstaged"] or status["untracked"])


def stage_files(files: List[str]) -> bool:
    """
    Stage specific files for commit.

    Args:
        files: List of file paths to stage

    Returns:
        True if successful
    """
    if not is_git_repo() or not files:
        return False

    try:
        _run_git_command(["add"] + files)
        return True
    except subprocess.CalledProcessError:
        return False
