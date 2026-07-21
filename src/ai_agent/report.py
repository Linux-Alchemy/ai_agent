import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunReport:
    """Accumulates what happened during one agent run.

    Tallies tool calls and token usage as the run proceeds, then renders a
    human summary and appends a machine-readable audit line.
    """

    started: float = field(default_factory=time.monotonic)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0

    def record(self, name: str, args: dict[str, Any], result: str) -> None:
        """Append one tool call to the tally.

        Args:
            name: The tool that ran.
            args: The arguments it was called with.
            result: Its return string; ``ok`` is derived from whether this
                starts with ``"Error:"``.
        """
        ...  # TODO 4.2.1: append {name, args, ok} to tool_calls

    def summary(self) -> str:
        """Return the human-readable end-of-run summary."""
        ...  # TODO 4.2.1: tools called, files changed, tokens, elapsed seconds

    def write_audit(self, path: str) -> None:
        """Append the run as one JSON object to a JSONL file.

        Args:
            path: The JSONL file to append one line to.
        """
        ...  # TODO 4.2.1: json.dumps the tally, append one line to path
