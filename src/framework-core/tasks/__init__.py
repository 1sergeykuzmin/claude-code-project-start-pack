"""
Framework tasks module.

Task modules:
- config: Configuration and preset management
- git: Git operations
- hooks: Git hooks management
- security: Security scanning
- session: Session state management
- version: Version checking and updates
"""

from .config import read_framework_config, write_framework_config, get_active_preset, get_setting
from .git import get_status, get_diff_stat, commit, get_recent_commits
from .hooks import is_hook_installed, install_hook, verify_all_hooks
from .security import quick_scan, run_initial_scan, cleanup_dialogs
from .session import read_last_session, write_last_session, is_crash_detected, clear_session
from .version import get_current_version, get_latest_version, is_update_available

__all__ = [
    # config
    "read_framework_config", "write_framework_config", "get_active_preset", "get_setting",
    # git
    "get_status", "get_diff_stat", "commit", "get_recent_commits",
    # hooks
    "is_hook_installed", "install_hook", "verify_all_hooks",
    # security
    "quick_scan", "run_initial_scan", "cleanup_dialogs",
    # session
    "read_last_session", "write_last_session", "is_crash_detected", "clear_session",
    # version
    "get_current_version", "get_latest_version", "is_update_available",
]
