"""Curated limited technical-beta CLI for advanced RetroFX 2.x testers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from v2.core.dev import compile_targets as core_compile
from v2.core.dev import list_packs as core_list_packs
from v2.core.dev import plan_session as core_plan
from v2.core.dev import resolve_profile as core_resolve
from v2.core.dev import show_pack as core_show_pack
from v2.core.dev.profile_input import add_profile_selection_args
from v2.session.apply import cli as apply_cli
from v2.session.install import cli as install_cli

from . import capture_diagnostics as dev_diagnostics
from .release import build_technical_beta_candidate_metadata
from .smoke import run_smoke_workflow
from .technical_beta import (
    TECHNICAL_BETA_IMPLEMENTATION_INFO,
    build_technical_beta_status,
    is_supported_technical_beta_apply_environment,
    technical_beta_apply_environment_error,
)

TECHNICAL_BETA_DIAGNOSTICS_IMPLEMENTATION_INFO = {
    **TECHNICAL_BETA_IMPLEMENTATION_INFO,
    "surface": "technical-beta-diagnostics",
}


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    delegated = _dispatch_passthrough_command(argv)
    if delegated is not None:
        return delegated

    parser = argparse.ArgumentParser(
        prog="retrofx-v2-techbeta",
        description=(
            "Curated limited technical-beta RetroFX 2.x surface for advanced testers. "
            "This command does not replace 1.x, does not promise universal desktop support, "
            "and currently supports bounded live apply only on X11-oriented environments."
        ),
        epilog=(
            "Wayland planning and compile remain useful for export-oriented validation, but they are not part of the supported live technical-beta path. "
            "Migration inspection and the explicit X11 preview probe remain on the internal developer surface."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show the limited technical-beta status report and support matrix.")
    subparsers.add_parser("capabilities", help="Alias for `status` with the same machine-readable candidate report.")

    _add_passthrough_command(subparsers, "resolve", "Resolve one 2.x profile or curated pack profile.")
    _add_passthrough_command(subparsers, "compile", "Compile deterministic artifacts for the supported technical-beta target families.")
    _add_passthrough_command(subparsers, "plan", "Preview capability-aware planning without mutating the live session.")
    _add_passthrough_command(subparsers, "bundle", "Build one deterministic bundle for the limited technical-beta surface.")
    _add_passthrough_command(subparsers, "diagnostics", "Capture a local diagnostics directory suitable for technical-beta bug reports.")
    _add_passthrough_command(subparsers, "install", "Install one generated bundle into the bounded `retrofx-v2-dev` footprint.")
    _add_passthrough_command(subparsers, "uninstall", "Remove one installed bundle from the bounded `retrofx-v2-dev` footprint.")

    apply_parser = subparsers.add_parser(
        "apply",
        help="Run the bounded apply flow on supported X11 environments only.",
        add_help=False,
    )
    apply_parser.add_argument("args", nargs=argparse.REMAINDER)

    _add_passthrough_command(subparsers, "off", "Clear the bounded current activation without touching 1.x.")

    packs_parser = subparsers.add_parser("packs", help="Inspect the curated pack surface shipped with the technical-beta toolchain.")
    packs_subparsers = packs_parser.add_subparsers(dest="packs_command", required=True)
    packs_subparsers.add_parser("list", help="List available 2.x packs.")
    packs_show = packs_subparsers.add_parser("show", help="Show one 2.x pack manifest.")
    packs_show.add_argument("pack_id", help="Pack id under v2/packs/.")

    smoke_parser = subparsers.add_parser(
        "smoke",
        help="Run the supported smoke path: resolve, plan, compile, and optionally bounded apply on X11.",
    )
    add_profile_selection_args(smoke_parser)
    smoke_parser.add_argument(
        "--out-root",
        default=str(core_compile.DEFAULT_OUT_ROOT),
        help=f"Output root for generated preview and compile artifacts. Defaults to {core_compile.DEFAULT_OUT_ROOT}.",
    )
    smoke_parser.add_argument(
        "--apply",
        action="store_true",
        help="Also run the bounded apply step after resolve, plan, and compile. Supported on X11 only.",
    )

    args = parser.parse_args(argv)

    if args.command in {"status", "capabilities"}:
        payload = build_technical_beta_status(cwd=Path.cwd(), stdin_isatty=sys.stdin.isatty())
        if args.command == "capabilities":
            payload["stage"] = "technical-beta-capabilities"
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0

    if args.command == "resolve":
        return core_resolve.main(_normalize_passthrough(args.args))
    if args.command == "compile":
        return core_compile.main(_normalize_passthrough(args.args))
    if args.command == "plan":
        return core_plan.main(_normalize_passthrough(args.args))
    if args.command == "bundle":
        return install_cli.main(["bundle", *_normalize_passthrough(args.args)])
    if args.command == "diagnostics":
        return dev_diagnostics.main(
            _normalize_passthrough(args.args),
            release_status=build_technical_beta_candidate_metadata(),
            platform_status_builder=build_technical_beta_status,
            implementation_info=TECHNICAL_BETA_DIAGNOSTICS_IMPLEMENTATION_INFO,
        )
    if args.command == "install":
        return install_cli.main(["install", *_normalize_passthrough(args.args)])
    if args.command == "uninstall":
        return install_cli.main(["uninstall", *_normalize_passthrough(args.args)])
    if args.command == "apply":
        supported, environment = is_supported_technical_beta_apply_environment(cwd=Path.cwd(), stdin_isatty=sys.stdin.isatty())
        if not supported:
            payload = technical_beta_apply_environment_error(environment)
            print(json.dumps(payload, indent=2, sort_keys=False))
            return 1
        return apply_cli.main(["apply", *_normalize_passthrough(args.args)])
    if args.command == "off":
        return apply_cli.main(["off", *_normalize_passthrough(args.args)])

    if args.command == "packs":
        if args.packs_command == "list":
            return core_list_packs.main([])
        return core_show_pack.main([args.pack_id])

    if args.apply:
        supported, environment = is_supported_technical_beta_apply_environment(cwd=Path.cwd(), stdin_isatty=sys.stdin.isatty())
        if not supported:
            payload = technical_beta_apply_environment_error(environment)
            print(json.dumps(payload, indent=2, sort_keys=False))
            return 1

    payload = run_smoke_workflow(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        out_root=args.out_root,
        cwd=Path.cwd(),
        apply=args.apply,
        probe_x11=False,
        probe_seconds=0.0,
        stdin_isatty=sys.stdin.isatty(),
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _add_passthrough_command(subparsers: argparse._SubParsersAction[argparse.ArgumentParser], name: str, help_text: str) -> None:
    parser = subparsers.add_parser(name, help=help_text, add_help=False)
    parser.add_argument("args", nargs=argparse.REMAINDER)


def _normalize_passthrough(values: list[str]) -> list[str]:
    if values and values[0] == "--":
        return values[1:]
    return values


def _dispatch_passthrough_command(argv: list[str]) -> int | None:
    if not argv:
        return None

    command = argv[0]
    if command == "resolve":
        return core_resolve.main(argv[1:])
    if command == "compile":
        return core_compile.main(argv[1:])
    if command == "plan":
        return core_plan.main(argv[1:])
    if command == "bundle":
        return install_cli.main(["bundle", *argv[1:]])
    if command == "diagnostics":
        return dev_diagnostics.main(
            argv[1:],
            release_status=build_technical_beta_candidate_metadata(),
            platform_status_builder=build_technical_beta_status,
            implementation_info=TECHNICAL_BETA_DIAGNOSTICS_IMPLEMENTATION_INFO,
        )
    if command == "install":
        return install_cli.main(["install", *argv[1:]])
    if command == "uninstall":
        return install_cli.main(["uninstall", *argv[1:]])
    if command == "apply":
        supported, environment = is_supported_technical_beta_apply_environment(cwd=Path.cwd(), stdin_isatty=sys.stdin.isatty())
        if not supported:
            payload = technical_beta_apply_environment_error(environment)
            print(json.dumps(payload, indent=2, sort_keys=False))
            return 1
        return apply_cli.main(["apply", *argv[1:]])
    if command == "off":
        return apply_cli.main(["off", *argv[1:]])
    return None


if __name__ == "__main__":
    raise SystemExit(main())
