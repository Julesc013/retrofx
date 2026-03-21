"""Compatibility and migration helpers for the experimental RetroFX 2.x scaffold."""

from .legacy import LegacyProfileError, load_legacy_profile_document, normalize_legacy_profile
from .migration import DEFAULT_MIGRATION_OUT_ROOT, LEGACY_TO_V2_RULES, inspect_legacy_profile

__all__ = [
    "DEFAULT_MIGRATION_OUT_ROOT",
    "LEGACY_TO_V2_RULES",
    "LegacyProfileError",
    "inspect_legacy_profile",
    "load_legacy_profile_document",
    "normalize_legacy_profile",
]
