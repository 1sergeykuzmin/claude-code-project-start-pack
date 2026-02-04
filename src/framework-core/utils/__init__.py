"""
Framework utilities module.

Utilities:
- parallel: ThreadPoolExecutor wrapper for parallel task execution
- logger: JSON-based structured logging
- result: TaskResult and ProtocolResult dataclasses
"""

from .parallel import run_tasks_parallel, time_task
from .logger import log_task, setup_logging
from .result import TaskResult, ProtocolResult

__all__ = [
    "run_tasks_parallel", "time_task",
    "log_task", "setup_logging",
    "TaskResult", "ProtocolResult",
]
