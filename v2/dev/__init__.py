"""Unified dev-only entrypoints for the experimental RetroFX 2.x platform."""

from .smoke import run_smoke_workflow
from .status import (
    COMMAND_SUMMARY,
    IMPLEMENTED_STATUS_MATRIX,
    PLATFORM_IMPLEMENTATION_INFO,
    build_platform_status,
)

__all__ = [
    "COMMAND_SUMMARY",
    "IMPLEMENTED_STATUS_MATRIX",
    "PLATFORM_IMPLEMENTATION_INFO",
    "build_platform_status",
    "run_smoke_workflow",
]
