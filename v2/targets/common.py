"""Shared helpers for early 2.x target compilers."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetArtifact


def require_mapping(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = container.get(key)
    if not isinstance(value, Mapping):
        raise KeyError(f"Resolved profile is missing required mapping `{key}`.")
    return value


def has_non_default_display_policy(display: Mapping[str, Any]) -> bool:
    return any(
        (
            display.get("gamma", 1.0) != 1.0,
            display.get("contrast", 1.0) != 1.0,
            display.get("temperature", 6500) != 6500,
            display.get("black_lift", 0.0) != 0.0,
            display.get("blue_light_reduction", 0.0) != 0.0,
            display.get("tint_bias") is not None,
        )
    )


def has_non_default_typography_aa(policy: Mapping[str, Any]) -> bool:
    return any(
        (
            policy.get("antialias", "default") != "default",
            policy.get("subpixel", "default") != "default",
            policy.get("hinting", "default") != "default",
        )
    )


def write_target_artifact(
    *,
    target_name: str,
    output_dir: Path,
    file_name: str,
    content: str,
) -> TargetArtifact:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / file_name
    output_path.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    relative_path = f"{target_name}/{file_name}"
    return TargetArtifact(
        target_name=target_name,
        file_name=file_name,
        relative_path=relative_path,
        output_path=str(output_path),
        content_sha256=digest,
        byte_count=len(content.encode("utf-8")),
    )
