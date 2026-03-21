"""Dev-only session planning preview for the early 2.x scaffold."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from v2.core.pipeline import run_profile_pipeline
from v2.session import build_session_plan, detect_environment
from v2.targets import list_target_families, list_targets

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT_ROOT = REPO_ROOT / "v2" / "out"
IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-12",
    "surface": "session-planning-preview",
    "implemented_targets": list_targets(),
    "families": list_target_families(),
    "mode": "non-destructive-preview",
    "not_implemented": [
        "live apply/off/install behavior",
        "session wrapper mutation",
        "artifact-plan driven lifecycle execution",
        "X11 render family",
        "global toolkit orchestration and login target families",
    ],
}


def plan_profile_session(
    profile_path: str | Path,
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    out_root: str | Path | None = None,
    write_preview: bool = False,
) -> dict[str, Any]:
    pipeline_result = run_profile_pipeline(profile_path)
    chosen_out_root = Path(out_root) if out_root is not None else DEFAULT_OUT_ROOT

    if not pipeline_result.ok:
        return {
            "ok": False,
            "stage": pipeline_result.stage,
            "implementation": IMPLEMENTATION_INFO,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [error.to_dict() for error in pipeline_result.errors],
            "environment": None,
            "plan": None,
            "preview_bundle": None,
        }

    resolved_profile = pipeline_result.resolved_profile
    assert resolved_profile is not None

    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty)
    plan = build_session_plan(resolved_profile, environment)
    preview_bundle = None
    if write_preview:
        preview_bundle = _write_preview_bundle(
            resolved_profile=resolved_profile,
            environment=environment,
            plan=plan,
            out_root=chosen_out_root,
        )

    return {
        "ok": True,
        "stage": "session-plan",
        "implementation": IMPLEMENTATION_INFO,
        "source": pipeline_result.source,
        "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
        "errors": [],
        "profile": {
            "id": resolved_profile["identity"]["id"],
            "name": resolved_profile["identity"]["name"],
            "requested_targets": plan["requested_targets"],
            "apply_mode": plan["session_policy"]["apply_mode"],
            "persistence": plan["session_policy"]["persistence"],
            "typography": resolved_profile["semantics"]["typography"],
        },
        "environment": environment,
        "plan": plan,
        "preview_bundle": preview_bundle,
        "note": "This is a dev-only planning preview. It does not apply or install anything.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plan an experimental RetroFX 2.x session preview from a 2.x profile without mutating the live session.",
    )
    parser.add_argument("profile", help="Path to a RetroFX 2.x TOML profile.")
    parser.add_argument(
        "--out-root",
        default=str(DEFAULT_OUT_ROOT),
        help=f"Base output root for optional preview bundles. Defaults to {DEFAULT_OUT_ROOT}.",
    )
    parser.add_argument(
        "--write-preview",
        action="store_true",
        help="Write a preview bundle under v2/out/<profile-id>/plan/ without applying anything.",
    )
    args = parser.parse_args(argv)

    payload = plan_profile_session(
        args.profile,
        out_root=args.out_root,
        write_preview=args.write_preview,
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _write_preview_bundle(
    *,
    resolved_profile: Mapping[str, Any],
    environment: Mapping[str, Any],
    plan: Mapping[str, Any],
    out_root: Path,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    plan_root = out_root / profile_id / "plan"
    plan_root.mkdir(parents=True, exist_ok=True)

    plan_payload = {
        "profile": {
            "id": resolved_profile["identity"]["id"],
            "name": resolved_profile["identity"]["name"],
            "typography": resolved_profile["semantics"]["typography"],
        },
        "environment": environment,
        "plan": plan,
    }
    artifacts = [
        _write_preview_file(plan_root / "session-plan.json", json.dumps(plan_payload, indent=2, sort_keys=True) + "\n"),
        _write_preview_file(plan_root / "summary.txt", _render_summary_text(plan_payload)),
    ]
    return {
        "output_dir": str(plan_root),
        "artifacts": artifacts,
    }


def _write_preview_file(path: Path, content: str) -> dict[str, Any]:
    path.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "file_name": path.name,
        "output_path": str(path),
        "content_sha256": digest,
        "byte_count": len(content.encode("utf-8")),
    }


def _render_summary_text(payload: Mapping[str, Any]) -> str:
    plan = payload["plan"]
    environment = payload["environment"]
    lines = [
        "RetroFX 2.x Session Plan Preview",
        f"profile.id: {payload['profile']['id']}",
        f"profile.name: {payload['profile']['name']}",
        f"session_type: {environment['session_type']}",
        f"wm_or_de: {environment['wm_or_de']}",
        f"requested_targets: {', '.join(plan['requested_targets']) or '(none)'}",
        f"terminal_primary: {payload['profile']['typography']['terminal_primary']}",
        f"ui_sans: {payload['profile']['typography']['ui_sans']}",
        (
            "aa_policy: "
            f"antialias={payload['profile']['typography']['aa']['antialias']}, "
            f"subpixel={payload['profile']['typography']['aa']['subpixel']}, "
            f"hinting={payload['profile']['typography']['aa']['hinting']}"
        ),
        f"compile_targets: {', '.join(plan['compile_targets']) or '(none)'}",
        f"apply_preview_targets: {', '.join(plan['apply_preview_targets']) or '(none)'}",
        f"export_only_targets: {', '.join(plan['export_only_targets']) or '(none)'}",
        f"degraded_targets: {', '.join(plan['degraded_targets']) or '(none)'}",
        "",
    ]
    if plan["skipped_targets"]:
        lines.append("skipped_targets:")
        for entry in plan["skipped_targets"]:
            if entry.get("kind") == "requested-target-class":
                lines.append(f"  - {entry['requested_target_class']}: {entry['reason']}")
            else:
                lines.append(f"  - {entry['target_name']}: {', '.join(entry.get('warnings', []))}")
        lines.append("")
    if plan["warnings"]:
        lines.append("warnings:")
        for warning in plan["warnings"]:
            lines.append(f"  - {warning}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
