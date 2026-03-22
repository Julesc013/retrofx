"""Reproducible limited technical-beta candidate package builder for RetroFX 2.x."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Callable, Mapping

from v2.core.dev.profile_input import add_profile_selection_args
from v2.session.install import build_dev_bundle, load_bundle_manifest
from v2.targets import list_target_families, list_targets

from .release import (
    CURRENT_PROMPT,
    DEFAULT_TECHNICAL_BETA_PACKAGE_ROOT,
    TECHNICAL_BETA_PACKAGE_SCHEMA,
    build_experimental_release_metadata,
    build_technical_beta_candidate_metadata,
    package_id_for_bundle,
)
from .technical_beta import TECHNICAL_BETA_COMMAND_SUMMARY, TECHNICAL_BETA_SUPPORT_MATRIX, technical_beta_candidate_summary_text

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "v2"
TECHNICAL_BETA_PACKAGE_DOCS = (
    "README.md",
    "IMPLEMENTED_STATUS.md",
    "VALIDATION_MATRIX.md",
    "PUBLIC_BETA_RISK_SURFACE.md",
    "PUBLIC_BETA_GATES.md",
    "PUBLIC_BETA_BLOCKERS.md",
    "PUBLIC_BETA_READINESS.md",
    "TECHNICAL_BETA_NOTES.md",
    "TECHNICAL_BETA_CHECKLIST.md",
    "TECHNICAL_BETA_OPERATIONS.md",
    "LIMITED_TECHNICAL_BETA_RUNBOOK.md",
    "TECHNICAL_BETA_CANDIDATE_NOTES.md",
    "TECHNICAL_BETA_CANDIDATE_SUMMARY.md",
    "TECHNICAL_BETA_RELEASE_CHECKLIST.md",
    "NEXT_STAGE_VERDICT.md",
    "EXPERIMENTAL_STATUS.md",
)

IMPLEMENTATION_INFO = {
    "status": "experimental-limited-technical-beta",
    "prompt": CURRENT_PROMPT,
    "surface": "technical-beta-package-builder",
    "package_schema": TECHNICAL_BETA_PACKAGE_SCHEMA,
    "mode": "limited-public-technical-beta-candidate-package",
    "not_implemented": [
        "automatic public publication",
        "signed release artifacts",
        "distro-native packages",
        "general-user installation UX",
    ],
}


def build_technical_beta_package(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    package_root: str | Path | None = None,
    target_names: list[str] | None = None,
    allow_dirty: bool = False,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    current_release = build_experimental_release_metadata()
    if not current_release["ready_for_limited_public_technical_beta"]:
        return {
            "ok": False,
            "stage": "package-technical-beta",
            "implementation": IMPLEMENTATION_INFO,
            "release_status": current_release,
            "source": None,
            "warnings": [],
            "errors": [
                {
                    "severity": "error",
                    "code": "technical-beta-gate-denied",
                    "message": "The current branch does not clear the limited public technical-beta gates.",
                }
            ],
            "package": None,
        }
    if current_release["working_tree_clean"] is False and not allow_dirty:
        return {
            "ok": False,
            "stage": "package-technical-beta",
            "implementation": IMPLEMENTATION_INFO,
            "release_status": current_release,
            "source": None,
            "warnings": [],
            "errors": [
                {
                    "severity": "error",
                    "code": "dirty-working-tree",
                    "message": "Technical-beta candidate packaging requires a clean working tree.",
                }
            ],
            "package": None,
        }

    release = build_technical_beta_candidate_metadata()
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
        output_root = Path(package_root) if package_root is not None else DEFAULT_TECHNICAL_BETA_PACKAGE_ROOT
        output_dir = output_root / package_id
        if output_dir.exists():
            shutil.rmtree(output_dir)

        copied_bundle_dir = output_dir / "bundle"
        copied_bundle_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(bundle_dir, copied_bundle_dir)
        _rewrite_bundle_manifest_release(copied_bundle_dir, release)

    toolchain_artifacts = _copy_toolchain(output_dir)
    doc_artifacts = _copy_package_docs(output_dir)
    metadata_artifacts = [
        _write_package_file(output_dir, "metadata/release-status.json", _json_text(release)),
        _write_package_file(
            output_dir,
            "metadata/platform-snapshot.json",
            _json_text(
                {
                    "release_status": release,
                    "supported_target_families": list_target_families(),
                    "supported_targets": list_targets(),
                    "technical_beta_commands": [item["command"] for item in TECHNICAL_BETA_COMMAND_SUMMARY],
                    "technical_beta_support_matrix": TECHNICAL_BETA_SUPPORT_MATRIX,
                }
            ),
        ),
        _write_package_file(
            output_dir,
            "metadata/summary.txt",
            technical_beta_candidate_summary_text(str(output_dir)),
        ),
    ]

    manifest = {
        "schema": TECHNICAL_BETA_PACKAGE_SCHEMA,
        "package_id": package_id,
        "release_status": release,
        "distribution": {
            "scope": "limited-public-technical-beta",
            "toolchain_mode": "copied-toolchain",
            "public_release": False,
            "automatic_publication": False,
        },
        "bundle": {
            "bundle_id": bundle_manifest["bundle_id"],
            "relative_dir": "bundle",
            "manifest_relative_path": "bundle/manifest.json",
            "install_name": bundle_manifest["install_name"],
        },
        "toolchain": {
            "relative_dir": "toolchain",
            "entrypoint_relative_path": "bin/retrofx-v2-techbeta",
            "copied_wrapper_relative_path": "toolchain/scripts/dev/retrofx-v2-techbeta",
            "copied_paths": [artifact["relative_path"] for artifact in toolchain_artifacts],
        },
        "profile": dict(bundle_manifest["profile"]),
        "pack": bundle_manifest.get("pack"),
        "source": bundle_manifest.get("source"),
        "supported_target_families": list_target_families(),
        "supported_targets": list_targets(),
        "technical_beta_commands": [item["command"] for item in TECHNICAL_BETA_COMMAND_SUMMARY],
        "technical_beta_support_matrix": TECHNICAL_BETA_SUPPORT_MATRIX,
        "included_docs": [artifact["relative_path"] for artifact in doc_artifacts],
        "metadata_artifacts": [artifact["relative_path"] for artifact in metadata_artifacts],
        "known_limitations": [
            *release["technical_beta_limitations"],
            "This candidate remains experimental and is intended only for advanced testers.",
            "Wayland planning and compile remain useful for export-oriented validation but are outside the supported live runtime matrix.",
            "Migration inspection remains an internal developer workflow and is not part of this candidate surface.",
            "No automatic publication is performed by this package flow.",
        ],
        "recommended_smoke_flow": _recommended_smoke_flow(bundle_manifest),
        "notes": [
            "This package is the limited technical-beta candidate surface for advanced testers.",
            "It does not replace the 1.x runtime, installer, or production CLI.",
            "It remains non-destructive, user-local, and explicitly scoped.",
        ],
    }
    manifest_artifact = _write_package_file(output_dir, "package-manifest.json", _json_text(manifest))

    return {
        "ok": True,
        "stage": "package-technical-beta",
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
            "entrypoint_path": str(output_dir / "bin" / "retrofx-v2-techbeta"),
            "docs_dir": str(output_dir / "docs"),
            "metadata_dir": str(output_dir / "metadata"),
            "included_docs": [artifact["relative_path"] for artifact in doc_artifacts],
            "artifacts": [manifest_artifact, *metadata_artifacts, *doc_artifacts, *toolchain_artifacts],
        },
        "note": (
            "This builds a limited technical-beta candidate package with a copied toolchain, bounded bundle, "
            "diagnostics guidance, and explicit support-matrix docs. It does not publish anything automatically."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 package-technical-beta",
        description="Build one reproducible limited public technical-beta candidate package for advanced testers. This stays local and does not publish anything automatically.",
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
        default=str(DEFAULT_TECHNICAL_BETA_PACKAGE_ROOT),
        help=f"Package output root. Defaults to {DEFAULT_TECHNICAL_BETA_PACKAGE_ROOT}.",
    )
    args = parser.parse_args(argv)

    payload = build_technical_beta_package(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        package_root=args.package_root,
        target_names=args.targets,
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _copy_toolchain(package_root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    toolchain_root = package_root / "toolchain"

    copied_v2_root = toolchain_root / "v2"
    shutil.copytree(
        REPO_ROOT / "v2",
        copied_v2_root,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "out", "bundles", "releases", "tests"),
    )
    artifacts.append(_record_tree_artifact(package_root, copied_v2_root))

    copied_docs_root = toolchain_root / "docs" / "v2"
    shutil.copytree(REPO_ROOT / "docs" / "v2", copied_docs_root)
    artifacts.append(_record_tree_artifact(package_root, copied_docs_root))

    wrapper_src = REPO_ROOT / "scripts" / "dev" / "retrofx-v2-techbeta"
    wrapper_dst = toolchain_root / "scripts" / "dev" / "retrofx-v2-techbeta"
    wrapper_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wrapper_src, wrapper_dst)
    wrapper_dst.chmod(0o755)
    artifacts.append(_record_file_artifact(package_root, wrapper_dst))

    entrypoint = package_root / "bin" / "retrofx-v2-techbeta"
    entrypoint.parent.mkdir(parents=True, exist_ok=True)
    entrypoint.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                'script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"',
                'package_root="$(cd "${script_dir}/.." && pwd)"',
                'exec "${package_root}/toolchain/scripts/dev/retrofx-v2-techbeta" "$@"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    entrypoint.chmod(0o755)
    artifacts.append(_record_file_artifact(package_root, entrypoint))
    return artifacts


def _copy_package_docs(package_root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for doc_name in TECHNICAL_BETA_PACKAGE_DOCS:
        source_path = DOCS_ROOT / doc_name
        relative_path = f"docs/{doc_name}"
        content = source_path.read_text(encoding="utf-8")
        artifacts.append(_write_package_file(package_root, relative_path, content))
    return artifacts


def _recommended_smoke_flow(bundle_manifest: Mapping[str, Any]) -> list[str]:
    bundle_id = str(bundle_manifest["bundle_id"])
    commands = [
        "bin/retrofx-v2-techbeta status",
    ]
    pack = bundle_manifest.get("pack")
    profile_id = bundle_manifest["profile"]["id"]
    if isinstance(pack, Mapping) and pack.get("id"):
        commands.extend(
            [
                f"bin/retrofx-v2-techbeta resolve --pack {pack['id']} --profile-id {profile_id}",
                f"bin/retrofx-v2-techbeta plan --pack {pack['id']} --profile-id {profile_id} --write-preview",
                f"bin/retrofx-v2-techbeta compile --pack {pack['id']} --profile-id {profile_id}",
            ]
        )
    commands.extend(
        [
            "bin/retrofx-v2-techbeta install <package-dir>/bundle",
            "bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --label techbeta-pass",
            "bin/retrofx-v2-techbeta off",
            f"bin/retrofx-v2-techbeta uninstall {bundle_id}",
        ]
    )
    return commands


def _rewrite_bundle_manifest_release(bundle_dir: Path, release: Mapping[str, Any]) -> None:
    manifest_path = bundle_dir / "manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["experimental_release"] = dict(release)
    manifest_path.write_text(_json_text(payload), encoding="utf-8")


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


def _record_file_artifact(package_root: Path, path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "file_name": path.name,
        "relative_path": str(path.relative_to(package_root)),
        "output_path": str(path),
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "byte_count": len(content),
    }


def _record_tree_artifact(package_root: Path, path: Path) -> dict[str, Any]:
    file_count = sum(1 for item in path.rglob("*") if item.is_file())
    return {
        "file_name": path.name,
        "relative_path": str(path.relative_to(package_root)),
        "output_path": str(path),
        "directory": True,
        "file_count": file_count,
    }


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
