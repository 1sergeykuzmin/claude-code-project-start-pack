"""
Result dataclasses for structured task and protocol outputs.

TaskResult: Individual task execution result
ProtocolResult: Aggregated protocol execution result
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Any, Dict
from enum import Enum
import json


class TaskStatus(Enum):
    """Task execution status."""
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"


class ProtocolStatus(Enum):
    """Protocol execution status."""
    SUCCESS = "success"
    ERROR = "error"
    USER_INPUT_REQUIRED = "user_input_required"


@dataclass
class TaskResult:
    """
    Result of a single task execution.

    Attributes:
        name: Task identifier
        status: Execution status (success/error/skipped)
        duration_ms: Execution time in milliseconds
        data: Optional task-specific data
        error: Error message if status is error
    """
    name: str
    status: TaskStatus
    duration_ms: int = 0
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "name": self.name,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
        }
        if self.data is not None:
            result["data"] = self.data
        if self.error is not None:
            result["error"] = self.error
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def create_success(cls, name: str, duration_ms: int = 0, data: Optional[Dict[str, Any]] = None) -> "TaskResult":
        """Create a successful task result."""
        return cls(name=name, status=TaskStatus.SUCCESS, duration_ms=duration_ms, data=data, error=None)

    @classmethod
    def create_error(cls, name: str, error_msg: str, duration_ms: int = 0) -> "TaskResult":
        """Create an error task result."""
        return cls(name=name, status=TaskStatus.ERROR, duration_ms=duration_ms, data=None, error=error_msg)

    @classmethod
    def create_skipped(cls, name: str, reason: str = "") -> "TaskResult":
        """Create a skipped task result."""
        return cls(name=name, status=TaskStatus.SKIPPED, duration_ms=0, data={"reason": reason} if reason else None, error=None)


@dataclass
class ProtocolResult:
    """
    Aggregated result of a protocol execution.

    Attributes:
        protocol: Protocol name (cold-start, completion)
        status: Overall execution status
        tasks: List of individual task results
        total_duration_ms: Total execution time
        user_prompt: Optional prompt for user input (when status is user_input_required)
        summary: Optional summary message
    """
    protocol: str
    status: ProtocolStatus
    tasks: List[TaskResult] = field(default_factory=list)
    total_duration_ms: int = 0
    user_prompt: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "protocol": self.protocol,
            "status": self.status.value,
            "tasks": [t.to_dict() for t in self.tasks],
            "total_duration_ms": self.total_duration_ms,
        }
        if self.user_prompt is not None:
            result["user_prompt"] = self.user_prompt
        if self.summary is not None:
            result["summary"] = self.summary
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @property
    def success_count(self) -> int:
        """Count of successful tasks."""
        return sum(1 for t in self.tasks if t.status == TaskStatus.SUCCESS)

    @property
    def error_count(self) -> int:
        """Count of failed tasks."""
        return sum(1 for t in self.tasks if t.status == TaskStatus.ERROR)

    @property
    def skipped_count(self) -> int:
        """Count of skipped tasks."""
        return sum(1 for t in self.tasks if t.status == TaskStatus.SKIPPED)

    def add_task(self, task: TaskResult) -> None:
        """Add a task result."""
        self.tasks.append(task)
        self.total_duration_ms += task.duration_ms

    def get_errors(self) -> List[TaskResult]:
        """Get all error tasks."""
        return [t for t in self.tasks if t.status == TaskStatus.ERROR]

    @classmethod
    def success(cls, protocol: str, tasks: List[TaskResult], summary: Optional[str] = None) -> "ProtocolResult":
        """Create a successful protocol result."""
        total_ms = sum(t.duration_ms for t in tasks)
        return cls(
            protocol=protocol,
            status=ProtocolStatus.SUCCESS,
            tasks=tasks,
            total_duration_ms=total_ms,
            summary=summary
        )

    @classmethod
    def error(cls, protocol: str, tasks: List[TaskResult], summary: Optional[str] = None) -> "ProtocolResult":
        """Create an error protocol result."""
        total_ms = sum(t.duration_ms for t in tasks)
        return cls(
            protocol=protocol,
            status=ProtocolStatus.ERROR,
            tasks=tasks,
            total_duration_ms=total_ms,
            summary=summary
        )

    @classmethod
    def user_input_required(cls, protocol: str, tasks: List[TaskResult], prompt: str) -> "ProtocolResult":
        """Create a protocol result requiring user input."""
        total_ms = sum(t.duration_ms for t in tasks)
        return cls(
            protocol=protocol,
            status=ProtocolStatus.USER_INPUT_REQUIRED,
            tasks=tasks,
            total_duration_ms=total_ms,
            user_prompt=prompt
        )
