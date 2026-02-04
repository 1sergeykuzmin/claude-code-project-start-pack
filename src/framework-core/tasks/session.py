"""
Session state management tasks.

Handles .last_session file for crash detection and recovery.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

# Session file path
SESSION_FILE = Path(".claude/.last_session")


def read_last_session() -> Optional[Dict[str, Any]]:
    """
    Read the last session state.

    Returns:
        Session state dictionary or None if no session file
    """
    if not SESSION_FILE.exists():
        return None

    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def write_last_session(
    status: str,
    task: str = "",
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Write session state to file.

    Args:
        status: Session status (active, completed, crashed)
        task: Current task description
        metadata: Additional metadata

    Returns:
        True if successful
    """
    session_data = {
        "status": status,
        "task": task,
        "timestamp": datetime.now().isoformat(),
        "pid": None,  # Could be os.getpid() if needed
    }

    if metadata:
        session_data["metadata"] = metadata

    try:
        # Ensure directory exists
        SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(SESSION_FILE, "w") as f:
            json.dump(session_data, f, indent=2)
        return True
    except IOError:
        return False


def is_crash_detected() -> bool:
    """
    Check if the last session appears to have crashed.

    A crash is detected if:
    - Session file exists
    - Status is "active" (not properly closed)

    Returns:
        True if crash detected
    """
    session = read_last_session()
    if not session:
        return False

    return session.get("status") == "active"


def get_crash_info() -> Optional[Dict[str, Any]]:
    """
    Get information about a detected crash.

    Returns:
        Crash info dictionary or None if no crash
    """
    if not is_crash_detected():
        return None

    session = read_last_session()
    if not session:
        return None

    return {
        "task": session.get("task", "Unknown task"),
        "timestamp": session.get("timestamp", "Unknown time"),
        "metadata": session.get("metadata", {}),
    }


def clear_session() -> bool:
    """
    Clear the session file (mark as completed).

    Returns:
        True if successful
    """
    return write_last_session("completed", "Session closed normally")


def mark_session_active(task: str = "") -> bool:
    """
    Mark session as active (starting work).

    Args:
        task: Description of current task

    Returns:
        True if successful
    """
    return write_last_session("active", task)


def mark_session_completed(summary: str = "") -> bool:
    """
    Mark session as completed successfully.

    Args:
        summary: Session summary

    Returns:
        True if successful
    """
    return write_last_session(
        "completed",
        summary,
        metadata={"completed_at": datetime.now().isoformat()}
    )


def get_session_duration() -> Optional[int]:
    """
    Get the duration of the current/last session in seconds.

    Returns:
        Duration in seconds or None if can't calculate
    """
    session = read_last_session()
    if not session or "timestamp" not in session:
        return None

    try:
        start_time = datetime.fromisoformat(session["timestamp"])
        duration = datetime.now() - start_time
        return int(duration.total_seconds())
    except (ValueError, TypeError):
        return None


def update_session_task(task: str) -> bool:
    """
    Update the current task without changing status.

    Args:
        task: New task description

    Returns:
        True if successful
    """
    session = read_last_session()
    if not session:
        return mark_session_active(task)

    return write_last_session(
        session.get("status", "active"),
        task,
        session.get("metadata")
    )
