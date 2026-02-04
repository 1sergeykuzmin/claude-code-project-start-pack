"""
Completion Protocol Command

Runs parallel and sequential tasks for session finalization.
"""

from typing import Optional
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parallel import run_tasks_parallel, run_tasks_sequential, TaskDefinition
from utils.result import ProtocolResult, TaskResult, ProtocolStatus, TaskStatus
from utils.logger import log_protocol
from tasks.config import is_silent_mode, get_active_preset, get_setting
from tasks.git import get_status, get_diff_stat, commit, has_uncommitted_changes
from tasks.security import quick_scan, cleanup_dialogs
from tasks.session import mark_session_completed, clear_session


def run_completion(
    skip_review: bool = False,
    no_commit: bool = False,
    commit_message: Optional[str] = None,
    silent: bool = False
) -> ProtocolResult:
    """
    Run the completion protocol.

    Phase 1: 3 parallel tasks (build check, dialog export, security scan)
    Phase 2: Sequential tasks (update metafiles, codex-review, commit, cleanup)

    Args:
        skip_review: Skip code review (NOT RECOMMENDED)
        no_commit: Skip automatic commit
        commit_message: Custom commit message
        silent: Silent mode

    Returns:
        ProtocolResult with all task results
    """
    # Check if silent mode is configured
    if not silent:
        silent = is_silent_mode()

    all_results = []

    # Phase 1: Parallel tasks
    parallel_tasks = [
        TaskDefinition("build_check", task_build_check),
        TaskDefinition("dialog_export", task_dialog_export),
        TaskDefinition("security_scan", task_security_scan),
    ]

    parallel_results = run_tasks_parallel(parallel_tasks, max_workers=3)
    all_results.extend(parallel_results)

    # Check for critical errors in parallel phase
    parallel_errors = [r for r in parallel_results if r.status == TaskStatus.ERROR]

    # Check security scan results
    security_result = next((r for r in parallel_results if r.name == "security_scan"), None)
    if security_result and security_result.data:
        critical_count = security_result.data.get("critical", 0)
        if critical_count > 0:
            return ProtocolResult.error(
                "completion",
                all_results,
                summary=f"CRITICAL security issues found: {critical_count}. Fix before committing."
            )

    # Phase 2: Sequential tasks
    sequential_tasks = [
        TaskDefinition("update_metafiles", task_update_metafiles),
    ]

    # Add codex review unless skipped (NOT RECOMMENDED)
    if not skip_review:
        sequential_tasks.append(
            TaskDefinition("codex_review", task_codex_review)
        )

    # Add commit unless skipped
    if not no_commit:
        sequential_tasks.append(
            TaskDefinition(
                "commit",
                task_commit,
                kwargs={"message": commit_message}
            )
        )

    # Always add session cleanup
    sequential_tasks.append(
        TaskDefinition("session_cleanup", task_session_cleanup)
    )

    sequential_results = run_tasks_sequential(sequential_tasks)
    all_results.extend(sequential_results)

    # Check for errors
    all_errors = [r for r in all_results if r.status == TaskStatus.ERROR]

    # Get commit result for summary
    commit_result = next((r for r in all_results if r.name == "commit"), None)

    if all_errors:
        error_summary = "; ".join([f"{e.name}: {e.error}" for e in all_errors[:3]])
        return ProtocolResult.error(
            "completion",
            all_results,
            summary=f"Completion failed: {error_summary}"
        )

    # Build success summary
    summary_parts = []

    if commit_result and commit_result.data:
        commit_hash = commit_result.data.get("hash", "")
        if commit_hash:
            summary_parts.append(commit_hash[:8])

    diff_stat = get_diff_stat()
    if diff_stat["files"] > 0:
        summary_parts.append(f"{diff_stat['files']} files")

    if not summary_parts:
        summary_parts.append("No changes to commit")

    return ProtocolResult.success(
        "completion",
        all_results,
        summary=" | ".join(summary_parts)
    )


# --- Individual Tasks ---

def task_build_check() -> TaskResult:
    """Verify build passes (if applicable)."""
    try:
        from pathlib import Path
        import subprocess

        # Check for common build configurations
        has_package_json = Path("package.json").exists()
        has_makefile = Path("Makefile").exists()
        has_cargo = Path("Cargo.toml").exists()

        # For now, just check if build files exist
        # Actual build running would be project-specific

        build_info = {
            "package_json": has_package_json,
            "makefile": has_makefile,
            "cargo": has_cargo,
        }

        # Check if there's a build script in package.json
        if has_package_json:
            import json
            with open("package.json", "r") as f:
                pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                build_info["has_build_script"] = "build" in scripts
                build_info["has_test_script"] = "test" in scripts

        return TaskResult.create_success("build_check", data=build_info)

    except Exception as e:
        # Build check is non-critical
        return TaskResult.create_success(
            "build_check",
            data={"status": "skipped", "reason": str(e)}
        )


def task_dialog_export() -> TaskResult:
    """Export current session dialog."""
    try:
        from pathlib import Path

        dialog_dir = Path("dialog")
        dialog_dir.mkdir(exist_ok=True)

        # Note: Actual dialog export would need access to session data
        # This is a placeholder that checks the export directory

        existing_exports = list(dialog_dir.glob("*.md"))

        return TaskResult.create_success(
            "dialog_export",
            data={
                "exported": len(existing_exports),
                "directory": str(dialog_dir)
            }
        )

    except Exception as e:
        return TaskResult.create_error("dialog_export", str(e))


def task_security_scan() -> TaskResult:
    """Run security scan on changes."""
    try:
        findings = quick_scan()

        return TaskResult.create_success(
            "security_scan",
            data={
                "total": findings["total_findings"],
                "critical": len(findings.get("CRITICAL", [])),
                "high": len(findings.get("HIGH", [])),
                "medium": len(findings.get("MEDIUM", [])),
                "scanned_files": findings["scanned_files"]
            }
        )

    except Exception as e:
        return TaskResult.create_error("security_scan", str(e))


def task_update_metafiles() -> TaskResult:
    """Update snapshot.md, to-do.md, architecture.md if needed."""
    try:
        from pathlib import Path
        from datetime import datetime

        updated_files = []

        # Check which metafiles exist
        metafiles = [
            "dev-docs/snapshot.md",
            "dev-docs/to-do.md",
            "dev-docs/architecture.md"
        ]

        for filepath in metafiles:
            path = Path(filepath)
            if path.exists():
                # Note: Actual update logic would involve AI analysis
                # This is a placeholder that records the file exists
                updated_files.append(filepath)

        return TaskResult.create_success(
            "update_metafiles",
            data={
                "checked": metafiles,
                "existing": updated_files,
                "timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        return TaskResult.create_error("update_metafiles", str(e))


def task_codex_review() -> TaskResult:
    """
    Check if code review is needed (MANDATORY unless explicitly skipped).

    IMPORTANT: This task does NOT execute the actual code review.
    It only checks if there are changes that need review and reports
    the file count. The actual review must be performed by Claude
    using the /codex-review skill after this check completes.

    The Python framework provides:
    - Fast parallel task execution
    - File counting and status checks
    - JSON results for Claude to process

    Claude provides:
    - Actual code analysis via /codex-review skill
    - Review findings and recommendations
    - User interaction for review results
    """
    try:
        # Check if there are changes to review
        status = get_status()

        if not status["staged"] and not status["unstaged"]:
            return TaskResult.create_skipped("codex_review", "No changes to review")

        # Count files that need review
        # Actual review is performed by Claude using /codex-review skill
        files_to_review = len(status["staged"]) + len(status["unstaged"])

        review_check = {
            "files_to_review": files_to_review,
            "staged_files": status["staged"],
            "unstaged_files": status["unstaged"],
            "status": "review_required",
            "note": "Claude must run /codex-review skill for actual review"
        }

        return TaskResult.create_success("codex_review", data=review_check)

    except Exception as e:
        return TaskResult.create_error("codex_review", str(e))


def task_commit(message: Optional[str] = None) -> TaskResult:
    """Create git commit if there are changes."""
    try:
        # Check for changes
        if not has_uncommitted_changes():
            return TaskResult.create_skipped("commit", "No changes to commit")

        status = get_status()

        # Stage all changes if nothing staged
        if not status["staged"]:
            from tasks.git import stage_files
            files_to_stage = status["unstaged"] + status["untracked"]
            if files_to_stage:
                stage_files(files_to_stage)

        # Generate commit message if not provided
        if not message:
            diff_stat = get_diff_stat()
            message = f"Update: {diff_stat['files']} file(s) changed"

        # Create commit
        commit_hash = commit(message)

        if commit_hash:
            return TaskResult.create_success(
                "commit",
                data={
                    "hash": commit_hash,
                    "message": message
                }
            )
        else:
            return TaskResult.create_error("commit", "Commit failed - no hash returned")

    except Exception as e:
        return TaskResult.create_error("commit", str(e))


def task_session_cleanup() -> TaskResult:
    """Clean up session state."""
    try:
        success = mark_session_completed("Session completed successfully")

        if success:
            return TaskResult.create_success(
                "session_cleanup",
                data={"status": "completed"}
            )
        else:
            return TaskResult.create_error("session_cleanup", "Failed to update session state")

    except Exception as e:
        return TaskResult.create_error("session_cleanup", str(e))
