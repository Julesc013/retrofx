"""Deterministic internal-alpha package builder for the RetroFX 2.x branch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Callable, Mapping

from v2.core.interfaces import IMPLEMENTED_INTERFACES
from v2.core.dev.profile_input import add_profile_selection_args
from v2.session.install import build_dev_bundle, load_bundle_manifest
from v2.targets import list_target_families, list_targets

from .release import (
    CURRENT_PROMPT,
    DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT,
    INTERNAL_ALPHA_PACKAGE_SCHEMA,
    build_experimental_release_metadata,
    package_id_for_bundle,
)
from .status import COMMAND_SUMMARY, IMPLEMENTED_STATUS_MATRIX

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "v2"
PACKAGE_DOCS = (
    "README.md",
    "ALPHA_VERSIONING.md",
    "EXPERIMENTAL_STATUS.md",
    "INTERNAL_ALPHA_RUNBOOK.md",
    "INTERNAL_ALPHA_NOTES.md",
    "ALPHA_READINESS.md",
)

IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": CURRENT_PROMPT,
    "surface": "internal-alpha-package-builder",
    "package_schema": INTERNAL_ALPHA_PACKAGE_SCHEMA,
    "mode": "non-public-internal-alpha-package",
    "not_implemented": [
        "public release publishing",
        "standalone copied toolchain packaging",
        "distro-native packages",
        "signed release artifacts",
    ],
}


def build_internal_alpha_package(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    package_root: str | Path | None = None,
    target_names: list[str] | None = None,
    version: str | None = None,
    status_label: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    release = build_experimental_release_metadata(version=version, status_label=status_label)

    with TemporaryDirectory() as tmpbundle:
        bundle_payload = build_dev_bundle(
            profile_path,
            pack_id=pack_id,
            pack_profile_id=pack_profile_id,
            bundle_root=tmpbundle,
            target_names=target_names,
            env=env,
            cwd=cwd,
            stdin_isatty=stdin_isatty,
            path_lookup=path_lookup,
        )
        if not bundle_payload["ok"]:
            return {
                "ok": False,
                "stage": bundle_payload["stage"],
                "implementation": IMPLEMENTATION_INFO,
                "release_status": release,
                "source": bundle_payload.get("source"),
                "warnings": bundle_payload.get("warnings", []),
                "errors": bundle_payload.get("errors", []),
                "package": None,
            }

        bundle_dir = Path(str(bundle_payload["bundle"]["output_dir"]))
        bundle_manifest = load_bundle_manifest(bundle_dir)
        package_id = package_id_for_bundle(str(bundle_manifest["bundle_id"]), version=release["version"])
        output_root = Path(package_root) if package_root is not None else DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT
        output_dir = output_root / package_id
        if output_dir.exists():
            shutil.rmtree(output_dir)

        copied_bundle_dir = output_dir / "bundle"
        copied_bundle_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(bundle_dir, copied_bundle_dir)

    doc_artifacts = _copy_package_docs(output_dir)
    platform_snapshot = _build_platform_snapshot(release)
    metadata_artifacts = [
        _write_package_file(output_dir, "metadata/release-status.json", _json_text(release)),
        _write_package_file(output_dir, "metadata/platform-snapshot.json", _json_text(platform_snapshot)),
        _write_package_file(
            output_dir,
            "metadata/summary.txt",
            _render_package_summary(
                package_id=package_id,
                release=release,
                bundle_manifest=bundle_manifest,
            ),
        ),
    ]

    manifest = {
        "schema": INTERNAL_ALPHA_PACKAGE_SCHEMA,
        "package_id": package_id,
        "release_status": release,
        "distribution": {
            "scope": "internal-non-public",
            "toolchain_mode": "repo-checkout-required",
            "public_release": False,
        },
        "bundle": {
            "bundle_id": bundle_manifest["bundle_id"],
            "relative_dir": "bundle",
            "manifest_relative_path": "bundle/manifest.json",
            "install_name": bundle_manifest["install_name"],
        },
        "profile": dict(bundle_manifest["profile"]),
        "pack": bundle_manifest.get("pack"),
        "source": bundle_manifest.get("source"),
        "supported_target_families": list_target_families(),
        "supported_targets": list_targets(),
        "implemented_interfaces": [item["name"] for item in IMPLEMENTED_INTERFACES],
        "included_docs": [artifact["relative_path"] for artifact in doc_artifacts],
        "metadata_artifacts": [artifact["relative_path"] for artifact in metadata_artifacts],
        "known_limitations": [
            "This package does not contain a standalone copied 2.x toolchain.",
            "Internal testers are expected to run the package against a repo checkout with `scripts/dev/retrofx-v2` available.",
            "Toolkit exports remain advisory and live desktop integration is not implemented.",
            "Live Wayland render is not implemented.",
            "1.x remains the production line.",
        ],
        "recommended_smoke_flow": _recommended_smoke_flow(bundle_manifest),
        "notes": [
            "This package is for controlled internal alpha circulation only.",
            "It does not replace the 1.x runtime, installer, or public release process.",
        ],
    }
    manifest_artifact = _write_package_file(output_dir, "package-manifest.json", _json_text(manifest))

    return {
        "ok": True,
        "stage": "package-alpha",
        "implementation": IMPLEMENTATION_INFO,
        "release_status": release,
        "source": bundle_payload["source"],
        "warnings": bundle_payload["warnings"],
        "errors": [],
        "bundle": {
            "bundle_id": bundle_manifest["bundle_id"],
            "manifest_path": str(copied_bundle_dir / "manifest.json"),
            "output_dir": str(copied_bundle_dir),
        },
        "package": {
            "package_id": package_id,
            "output_dir": str(output_dir),
            "manifest_path": str(output_dir / "package-manifest.json"),
            "docs_dir": str(output_dir / "docs"),
            "metadata_dir": str(output_dir / "metadata"),
            "included_docs": [artifact["relative_path"] for artifact in doc_artifacts],
            "artifacts": [manifest_artifact, *metadata_artifacts, *doc_artifacts],
        },
        "note": (
            "This creates a reproducible internal-alpha package around one deterministic 2.x bundle. "
            "It remains non-public and does not provide a standalone production toolchain."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 package-alpha",
        description="Build one deterministic RetroFX 2.x internal-alpha package for non-public internal testing.",
    )
    add_profile_selection_args(parser)
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Package only the selected compiled target. Repeat for multiple targets.",
    )
    parser.add_argument(
        "--package-root",
        default=str(DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT),
        help=f"Package output root. Defaults to {DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT}.",
    )
    parser.add_argument(
        "--version",
        help="Override the experimental internal-alpha version string for this package.",
    )
    parser.add_argument(
        "--status-label",
        help="Override the experimental status label for this package.",
    )
    args = parser.parse_args(argv)

    payload = build_internal_alpha_package(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        package_root=args.package_root,
        target_names=args.targets,
        version=args.version,
        status_label=args.status_label,
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _copy_package_docs(package_root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for doc_name in PACKAGE_DOCS:
        source_path = DOCS_ROOT / doc_name
        relative_path = f"docs/{doc_name}"
        content = source_path.read_text(encoding="utf-8")
        artifacts.append(_write_package_file(package_root, relative_path, content))
    return artifacts


def _build_platform_snapshot(release: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "release_status": release,
        "implemented_status_matrix": IMPLEMENTED_STATUS_MATRIX,
        "implemented_interfaces": [item["name"] for item in IMPLEMENTED_INTERFACES],
        "supported_target_families": list_target_families(),
        "supported_targets": list_targets(),
        "dev_surface_commands": [item["command"] for item in COMMAND_SUMMARY],
    }


def _recommended_smoke_flow(bundle_manifest: Mapping[str, Any]) -> list[str]:
    bundle_id = str(bundle_manifest["bundle_id"])
    commands = [
        "scripts/dev/retrofx-v2 status",
    ]
    pack = bundle_manifest.get("pack")
    profile_id = bundle_manifest["profile"]["id"]
    if isinstance(pack, Mapping) and pack.get("id"):
        commands.extend(
            [
                f"scripts/dev/retrofx-v2 resolve --pack {pack['id']} --profile-id {profile_id}",
                f"scripts/dev/retrofx-v2 plan --pack {pack['id']} --profile-id {profile_id} --write-preview",
                f"scripts/dev/retrofx-v2 compile --pack {pack['id']} --profile-id {profile_id}",
            ]
        )
    commands.extend(
        [
            "scripts/dev/retrofx-v2 install <package-dir>/bundle",
            "scripts/dev/retrofx-v2 status",
            "scripts/dev/retrofx-v2 off",
            f"scripts/dev/retrofx-v2 uninstall {bundle_id}",
        ]
    )
    return commands


def _render_package_summary(
    *,
    package_id: str,
    release: Mapping[str, Any],
    bundle_manifest: Mapping[str, Any],
) -> str:
    lines = [
        "RetroFX 2.x Internal Alpha Package",
        f"package.id: {package_id}",
        f"release.version: {release['version']}",
        f"release.status: {release['status_label']}",
        f"distribution.scope: {release['distribution_scope']}",
        f"bundle.id: {bundle_manifest['bundle_id']}",
        f"profile.id: {bundle_manifest['profile']['id']}",
        f"profile.name: {bundle_manifest['profile']['name']}",
        f"compile_targets: {', '.join(bundle_manifest['plan_summary']['compile_targets']) or '(none)'}",
        f"degraded_targets: {', '.join(bundle_manifest['plan_summary']['degraded_targets']) or '(none)'}",
        "",
        "This package is non-public and expects a repo checkout for command execution.",
        "Recommended first command: scripts/dev/retrofx-v2 status",
        "",
    ]
    return "\n".join(lines)


def _write_package_file(package_root: Path, relative_path: str, content: str) -> dict[str, Any]:
    output_path = package_root / relative_path
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


if __name__ == "__main__":
    raise SystemExit(main())
