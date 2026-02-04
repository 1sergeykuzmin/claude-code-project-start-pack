"""
Security scanning tasks.

Handles credential detection and security scans.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# Credential patterns to detect
CREDENTIAL_PATTERNS = [
    # API Keys
    (r"sk-[a-zA-Z0-9]{32,}", "api_key", "CRITICAL"),
    (r"sk_live_[a-zA-Z0-9]+", "stripe_key", "CRITICAL"),
    (r"sk_test_[a-zA-Z0-9]+", "stripe_test_key", "HIGH"),
    (r"pk_live_[a-zA-Z0-9]+", "stripe_key", "CRITICAL"),
    (r"pk_test_[a-zA-Z0-9]+", "stripe_test_key", "HIGH"),

    # GitHub tokens
    (r"ghp_[a-zA-Z0-9]{36}", "github_token", "CRITICAL"),
    (r"gho_[a-zA-Z0-9]{36}", "github_oauth", "CRITICAL"),
    (r"ghu_[a-zA-Z0-9]{36}", "github_user_token", "CRITICAL"),
    (r"ghs_[a-zA-Z0-9]{36}", "github_server_token", "CRITICAL"),

    # AWS
    (r"AKIA[0-9A-Z]{16}", "aws_access_key", "CRITICAL"),

    # Generic patterns
    (r'password\s*[:=]\s*["\'][^"\']+["\']', "hardcoded_password", "HIGH"),
    (r'api_key\s*[:=]\s*["\'][^"\']+["\']', "hardcoded_api_key", "HIGH"),
    (r'secret\s*[:=]\s*["\'][^"\']+["\']', "hardcoded_secret", "HIGH"),
    (r'token\s*[:=]\s*["\'][^"\']+["\']', "hardcoded_token", "HIGH"),
    (r'private_key\s*[:=]\s*["\'][^"\']+["\']', "hardcoded_private_key", "CRITICAL"),
]

# File patterns to scan
SCANNABLE_EXTENSIONS = {
    ".js", ".ts", ".py", ".java", ".go", ".rb", ".php",
    ".json", ".yaml", ".yml", ".xml", ".conf", ".config",
    ".env", ".sh", ".bash"
}

# Paths to exclude
EXCLUDED_PATHS = {
    "node_modules", ".git", "venv", ".venv", "__pycache__",
    "dist", "build", ".next", "coverage", "security/reports"
}


def quick_scan() -> Dict[str, Any]:
    """
    Run a quick security scan on recent changes.

    Scans only staged and modified files for credential patterns.

    Returns:
        Dictionary with findings by severity
    """
    from .git import get_status

    findings = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "scanned_files": 0,
        "total_findings": 0,
    }

    status = get_status()
    files_to_scan = status.get("staged", []) + status.get("unstaged", [])

    for file_path in files_to_scan:
        path = Path(file_path)
        if not path.exists() or path.suffix not in SCANNABLE_EXTENSIONS:
            continue

        file_findings = scan_file(path)
        findings["scanned_files"] += 1

        for finding in file_findings:
            severity = finding["severity"]
            findings[severity].append(finding)
            findings["total_findings"] += 1

    return findings


def run_initial_scan() -> Dict[str, Any]:
    """
    Run a comprehensive security scan on the entire project.

    Returns:
        Dictionary with all findings and summary
    """
    findings = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "env_files": [],
        "credential_files": [],
        "scanned_files": 0,
        "total_findings": 0,
    }

    project_root = Path(".")

    # Check for .env files
    for env_file in project_root.glob("**/.env*"):
        if should_exclude_path(env_file):
            continue
        if env_file.name not in (".env.example", ".env.template"):
            findings["env_files"].append(str(env_file))
            findings["CRITICAL"].append({
                "file": str(env_file),
                "type": "env_file",
                "severity": "CRITICAL",
                "description": ".env file detected",
            })
            findings["total_findings"] += 1

    # Check for credential files by name
    credential_patterns = [
        "*credentials*", "*secret*", "*password*",
        "*.pem", "*.key", "*token*",
        "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
        "*.p12", "*.pfx", "*.jks"
    ]

    for pattern in credential_patterns:
        for cred_file in project_root.glob(f"**/{pattern}"):
            if should_exclude_path(cred_file) or cred_file.is_dir():
                continue
            findings["credential_files"].append(str(cred_file))
            findings["HIGH"].append({
                "file": str(cred_file),
                "type": "credential_file",
                "severity": "HIGH",
                "description": f"Potential credential file: {cred_file.name}",
            })
            findings["total_findings"] += 1

    # Scan source files for hardcoded secrets
    for path in project_root.rglob("*"):
        if path.is_dir() or should_exclude_path(path):
            continue
        if path.suffix not in SCANNABLE_EXTENSIONS:
            continue

        file_findings = scan_file(path)
        findings["scanned_files"] += 1

        for finding in file_findings:
            severity = finding["severity"]
            findings[severity].append(finding)
            findings["total_findings"] += 1

    # Check .gitignore
    gitignore_findings = check_gitignore()
    findings["MEDIUM"].extend(gitignore_findings)
    findings["total_findings"] += len(gitignore_findings)

    return findings


def scan_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Scan a single file for credential patterns.

    Args:
        file_path: Path to the file to scan

    Returns:
        List of findings
    """
    findings = []

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except IOError:
        return findings

    # Check for security: ignore comment
    if "security: ignore" in content.lower():
        return findings

    for pattern, cred_type, severity in CREDENTIAL_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            # Get line number
            line_num = content[:match.start()].count("\n") + 1

            findings.append({
                "file": str(file_path),
                "line": line_num,
                "type": cred_type,
                "severity": severity,
                "match": match.group()[:50] + "..." if len(match.group()) > 50 else match.group(),
                "description": f"Potential {cred_type} detected",
            })

    return findings


def should_exclude_path(path: Path) -> bool:
    """Check if a path should be excluded from scanning."""
    path_parts = set(path.parts)
    return bool(path_parts & EXCLUDED_PATHS)


def check_gitignore() -> List[Dict[str, Any]]:
    """
    Check if .gitignore has required security patterns.

    Returns:
        List of findings for missing patterns
    """
    findings = []
    gitignore_path = Path(".gitignore")

    required_patterns = [".env", "*.pem", "*.key", "credentials", "secrets"]

    if not gitignore_path.exists():
        findings.append({
            "file": ".gitignore",
            "type": "missing_gitignore",
            "severity": "MEDIUM",
            "description": "No .gitignore file found",
        })
        return findings

    try:
        content = gitignore_path.read_text()
        for pattern in required_patterns:
            if pattern not in content:
                findings.append({
                    "file": ".gitignore",
                    "type": "missing_pattern",
                    "severity": "MEDIUM",
                    "description": f"Missing security pattern: {pattern}",
                })
    except IOError:
        pass

    return findings


def cleanup_dialogs(dialog_dir: str = "dialog") -> int:
    """
    Redact credentials from dialog export files.

    Args:
        dialog_dir: Directory containing dialog files

    Returns:
        Number of redactions made
    """
    dialog_path = Path(dialog_dir)
    if not dialog_path.exists():
        return 0

    redaction_count = 0
    redact_patterns = [
        (r"sk-[a-zA-Z0-9]{32,}", "[REDACTED_API_KEY]"),
        (r"sk_live_[a-zA-Z0-9]+", "[REDACTED_STRIPE_KEY]"),
        (r"sk_test_[a-zA-Z0-9]+", "[REDACTED_STRIPE_KEY]"),
        (r"ghp_[a-zA-Z0-9]{36}", "[REDACTED_GITHUB_TOKEN]"),
        (r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_KEY]"),
        (r'password\s*[:=]\s*["\'][^"\']+["\']', 'password = "[REDACTED]"'),
        (r'api_key\s*[:=]\s*["\'][^"\']+["\']', 'api_key = "[REDACTED]"'),
        (r"Bearer [a-zA-Z0-9._-]+", "Bearer [REDACTED]"),
        (r"Basic [a-zA-Z0-9+/=]+", "Basic [REDACTED]"),
    ]

    for md_file in dialog_path.glob("**/*.md"):
        try:
            content = md_file.read_text()
            modified = content

            for pattern, replacement in redact_patterns:
                matches = len(re.findall(pattern, modified))
                if matches > 0:
                    modified = re.sub(pattern, replacement, modified)
                    redaction_count += matches

            if modified != content:
                md_file.write_text(modified)

        except IOError:
            continue

    return redaction_count
