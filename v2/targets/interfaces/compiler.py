"""Shared target compiler interfaces for the early 2.x implementation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol


@dataclass(slots=True)
class TargetArtifact:
    target_name: str
    file_name: str
    relative_path: str
    output_path: str
    content_sha256: str
    byte_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TargetCompileResult:
    target_name: str
    family_name: str
    mode: str
    output_dir: str
    artifacts: list[TargetArtifact]
    consumed_sections: list[str]
    ignored_sections: list[str]
    warnings: list[str]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["artifacts"] = [artifact.to_dict() for artifact in self.artifacts]
        return payload


class TargetCompiler(Protocol):
    target_name: str
    family_name: str
    output_file_name: str
    supported_target_classes: tuple[str, ...]

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        """Emit deterministic artifacts for a resolved profile."""
