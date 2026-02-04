"""
JSON-based structured logging for framework operations.

Logs to .claude/logs/{protocol}/{date}.json with automatic rotation.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import threading

# Thread-safe logging
_log_lock = threading.Lock()

# Global configuration
_config = {
    "log_dir": ".claude/logs",
    "silent_mode": False,
    "max_age_days": 7,
    "initialized": False,
}


def setup_logging(
    log_dir: str = ".claude/logs",
    silent_mode: bool = False,
    max_age_days: int = 7
) -> None:
    """
    Configure the logging system.

    Args:
        log_dir: Directory for log files
        silent_mode: If True, suppress stdout output
        max_age_days: Days to keep log files (0 = no rotation)
    """
    global _config
    _config.update({
        "log_dir": log_dir,
        "silent_mode": silent_mode,
        "max_age_days": max_age_days,
        "initialized": True,
    })

    # Ensure log directory exists
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Run log rotation
    if max_age_days > 0:
        _rotate_logs()


def _rotate_logs() -> None:
    """Remove log files older than max_age_days."""
    log_dir = Path(_config["log_dir"])
    if not log_dir.exists():
        return

    cutoff = datetime.now() - timedelta(days=_config["max_age_days"])

    for log_file in log_dir.rglob("*.json"):
        try:
            # Check file modification time
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < cutoff:
                log_file.unlink()
        except (OSError, ValueError):
            pass  # Skip files we can't process


def _get_log_path(protocol: str) -> Path:
    """Get the log file path for today's date."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = Path(_config["log_dir"]) / protocol
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{date_str}.json"


def log_task(
    name: str,
    status: str,
    duration_ms: int,
    protocol: str = "general",
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a task execution.

    Args:
        name: Task name
        status: Execution status (success/error/skipped)
        duration_ms: Execution time in milliseconds
        protocol: Protocol name for log organization
        details: Additional task details
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "task": name,
        "status": status,
        "duration_ms": duration_ms,
    }

    if details:
        entry["details"] = details

    _write_log_entry(protocol, entry)


def log_protocol(
    protocol: str,
    status: str,
    total_duration_ms: int,
    task_count: int,
    error_count: int = 0,
    summary: Optional[str] = None
) -> None:
    """
    Log a protocol execution summary.

    Args:
        protocol: Protocol name
        status: Execution status
        total_duration_ms: Total execution time
        task_count: Number of tasks executed
        error_count: Number of failed tasks
        summary: Optional summary message
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "protocol_summary",
        "protocol": protocol,
        "status": status,
        "total_duration_ms": total_duration_ms,
        "task_count": task_count,
        "error_count": error_count,
    }

    if summary:
        entry["summary"] = summary

    _write_log_entry(protocol, entry)


def log_error(
    protocol: str,
    error: str,
    task: Optional[str] = None,
    stack_trace: Optional[str] = None
) -> None:
    """
    Log an error.

    Args:
        protocol: Protocol name
        error: Error message
        task: Task name where error occurred
        stack_trace: Optional stack trace
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "error",
        "error": error,
    }

    if task:
        entry["task"] = task
    if stack_trace:
        entry["stack_trace"] = stack_trace

    _write_log_entry(protocol, entry)

    # Always output errors to stderr unless in silent mode
    if not _config["silent_mode"]:
        import sys
        print(f"[ERROR] {error}", file=sys.stderr)


def _write_log_entry(protocol: str, entry: Dict[str, Any]) -> None:
    """Write a log entry to the log file (thread-safe)."""
    with _log_lock:
        log_path = _get_log_path(protocol)

        # Read existing entries
        entries = []
        if log_path.exists():
            try:
                with open(log_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        entries = json.loads(content)
                        if not isinstance(entries, list):
                            entries = [entries]
            except (json.JSONDecodeError, IOError):
                entries = []

        # Append new entry
        entries.append(entry)

        # Write back
        try:
            with open(log_path, "w") as f:
                json.dump(entries, f, indent=2)
        except IOError as e:
            import sys
            print(f"[WARN] Failed to write log: {e}", file=sys.stderr)


def get_recent_logs(
    protocol: str,
    days: int = 1,
    status_filter: Optional[str] = None
) -> list:
    """
    Get recent log entries.

    Args:
        protocol: Protocol name
        days: Number of days to look back
        status_filter: Filter by status (success/error/skipped)

    Returns:
        List of log entries
    """
    entries = []
    log_dir = Path(_config["log_dir"]) / protocol

    if not log_dir.exists():
        return entries

    cutoff = datetime.now() - timedelta(days=days)

    for log_file in sorted(log_dir.glob("*.json"), reverse=True):
        try:
            # Check date from filename
            date_str = log_file.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                break

            with open(log_file, "r") as f:
                file_entries = json.load(f)
                if not isinstance(file_entries, list):
                    file_entries = [file_entries]

                for entry in file_entries:
                    if status_filter is None or entry.get("status") == status_filter:
                        entries.append(entry)

        except (json.JSONDecodeError, IOError, ValueError):
            continue

    return entries
