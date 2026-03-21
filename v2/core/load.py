"""Profile loading primitives for the experimental RetroFX 2.x core."""

from __future__ import annotations

from pathlib import Path
import tomllib

from v2.core.models.types import Issue, RawProfile


class ProfileLoadError(Exception):
    """Raised when a 2.x profile cannot be loaded."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(issue.message)
        self.issue = issue


def load_profile_document(path: str | Path, *, origin: dict[str, object] | None = None) -> RawProfile:
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        raise ProfileLoadError(
            Issue(
                severity="error",
                code="load-path-missing",
                message=f"Profile path does not exist or is not a file: {candidate}",
                path="source",
            )
        )

    resolved_path = candidate.resolve()
    try:
        with resolved_path.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ProfileLoadError(
            Issue(
                severity="error",
                code="toml-parse-error",
                message=str(exc),
                path="source",
            )
        ) from exc

    if not isinstance(data, dict):
        raise ProfileLoadError(
            Issue(
                severity="error",
                code="invalid-document",
                message="Loaded profile root is not a TOML table.",
                path="source",
            )
        )

    return RawProfile(
        source_path=str(resolved_path),
        source_dir=str(resolved_path.parent),
        origin=_normalize_origin(origin, resolved_path),
        data=data,
    )


def _normalize_origin(origin: dict[str, object] | None, resolved_path: Path) -> dict[str, object]:
    if origin is None:
        return {
            "type": "standalone",
            "profile_path": str(resolved_path),
            "profile_dir": str(resolved_path.parent),
        }

    normalized = dict(origin)
    normalized.setdefault("type", "standalone")
    normalized.setdefault("profile_path", str(resolved_path))
    normalized.setdefault("profile_dir", str(resolved_path.parent))
    return normalized
