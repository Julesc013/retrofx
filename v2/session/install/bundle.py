"""Deterministic dev bundle generation for the experimental RetroFX 2.x install slice."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from v2.core.dev.profile_input import run_selected_profile_pipeline
from v2.session.environment import detect_environment
from v2.session.planning import build_session_plan
from v2.targets import compile_resolved_profile_targets, list_target_families, list_targets

from .layout import INSTALL_NAME, bundle_root_path, install_root_relative_bundle_dir, install_root_relative_record_path

BUNDLE_SCHEMA = "retrofx.bundle/v2alpha1"
IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-16",
    "surface": "bundle-generation",
    "families": list_target_families(),
    "implemented_targets": list_targets(),
    "mode": "repo-local-bundle-builder",
    "not_implemented": [
        "public release packaging",
        "root/system install",
        "automatic session-default switching",
        "remote distribution and registry integration",
    ],
}


def build_dev_bundle(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    bundle_root: str | Path | None = None,
    target_names: list[str] | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
) -> dict[str, Any]:
    pipeline_result = run_selected_profile_pipeline(
        profile=str(profile_path) if profile_path is not None else None,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
    )

    if not pipeline_result.ok:
        return {
            "ok": False,
            "stage": pipeline_result.stage,
            "implementation": IMPLEMENTATION_INFO,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [error.to_dict() for error in pipeline_result.errors],
            "bundle": None,
        }

    resolved_profile = pipeline_result.resolved_profile
    assert resolved_profile is not None
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty)
    plan = build_session_plan(resolved_profile, environment)

    with TemporaryDirectory() as tmpdir:
        staging_root = Path(tmpdir) / "compiled"
        compiled = compile_resolved_profile_targets(
            resolved_profile,
            staging_root,
            target_names,
            compile_context={"environment": environment, "display_policy": plan["display_policy"]},
        )
        bundle = _materialize_bundle(
            resolved_profile=resolved_profile,
            source=pipeline_result.source,
            environment=environment,
            plan=plan,
            compiled=compiled,
            bundle_root=bundle_root_path(bundle_root),
        )

    return {
        "ok": True,
        "stage": "bundle",
        "implementation": IMPLEMENTATION_INFO,
        "source": pipeline_result.source,
        "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
        "errors": [],
        "profile": {
            "id": resolved_profile["identity"]["id"],
            "name": resolved_profile["identity"]["name"],
            "origin": resolved_profile["source"]["origin"],
            "pack": resolved_profile.get("pack"),
        },
        "environment": {
            "session_type": environment["session_type"],
            "wm_or_de": environment["wm_or_de"],
            "context_class": environment["context_class"],
        },
        "plan_summary": {
            "compile_targets": plan["compile_targets"],
            "export_only_targets": plan["export_only_targets"],
            "apply_preview_targets": plan["apply_preview_targets"],
            "degraded_targets": plan["degraded_targets"],
        },
        "bundle": bundle,
        "note": "This is a dev-only bundle builder. It does not replace the 1.x installer or runtime.",
    }


def load_bundle_manifest(bundle_path: str | Path) -> dict[str, Any]:
    bundle_dir = _resolve_bundle_dir(bundle_path)
    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"Missing bundle manifest: {manifest_path}")

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if payload.get("schema") != BUNDLE_SCHEMA:
        raise ValueError(f"Unsupported bundle schema in {manifest_path}")
    if not payload.get("bundle_id"):
        raise ValueError(f"Bundle manifest is missing `bundle_id`: {manifest_path}")
    return payload


def _materialize_bundle(
    *,
    resolved_profile: Mapping[str, Any],
    source: Mapping[str, Any],
    environment: Mapping[str, Any],
    plan: Mapping[str, Any],
    compiled: Mapping[str, Any],
    bundle_root: Path,
) -> dict[str, Any]:
    profile = resolved_profile["identity"]
    bundle_id = _bundle_id_for_resolved_profile(resolved_profile)
    output_dir = bundle_root / bundle_id

    if output_dir.exists():
        shutil.rmtree(output_dir)

    bundle_targets_root = output_dir / "targets"
    bundle_metadata_root = output_dir / "metadata"
    bundle_targets_root.mkdir(parents=True, exist_ok=True)
    bundle_metadata_root.mkdir(parents=True, exist_ok=True)

    copied_targets = _copy_target_outputs(compiled["compiled_targets"], bundle_targets_root, output_dir)
    metadata_artifacts = [
        _write_bundle_file(
            output_dir,
            "metadata/resolved-profile.json",
            _json_text(resolved_profile),
        ),
        _write_bundle_file(
            output_dir,
            "metadata/session-plan.json",
            _json_text({"environment": environment, "plan": plan}),
        ),
        _write_bundle_file(
            output_dir,
            "metadata/source.json",
            _json_text({"source": source, "pack": resolved_profile.get("pack")}),
        ),
        _write_bundle_file(
            output_dir,
            "metadata/summary.txt",
            _render_bundle_summary(
                bundle_id=bundle_id,
                profile=profile,
                pack=resolved_profile.get("pack"),
                environment=environment,
                plan=plan,
                copied_targets=copied_targets,
            ),
        ),
    ]

    manifest = {
        "schema": BUNDLE_SCHEMA,
        "bundle_id": bundle_id,
        "install_name": INSTALL_NAME,
        "profile": {
            "id": profile["id"],
            "name": profile["name"],
            "family": profile["family"],
            "strictness": profile["strictness"],
        },
        "pack": resolved_profile.get("pack"),
        "source": source,
        "environment": {
            "session_type": environment["session_type"],
            "wm_or_de": environment["wm_or_de"],
            "context_class": environment["context_class"],
        },
        "plan_summary": {
            "compile_targets": plan["compile_targets"],
            "export_only_targets": plan["export_only_targets"],
            "apply_preview_targets": plan["apply_preview_targets"],
            "degraded_targets": plan["degraded_targets"],
            "skipped_targets": plan["skipped_targets"],
            "warnings": plan["warnings"],
        },
        "install_hint": {
            "bundle_store_relative": install_root_relative_bundle_dir(bundle_id),
            "state_record_relative": install_root_relative_record_path(bundle_id),
            "preserve_config_subdirs": ["profiles", "packs"],
        },
        "compiled_targets": _manifest_compiled_targets(copied_targets),
        "metadata_artifacts": _manifest_artifacts(metadata_artifacts),
    }
    manifest_artifact = _write_bundle_file(output_dir, "manifest.json", _json_text(manifest))

    return {
        "bundle_id": bundle_id,
        "output_dir": str(output_dir),
        "manifest_path": str(output_dir / "manifest.json"),
        "artifacts": [manifest_artifact, *metadata_artifacts],
        "compiled_targets": copied_targets,
    }


def _copy_target_outputs(
    compiled_targets: list[Mapping[str, Any]],
    bundle_targets_root: Path,
    bundle_root: Path,
) -> list[dict[str, Any]]:
    copied_targets: list[dict[str, Any]] = []

    for result in compiled_targets:
        target_name = str(result["target_name"])
        src_dir = Path(str(result["output_dir"]))
        dst_dir = bundle_targets_root / target_name
        shutil.copytree(src_dir, dst_dir)

        artifacts = []
        for artifact in result["artifacts"]:
            bundle_relative_path = f"targets/{artifact['relative_path']}"
            artifacts.append(
                {
                    "target_name": artifact["target_name"],
                    "file_name": artifact["file_name"],
                    "relative_path": bundle_relative_path,
                    "output_path": str(bundle_root / bundle_relative_path),
                    "content_sha256": artifact["content_sha256"],
                    "byte_count": artifact["byte_count"],
                }
            )

        copied_targets.append(
            {
                "target_name": target_name,
                "family_name": result["family_name"],
                "mode": result["mode"],
                "output_dir": str(dst_dir),
                "artifacts": artifacts,
                "consumed_sections": list(result["consumed_sections"]),
                "ignored_sections": list(result["ignored_sections"]),
                "warnings": list(result["warnings"]),
                "notes": list(result["notes"]),
            }
        )

    return sorted(copied_targets, key=lambda item: str(item["target_name"]))


def _manifest_artifacts(artifacts: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "file_name": artifact["file_name"],
            "relative_path": artifact["relative_path"],
            "content_sha256": artifact["content_sha256"],
            "byte_count": artifact["byte_count"],
        }
        for artifact in sorted(artifacts, key=lambda item: str(item["relative_path"]))
    ]


def _manifest_compiled_targets(copied_targets: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    manifest_targets: list[dict[str, Any]] = []
    for result in copied_targets:
        manifest_targets.append(
            {
                "target_name": result["target_name"],
                "family_name": result["family_name"],
                "mode": result["mode"],
                "output_dir_relative": f"targets/{result['target_name']}",
                "artifacts": _manifest_artifacts(result["artifacts"]),
                "consumed_sections": list(result["consumed_sections"]),
                "ignored_sections": list(result["ignored_sections"]),
                "warnings": list(result["warnings"]),
                "notes": list(result["notes"]),
            }
        )
    return manifest_targets


def _render_bundle_summary(
    *,
    bundle_id: str,
    profile: Mapping[str, Any],
    pack: Mapping[str, Any] | None,
    environment: Mapping[str, Any],
    plan: Mapping[str, Any],
    copied_targets: list[Mapping[str, Any]],
) -> str:
    lines = [
        "RetroFX 2.x Dev Bundle",
        f"bundle.id: {bundle_id}",
        f"profile.id: {profile['id']}",
        f"profile.name: {profile['name']}",
        f"profile.family: {profile['family']}",
        f"session_type: {environment['session_type']}",
        f"wm_or_de: {environment['wm_or_de']}",
        f"context_class: {environment['context_class']}",
        f"compile_targets: {', '.join(plan['compile_targets']) or '(none)'}",
        f"degraded_targets: {', '.join(plan['degraded_targets']) or '(none)'}",
        f"bundle_install_hint: {install_root_relative_bundle_dir(bundle_id)}",
        "",
    ]
    if pack is not None:
        lines.extend(
            [
                f"pack.id: {pack['id']}",
                f"pack.name: {pack['name']}",
                f"pack.family: {pack['family'] or '(none)'}",
                "",
            ]
        )
    lines.append("targets:")
    for result in copied_targets:
        lines.append(f"  - {result['target_name']}: {', '.join(artifact['relative_path'] for artifact in result['artifacts'])}")
    lines.append("")
    if plan["warnings"]:
        lines.append("warnings:")
        for warning in plan["warnings"]:
            lines.append(f"  - {warning}")
    return "\n".join(lines) + "\n"


def _bundle_id_for_resolved_profile(resolved_profile: Mapping[str, Any]) -> str:
    profile_id = str(resolved_profile["identity"]["id"])
    pack = resolved_profile.get("pack")
    if isinstance(pack, Mapping) and pack.get("id"):
        return f"{pack['id']}--{profile_id}"
    return profile_id


def _resolve_bundle_dir(bundle_path: str | Path) -> Path:
    path = Path(bundle_path)
    if path.is_file():
        if path.name != "manifest.json":
            raise ValueError(f"Bundle path must be a bundle directory or manifest.json: {path}")
        return path.parent
    return path


def _write_bundle_file(bundle_root: Path, relative_path: str, content: str) -> dict[str, Any]:
    output_path = bundle_root / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "file_name": output_path.name,
        "relative_path": relative_path,
        "output_path": str(output_path),
        "content_sha256": digest,
        "byte_count": len(content.encode("utf-8")),
    }


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
