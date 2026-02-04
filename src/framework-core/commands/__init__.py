"""
Framework commands module.

Commands:
- cold_start: Initialize session with 10 parallel tasks
- completion: Finalize session with parallel + sequential tasks
"""

from .cold_start import run_cold_start
from .completion import run_completion

__all__ = ["run_cold_start", "run_completion"]
