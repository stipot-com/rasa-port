"""No-op telemetry shim for the AdaOS NLU-only port.

The upstream Rasa package reports product telemetry. AdaOS embeds this code as a
local NLU runtime, so telemetry is intentionally disabled at the source boundary.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


@contextmanager
def track_model_training(*_: Any, **__: Any) -> Iterator[None]:
    """Keep the upstream training call sites while emitting no telemetry."""
    yield


def initialize_telemetry(*_: Any, **__: Any) -> None:
    """Disable upstream telemetry initialization."""
    return None


def initialize_error_reporting(*_: Any, **__: Any) -> None:
    """Disable upstream error reporting initialization."""
    return None


def is_telemetry_enabled() -> bool:
    """Report that telemetry is disabled for this port."""
    return False


def __getattr__(name: str) -> Any:
    """Return no-op functions for remaining upstream telemetry hooks."""
    if name.startswith(("track_", "initialize_", "telemetry_")):
        return _noop
    raise AttributeError(name)


def _noop(*_: Any, **__: Any) -> None:
    return None

