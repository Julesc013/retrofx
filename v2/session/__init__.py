"""Session-planning helpers for the experimental RetroFX 2.x scaffold."""

from .environment import detect_environment
from .planning import build_session_plan

__all__ = ["build_session_plan", "detect_environment"]
