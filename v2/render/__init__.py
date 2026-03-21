"""Render-policy helpers for the experimental RetroFX 2.x scaffold."""

from .policy import DISPLAY_DEFAULTS, build_display_policy_summary, has_non_default_display_policy
from .x11 import SUPPORTED_X11_PALETTE_KINDS, build_x11_render_summary, compositor_required_for_render

__all__ = [
    "DISPLAY_DEFAULTS",
    "SUPPORTED_X11_PALETTE_KINDS",
    "build_display_policy_summary",
    "build_x11_render_summary",
    "compositor_required_for_render",
    "has_non_default_display_policy",
]
