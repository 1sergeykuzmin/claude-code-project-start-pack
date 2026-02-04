#!/usr/bin/env python3
"""
Claude Code Project Framework Core - CLI Entry Point

Fast parallel execution engine for framework protocols.
Requires Python 3.8+

Usage:
    python main.py cold-start [--silent] [--json]
    python main.py completion [--silent] [--json]
    python main.py --version

Exit Codes:
    0 = success
    1 = error
    2 = user_input_required
"""

import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from commands.cold_start import run_cold_start
from commands.completion import run_completion
from utils.result import ProtocolStatus
from utils.logger import setup_logging

__version__ = "2.0.0"


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="framework-core",
        description="Claude Code Project Framework Core - Parallel Protocol Engine",
        epilog="For more information, see the documentation at .claude/README.md"
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--silent", "-s",
        action="store_true",
        help="Silent mode - suppress all output except errors"
    )

    parser.add_argument(
        "--json", "-j",
        action="store_true",
        default=True,
        help="Output as JSON (default)"
    )

    parser.add_argument(
        "--pretty", "-p",
        action="store_true",
        help="Pretty-print JSON output"
    )

    parser.add_argument(
        "--log-dir",
        type=str,
        default=".claude/logs",
        help="Log directory (default: .claude/logs)"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available protocol commands"
    )

    # Cold start command
    cold_start_parser = subparsers.add_parser(
        "cold-start",
        help="Run cold start protocol (10 parallel initialization tasks)"
    )
    cold_start_parser.add_argument(
        "--skip-update",
        action="store_true",
        help="Skip version update check"
    )
    cold_start_parser.add_argument(
        "--skip-security",
        action="store_true",
        help="Skip security scan (not recommended)"
    )

    # Completion command
    completion_parser = subparsers.add_parser(
        "completion",
        help="Run completion protocol (finalize session)"
    )
    completion_parser.add_argument(
        "--skip-review",
        action="store_true",
        help="Skip code review (not recommended, breaks security invariant)"
    )
    completion_parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip automatic commit"
    )
    completion_parser.add_argument(
        "--message", "-m",
        type=str,
        help="Custom commit message"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show current framework status"
    )

    return parser


def output_result(result, pretty: bool = False, silent: bool = False) -> int:
    """
    Output the result and return appropriate exit code.

    Args:
        result: ProtocolResult object
        pretty: Pretty-print JSON
        silent: Suppress output

    Returns:
        Exit code (0=success, 1=error, 2=user_input_required)
    """
    # Determine exit code
    if result.status == ProtocolStatus.SUCCESS:
        exit_code = 0
    elif result.status == ProtocolStatus.USER_INPUT_REQUIRED:
        exit_code = 2
    else:
        exit_code = 1

    # Output result
    if not silent or result.status != ProtocolStatus.SUCCESS:
        json_output = result.to_json() if pretty else json.dumps(result.to_dict())
        print(json_output)

    return exit_code


def run_status() -> dict:
    """Get current framework status."""
    from tasks.config import read_framework_config, get_active_preset
    from tasks.session import read_last_session, is_crash_detected
    from tasks.version import get_current_version, is_update_available
    from tasks.hooks import verify_all_hooks

    return {
        "version": get_current_version(),
        "update_available": is_update_available(),
        "preset": get_active_preset(),
        "crash_detected": is_crash_detected(),
        "last_session": read_last_session(),
        "hooks": verify_all_hooks(),
        "config": read_framework_config(),
    }


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    setup_logging(
        log_dir=args.log_dir,
        silent_mode=args.silent
    )

    # Handle no command
    if not args.command:
        parser.print_help()
        return 0

    # Execute command
    try:
        if args.command == "cold-start":
            result = run_cold_start(
                skip_update=args.skip_update,
                skip_security=args.skip_security,
                silent=args.silent
            )
            return output_result(result, args.pretty, args.silent)

        elif args.command == "completion":
            result = run_completion(
                skip_review=args.skip_review,
                no_commit=args.no_commit,
                commit_message=args.message,
                silent=args.silent
            )
            return output_result(result, args.pretty, args.silent)

        elif args.command == "status":
            status = run_status()
            if args.pretty:
                print(json.dumps(status, indent=2))
            else:
                print(json.dumps(status))
            return 0

        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130

    except Exception as e:
        error_output = {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__
        }
        print(json.dumps(error_output), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
