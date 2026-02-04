"""
Cold Start Protocol Command

Runs 10 parallel initialization tasks for session startup.
"""

from typing import Optional
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parallel import run_tasks_parallel, TaskDefinition
from utils.result import ProtocolResult, TaskResult, ProtocolStatus, TaskStatus
from utils.logger import log_protocol, log_task
from tasks.config import read_framework_config, write_framework_config, is_silent_mode, get_active_preset
from tasks.git import is_git_repo, get_status
from tasks.hooks import verify_all_hooks, install_all_hooks
from tasks.security import quick_scan
from tasks.session import is_crash_detected, get_crash_info, mark_session_active, read_last_session
from tasks.version import get_current_version, is_update_available, get_update_info


def run_cold_start(
    skip_update: bool = False,
    skip_security: bool = False,
    silent: bool = False
) -> ProtocolResult:
    """
    Run the cold start protocol with 10 parallel tasks.

    Args:
        skip_update: Skip version update check
        skip_security: Skip security scan
        silent: Silent mode (minimal output)

    Returns:
        ProtocolResult with all task results
    """
    # Check if silent mode is configured
    if not silent:
        silent = is_silent_mode()

    # Define all cold start tasks
    task_definitions = [
        TaskDefinition("migration_cleanup", task_migration_cleanup),
        TaskDefinition("crash_detection", task_crash_detection),
        TaskDefinition("config_init", task_config_init),
        TaskDefinition("context_load", task_context_load),
        TaskDefinition("git_hooks_install", task_git_hooks_install),
        TaskDefinition("commit_policy_verify", task_commit_policy_verify),
    ]

    # Conditionally add optional tasks
    if not skip_update:
        task_definitions.append(TaskDefinition("version_check", task_version_check))

    if not skip_security:
        task_definitions.append(TaskDefinition("security_cleanup", task_security_cleanup))

    # Add dialog export check
    task_definitions.append(TaskDefinition("dialog_export", task_dialog_export))

    # Add session activation (always last conceptually, but runs in parallel)
    task_definitions.append(TaskDefinition("session_activate", task_session_activate))

    # Run all tasks in parallel
    results = run_tasks_parallel(task_definitions, max_workers=10)

    # Analyze results
    errors = [r for r in results if r.status == TaskStatus.ERROR]
    crash_result = next((r for r in results if r.name == "crash_detection"), None)
    update_result = next((r for r in results if r.name == "version_check"), None)

    # Determine overall status
    if crash_result and crash_result.data and crash_result.data.get("crash_detected"):
        # Crash detected - need user input
        crash_info = crash_result.data.get("crash_info", {})
        prompt = f"""
Previous session may have crashed.
Last task: {crash_info.get('task', 'Unknown')}
Time: {crash_info.get('timestamp', 'Unknown')}

Options:
1. Continue from where you left off
2. Start fresh (discard previous state)
3. View recovery details

Please choose an option.
"""
        return ProtocolResult.user_input_required("cold-start", results, prompt)

    if errors:
        # Has errors
        error_summary = "; ".join([f"{e.name}: {e.error}" for e in errors[:3]])
        return ProtocolResult.error(
            "cold-start",
            results,
            summary=f"Cold start completed with {len(errors)} error(s): {error_summary}"
        )

    # Success
    summary_parts = []
    summary_parts.append(f"v{get_current_version()}")

    if update_result and update_result.data and update_result.data.get("update_available"):
        summary_parts.append(f"Update available: {update_result.data.get('latest_version')}")

    preset = get_active_preset()
    summary_parts.append(f"Preset: {preset}")

    return ProtocolResult.success(
        "cold-start",
        results,
        summary=" | ".join(summary_parts)
    )


# --- Individual Tasks ---

def task_migration_cleanup() -> TaskResult:
    """Check for incomplete migrations and clean up if needed."""
    migration_log = ".claude/migration-log.json"

    try:
        import json
        from pathlib import Path

        log_path = Path(migration_log)
        if not log_path.exists():
            return TaskResult.create_success("migration_cleanup", data={"status": "no_migration"})

        with open(log_path, "r") as f:
            log_data = json.load(f)

        status = log_data.get("status", "")

        if status == "in_progress":
            return TaskResult.create_success(
                "migration_cleanup",
                data={
                    "status": "migration_pending",
                    "migration_id": log_data.get("migration_id"),
                    "message": "Incomplete migration detected. Run /migrate-resolve to continue."
                }
            )

        return TaskResult.create_success("migration_cleanup", data={"status": "clean"})

    except Exception as e:
        return TaskResult.create_error("migration_cleanup", str(e))


def task_crash_detection() -> TaskResult:
    """Detect if previous session crashed."""
    try:
        crash_detected = is_crash_detected()

        if crash_detected:
            crash_info = get_crash_info()
            return TaskResult.create_success(
                "crash_detection",
                data={
                    "crash_detected": True,
                    "crash_info": crash_info
                }
            )

        return TaskResult.create_success(
            "crash_detection",
            data={"crash_detected": False}
        )

    except Exception as e:
        return TaskResult.create_error("crash_detection", str(e))


def task_version_check() -> TaskResult:
    """Check for framework updates."""
    try:
        current = get_current_version()
        update_available = is_update_available()

        data = {
            "current_version": current,
            "update_available": update_available
        }

        if update_available:
            update_info = get_update_info()
            if update_info:
                data["latest_version"] = update_info.get("latest_version")

        return TaskResult.create_success("version_check", data=data)

    except Exception as e:
        # Version check failure is non-critical
        return TaskResult.create_success(
            "version_check",
            data={
                "current_version": get_current_version(),
                "update_available": False,
                "error": str(e)
            }
        )


def task_security_cleanup() -> TaskResult:
    """Run quick security scan on recent changes."""
    try:
        findings = quick_scan()

        if findings["total_findings"] > 0:
            return TaskResult.create_success(
                "security_cleanup",
                data={
                    "findings": findings["total_findings"],
                    "critical": len(findings.get("CRITICAL", [])),
                    "high": len(findings.get("HIGH", [])),
                    "medium": len(findings.get("MEDIUM", []))
                }
            )

        return TaskResult.create_success(
            "security_cleanup",
            data={"findings": 0, "status": "clean"}
        )

    except Exception as e:
        return TaskResult.create_error("security_cleanup", str(e))


def task_commit_policy_verify() -> TaskResult:
    """Verify COMMIT_POLICY.md exists and is valid."""
    try:
        from pathlib import Path

        policy_path = Path(".claude/COMMIT_POLICY.md")

        if not policy_path.exists():
            return TaskResult.create_success(
                "commit_policy_verify",
                data={
                    "exists": False,
                    "warning": "COMMIT_POLICY.md not found"
                }
            )

        content = policy_path.read_text()
        has_never_section = "NEVER" in content.upper()

        return TaskResult.create_success(
            "commit_policy_verify",
            data={
                "exists": True,
                "has_never_section": has_never_section
            }
        )

    except Exception as e:
        return TaskResult.create_error("commit_policy_verify", str(e))


def task_git_hooks_install() -> TaskResult:
    """Ensure git hooks are installed."""
    try:
        if not is_git_repo():
            return TaskResult.create_skipped("git_hooks_install", "Not a git repository")

        hook_status = verify_all_hooks()
        all_installed = all(hook_status.values())

        if not all_installed:
            # Install missing hooks
            install_results = install_all_hooks()
            return TaskResult.create_success(
                "git_hooks_install",
                data={
                    "installed": install_results,
                    "action": "installed_missing"
                }
            )

        return TaskResult.create_success(
            "git_hooks_install",
            data={
                "status": hook_status,
                "action": "already_installed"
            }
        )

    except Exception as e:
        return TaskResult.create_error("git_hooks_install", str(e))


def task_config_init() -> TaskResult:
    """Initialize .framework-config if needed."""
    try:
        config = read_framework_config()

        if not config.get("first_run_completed"):
            # First run - initialize
            config["first_run_completed"] = True
            config["framework_version"] = get_current_version()
            write_framework_config(config)

            return TaskResult.create_success(
                "config_init",
                data={
                    "action": "initialized",
                    "version": config["framework_version"]
                }
            )

        return TaskResult.create_success(
            "config_init",
            data={
                "action": "loaded",
                "version": config.get("framework_version", "unknown")
            }
        )

    except Exception as e:
        return TaskResult.create_error("config_init", str(e))


def task_context_load() -> TaskResult:
    """Load context from snapshot.md and to-do.md."""
    try:
        from pathlib import Path

        context = {
            "snapshot_exists": False,
            "todo_exists": False,
            "prd_exists": False,
        }

        # Check for key files
        files_to_check = [
            ("snapshot_exists", "dev-docs/snapshot.md"),
            ("todo_exists", "dev-docs/to-do.md"),
            ("prd_exists", "dev-docs/prd.md"),
        ]

        for key, filepath in files_to_check:
            if Path(filepath).exists():
                context[key] = True

        return TaskResult.create_success("context_load", data=context)

    except Exception as e:
        return TaskResult.create_error("context_load", str(e))


def task_dialog_export() -> TaskResult:
    """Check for pending dialog exports."""
    try:
        from pathlib import Path

        dialog_dir = Path("dialog")
        claude_sessions = Path.home() / ".claude" / "projects"

        # Check if dialog directory exists
        if not dialog_dir.exists():
            dialog_dir.mkdir(exist_ok=True)

        # Count existing exports
        existing_exports = list(dialog_dir.glob("*.md"))

        # Check for pending exports (sessions not yet exported)
        pending_exports = 0
        if claude_sessions.exists():
            # Look for session files that might need export
            session_files = list(claude_sessions.glob("**/*.jsonl"))
            # Simple heuristic: if more session files than exports, some may be pending
            pending_exports = max(0, len(session_files) - len(existing_exports))

        return TaskResult.create_success(
            "dialog_export",
            data={
                "exported_count": len(existing_exports),
                "pending_count": pending_exports,
                "directory": str(dialog_dir)
            }
        )

    except Exception as e:
        # Dialog export check is non-critical
        return TaskResult.create_success(
            "dialog_export",
            data={"status": "skipped", "reason": str(e)}
        )


def task_session_activate() -> TaskResult:
    """Mark session as active."""
    try:
        success = mark_session_active("Cold start initiated")

        if success:
            return TaskResult.create_success(
                "session_activate",
                data={"status": "active"}
            )
        else:
            return TaskResult.create_error("session_activate", "Failed to write session file")

    except Exception as e:
        return TaskResult.create_error("session_activate", str(e))
