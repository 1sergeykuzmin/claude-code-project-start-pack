"""
Parallel task execution utilities.

Uses ThreadPoolExecutor for concurrent task execution with
structured error handling and timing.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from typing import Callable, List, Dict, Any, Optional, Tuple
from functools import wraps
from dataclasses import dataclass

from .result import TaskResult, TaskStatus


@dataclass
class TaskDefinition:
    """
    Definition of a task to be executed.

    Attributes:
        name: Task identifier
        func: Callable to execute
        args: Positional arguments
        kwargs: Keyword arguments
    """
    name: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


def time_task(func: Callable) -> Callable:
    """
    Decorator to time task execution.

    Returns a tuple of (result, duration_ms).
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, int]:
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration_ms = int((time.perf_counter() - start) * 1000)
            return result, duration_ms
        except Exception as e:
            duration_ms = int((time.perf_counter() - start) * 1000)
            raise TaskExecutionError(str(e), duration_ms) from e
    return wrapper


class TaskExecutionError(Exception):
    """Exception raised during task execution with timing info."""
    def __init__(self, message: str, duration_ms: int = 0):
        super().__init__(message)
        self.duration_ms = duration_ms


def _execute_task(task: TaskDefinition) -> TaskResult:
    """
    Execute a single task and return its result.

    Handles exceptions and timing internally.
    """
    start = time.perf_counter()
    try:
        result = task.func(*task.args, **task.kwargs)
        duration_ms = int((time.perf_counter() - start) * 1000)

        # If the function returns a TaskResult, use it
        if isinstance(result, TaskResult):
            result.duration_ms = duration_ms
            return result

        # Otherwise, wrap the result
        return TaskResult.create_success(
            name=task.name,
            duration_ms=duration_ms,
            data={"result": result} if result is not None else None
        )
    except TaskExecutionError as e:
        return TaskResult.create_error(
            name=task.name,
            error=str(e),
            duration_ms=e.duration_ms
        )
    except Exception as e:
        duration_ms = int((time.perf_counter() - start) * 1000)
        return TaskResult.create_error(
            name=task.name,
            error=str(e),
            duration_ms=duration_ms
        )


def run_tasks_parallel(
    tasks: List[TaskDefinition],
    max_workers: int = 10,
    fail_fast: bool = False
) -> List[TaskResult]:
    """
    Execute tasks in parallel using ThreadPoolExecutor.

    Args:
        tasks: List of TaskDefinition objects to execute
        max_workers: Maximum concurrent workers (default: 10)
        fail_fast: If True, stop on first error (default: False)

    Returns:
        List of TaskResult objects in completion order

    Example:
        tasks = [
            TaskDefinition("task1", func1, args=(arg1,)),
            TaskDefinition("task2", func2, kwargs={"key": "value"}),
        ]
        results = run_tasks_parallel(tasks, max_workers=5)
    """
    results: List[TaskResult] = []

    if not tasks:
        return results

    with ThreadPoolExecutor(max_workers=min(max_workers, len(tasks))) as executor:
        # Submit all tasks
        future_to_task: Dict[Future, TaskDefinition] = {
            executor.submit(_execute_task, task): task
            for task in tasks
        }

        # Collect results as they complete
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results.append(result)

                # Check for fail_fast
                if fail_fast and result.status == TaskStatus.ERROR:
                    # Cancel remaining futures
                    for f in future_to_task:
                        f.cancel()
                    break

            except Exception as e:
                # This shouldn't happen as _execute_task catches exceptions
                results.append(TaskResult.create_error(
                    name=task.name,
                    error=f"Unexpected error: {str(e)}",
                    duration_ms=0
                ))

    return results


def run_tasks_sequential(tasks: List[TaskDefinition]) -> List[TaskResult]:
    """
    Execute tasks sequentially (for tasks that must run in order).

    Args:
        tasks: List of TaskDefinition objects to execute in order

    Returns:
        List of TaskResult objects in execution order
    """
    results: List[TaskResult] = []

    for task in tasks:
        result = _execute_task(task)
        results.append(result)

        # Stop on error for sequential tasks
        if result.status == TaskStatus.ERROR:
            # Mark remaining tasks as skipped
            for remaining_task in tasks[len(results):]:
                results.append(TaskResult.create_skipped(
                    name=remaining_task.name,
                    reason=f"Skipped due to error in {task.name}"
                ))
            break

    return results
