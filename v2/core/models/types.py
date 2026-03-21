"""Core data shapes for the experimental 2.x pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Issue:
    severity: str
    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(slots=True)
class RawProfile:
    source_path: str
    source_dir: str
    origin: dict[str, Any]
    data: dict[str, Any]


@dataclass(slots=True)
class NormalizationReport:
    derived_semantic_tokens: list[str] = field(default_factory=list)
    derived_terminal_slots: list[str] = field(default_factory=list)
    derived_tty_slots: list[str] = field(default_factory=list)
    derived_typography_roles: list[str] = field(default_factory=list)
    path_normalizations: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class NormalizedProfile:
    data: dict[str, Any]
    report: NormalizationReport


@dataclass(slots=True)
class ResolvedProfile:
    data: dict[str, Any]


@dataclass(slots=True)
class PipelineResult:
    ok: bool
    stage: str
    implementation: dict[str, Any]
    source: dict[str, Any]
    warnings: list[Issue]
    errors: list[Issue]
    normalized_profile: dict[str, Any] | None
    resolved_profile: dict[str, Any] | None

    def to_dict(self, *, include_normalized: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": self.ok,
            "stage": self.stage,
            "implementation": self.implementation,
            "source": self.source,
            "warnings": [warning.to_dict() for warning in self.warnings],
            "errors": [error.to_dict() for error in self.errors],
        }
        if include_normalized and self.normalized_profile is not None:
            payload["normalized_profile"] = self.normalized_profile
        if self.resolved_profile is not None:
            payload["resolved_profile"] = self.resolved_profile
        return payload
