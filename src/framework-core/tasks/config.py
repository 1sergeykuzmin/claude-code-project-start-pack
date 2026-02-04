"""
Configuration and preset management tasks.

Handles reading/writing .framework-config and settings.json.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

# Default paths
FRAMEWORK_CONFIG_PATH = Path(".claude/.framework-config")
SETTINGS_PATH = Path(".claude/settings.json")
PRESETS_PATH = Path(".claude/presets.json")

# Default configuration
DEFAULT_FRAMEWORK_CONFIG = {
    "project_id": "",
    "framework_version": "2.0.0",
    "first_run_completed": False,
    "consent_version": "",
    "last_update_check": "",
    "active_preset": "verbose",
    "python_detected": True,
}

DEFAULT_SETTINGS = {
    "framework": {"version": "2.0.0"},
    "preset": "verbose",
    "execution": {
        "mode": "verbose",
        "parallelism": True,
        "pythonPath": "auto"
    },
}


def read_framework_config() -> Dict[str, Any]:
    """
    Read the framework configuration file.

    Returns:
        Configuration dictionary (defaults if file doesn't exist)
    """
    if not FRAMEWORK_CONFIG_PATH.exists():
        return DEFAULT_FRAMEWORK_CONFIG.copy()

    try:
        with open(FRAMEWORK_CONFIG_PATH, "r") as f:
            config = json.load(f)
            # Merge with defaults for missing keys
            return {**DEFAULT_FRAMEWORK_CONFIG, **config}
    except (json.JSONDecodeError, IOError):
        return DEFAULT_FRAMEWORK_CONFIG.copy()


def write_framework_config(config: Dict[str, Any]) -> bool:
    """
    Write the framework configuration file.

    Args:
        config: Configuration dictionary to write

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        FRAMEWORK_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(FRAMEWORK_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError:
        return False


def get_active_preset() -> str:
    """
    Get the currently active preset.

    Returns:
        Preset name (default: "verbose")
    """
    # First check framework config
    config = read_framework_config()
    if config.get("active_preset"):
        return config["active_preset"]

    # Fall back to settings.json
    settings = read_settings()
    return settings.get("preset", "verbose")


def set_active_preset(preset: str) -> bool:
    """
    Set the active preset.

    Args:
        preset: Preset name (paranoid, balanced, autopilot, verbose, silent)

    Returns:
        True if successful
    """
    valid_presets = {"paranoid", "balanced", "autopilot", "verbose", "silent"}
    if preset not in valid_presets:
        return False

    config = read_framework_config()
    config["active_preset"] = preset
    return write_framework_config(config)


def read_settings() -> Dict[str, Any]:
    """
    Read settings.json.

    Returns:
        Settings dictionary (defaults if file doesn't exist)
    """
    if not SETTINGS_PATH.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
            return settings
    except (json.JSONDecodeError, IOError):
        return DEFAULT_SETTINGS.copy()


def get_setting(key: str, default: Any = None) -> Any:
    """
    Get a specific setting value using dot notation.

    Args:
        key: Setting key (e.g., "execution.parallelism")
        default: Default value if key not found

    Returns:
        Setting value or default
    """
    settings = read_settings()
    keys = key.split(".")

    value = settings
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value


def get_preset_config(preset_name: str) -> Optional[Dict[str, Any]]:
    """
    Get the configuration for a specific preset.

    Args:
        preset_name: Name of the preset

    Returns:
        Preset configuration dictionary or None if not found
    """
    if not PRESETS_PATH.exists():
        return None

    try:
        with open(PRESETS_PATH, "r") as f:
            presets = json.load(f)
            return presets.get("presets", {}).get(preset_name)
    except (json.JSONDecodeError, IOError):
        return None


def is_silent_mode() -> bool:
    """Check if the current preset uses silent mode."""
    preset = get_active_preset()
    return preset in ("silent", "autopilot")


def is_parallelism_enabled() -> bool:
    """Check if parallel execution is enabled."""
    return get_setting("execution.parallelism", True)


def get_python_path() -> str:
    """Get the configured Python path."""
    path = get_setting("execution.pythonPath", "auto")
    if path == "auto":
        import sys
        return sys.executable
    return path
