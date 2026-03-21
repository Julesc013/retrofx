"""End-to-end dev-only pipeline for the initial 2.x core scaffold."""

from __future__ import annotations

from pathlib import Path

from v2.core.load import ProfileLoadError, load_profile_document
from v2.core.models.types import Issue, PipelineResult
from v2.core.normalization.normalize import normalize_profile
from v2.core.resolution.resolve import build_resolved_profile
from v2.core.validation.validator import validate_normalized_profile, validate_raw_profile

IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-08",
    "language": "python3-stdlib",
    "why_python": "Python stdlib tomllib provides deterministic TOML parsing without adding dependencies or touching the 1.x shell runtime.",
    "implemented_stages": ["load", "validate", "normalize", "resolve"],
    "not_implemented": [
        "capability filtering",
        "target planning",
        "artifact planning",
        "target emission",
        "session orchestration",
        "production CLI integration",
    ],
}


def run_profile_pipeline(path: str | Path) -> PipelineResult:
    source_path = str(Path(path).expanduser())

    try:
        raw_profile = load_profile_document(path)
    except ProfileLoadError as exc:
        return PipelineResult(
            ok=False,
            stage="load",
            implementation=IMPLEMENTATION_INFO,
            source={"requested_path": source_path},
            warnings=[],
            errors=[exc.issue],
            normalized_profile=None,
            resolved_profile=None,
        )

    raw_errors, raw_warnings = validate_raw_profile(raw_profile)
    if raw_errors:
        return PipelineResult(
            ok=False,
            stage="validation",
            implementation=IMPLEMENTATION_INFO,
            source={"profile_path": raw_profile.source_path, "profile_dir": raw_profile.source_dir},
            warnings=raw_warnings,
            errors=raw_errors,
            normalized_profile=None,
            resolved_profile=None,
        )

    normalized = normalize_profile(raw_profile)
    normalized_errors, normalized_warnings = validate_normalized_profile(normalized)
    warnings = raw_warnings + normalized_warnings
    errors = normalized_errors

    if errors:
        return PipelineResult(
            ok=False,
            stage="validation",
            implementation=IMPLEMENTATION_INFO,
            source={"profile_path": raw_profile.source_path, "profile_dir": raw_profile.source_dir},
            warnings=warnings,
            errors=errors,
            normalized_profile=normalized.data,
            resolved_profile=None,
        )

    resolved = build_resolved_profile(normalized, warnings)
    return PipelineResult(
        ok=True,
        stage="resolution",
        implementation=IMPLEMENTATION_INFO,
        source={"profile_path": raw_profile.source_path, "profile_dir": raw_profile.source_dir},
        warnings=warnings,
        errors=[],
        normalized_profile=normalized.data,
        resolved_profile=resolved.data,
    )

