"""
Version checking and update tasks.

Handles framework version management and update detection.
"""

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Tuple
from packaging import version as pkg_version

# Version info
CURRENT_VERSION = "2.0.0"

# Paths
FRAMEWORK_CONFIG = Path(".claude/.framework-config")
SETTINGS_PATH = Path(".claude/settings.json")

# GitHub release URL (placeholder - would be real repo)
GITHUB_RELEASES_URL = "https://api.github.com/repos/user/claude-code-project-start-pack/releases/latest"


def get_current_version() -> str:
    """
    Get the current framework version.

    Checks in order:
    1. .framework-config
    2. settings.json
    3. Falls back to hardcoded version

    Returns:
        Version string
    """
    # Check framework config first
    if FRAMEWORK_CONFIG.exists():
        try:
            with open(FRAMEWORK_CONFIG, "r") as f:
                config = json.load(f)
                if "framework_version" in config:
                    return config["framework_version"]
        except (json.JSONDecodeError, IOError):
            pass

    # Check settings.json
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
                version = settings.get("framework", {}).get("version")
                if version:
                    return version
        except (json.JSONDecodeError, IOError):
            pass

    return CURRENT_VERSION


def get_latest_version() -> Optional[str]:
    """
    Get the latest available version from GitHub releases.

    Returns:
        Latest version string or None if can't fetch
    """
    try:
        req = urllib.request.Request(
            GITHUB_RELEASES_URL,
            headers={"Accept": "application/vnd.github.v3+json"}
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            tag_name = data.get("tag_name", "")

            # Remove 'v' prefix if present
            if tag_name.startswith("v"):
                tag_name = tag_name[1:]

            return tag_name if tag_name else None

    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        return None


def is_update_available() -> bool:
    """
    Check if a newer version is available.

    Returns:
        True if update available
    """
    current = get_current_version()
    latest = get_latest_version()

    if not latest:
        return False

    try:
        return pkg_version.parse(latest) > pkg_version.parse(current)
    except Exception:
        # Fall back to string comparison
        return latest > current


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two version strings.

    Args:
        v1: First version
        v2: Second version

    Returns:
        -1 if v1 < v2, 0 if equal, 1 if v1 > v2
    """
    try:
        pv1 = pkg_version.parse(v1)
        pv2 = pkg_version.parse(v2)

        if pv1 < pv2:
            return -1
        elif pv1 > pv2:
            return 1
        else:
            return 0
    except Exception:
        # Fall back to string comparison
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0


def get_update_info() -> Optional[dict]:
    """
    Get detailed update information.

    Returns:
        Dictionary with update details or None if no update
    """
    current = get_current_version()
    latest = get_latest_version()

    if not latest or not is_update_available():
        return None

    return {
        "current_version": current,
        "latest_version": latest,
        "update_available": True,
    }


def update_version_in_config(new_version: str) -> bool:
    """
    Update the version in framework config.

    Args:
        new_version: New version string

    Returns:
        True if successful
    """
    config = {}

    if FRAMEWORK_CONFIG.exists():
        try:
            with open(FRAMEWORK_CONFIG, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    config["framework_version"] = new_version

    try:
        FRAMEWORK_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with open(FRAMEWORK_CONFIG, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError:
        return False


def download_update(version: str) -> bool:
    """
    Download and install a framework update.

    Note: This is a placeholder - actual implementation would
    download release assets and apply them.

    Args:
        version: Version to download

    Returns:
        True if successful
    """
    # Placeholder - would implement actual download logic
    # For now, just update the version number
    return update_version_in_config(version)


def check_version_compatibility() -> Tuple[bool, str]:
    """
    Check if current Python version is compatible.

    Returns:
        Tuple of (is_compatible, message)
    """
    import sys

    min_version = (3, 8)
    current = (sys.version_info.major, sys.version_info.minor)

    if current >= min_version:
        return True, f"Python {sys.version_info.major}.{sys.version_info.minor} is compatible"
    else:
        return False, f"Python {min_version[0]}.{min_version[1]}+ required, found {current[0]}.{current[1]}"
