"""Unified experimental CLI for the RetroFX 2.x development branch."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from v2.compat.dev import inspect_1x_profile as compat_inspect_1x
from v2.core.dev import compile_targets as core_compile
from v2.core.dev import list_packs as core_list_packs
from v2.core.dev import plan_session as core_plan
from v2.core.dev import resolve_profile as core_resolve
from v2.core.dev import show_pack as core_show_pack
from v2.core.dev.profile_input import add_profile_selection_args
from v2.session.apply import cli as apply_cli
from v2.session.dev import preview_x11_render as preview_x11
from v2.session.install import cli as install_cli

from . import package_alpha as dev_package_alpha
from .smoke import run_smoke_workflow
from .status import build_platform_status


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    delegated = _dispatch_passthrough_command(argv)
    if delegated is not None:
        return delegated

    parser = argparse.ArgumentParser(
        prog="retrofx-v2",
        description=(
            "Unified experimental RetroFX 2.x developer surface. "
            "This command does not replace the 1.x runtime or the production `retrofx` CLI."
        ),
        epilog=(
            "This surface exposes only the currently implemented experimental commands. "
            "Export-oriented targets remain far more complete than live apply behavior."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show the current 2.x platform status, implemented interfaces, environment, and active experimental state.")
    subparsers.add_parser("capabilities", help="Alias for `status` with the same machine-readable experimental platform report.")

    _add_passthrough_command(subparsers, "resolve", "Resolve one 2.x profile through the implemented dev-only load/validate/normalize/resolve pipeline.")
    _add_passthrough_command(subparsers, "compile", "Compile the implemented target families into deterministic export artifacts.")
    _add_passthrough_command(subparsers, "plan", "Run the implemented non-destructive session planning preview for the current environment.")
    _add_passthrough_command(subparsers, "preview-x11", "Run the bounded X11 render preview surface. This remains explicit and experimental.")
    _add_passthrough_command(subparsers, "apply", "Run the bounded TWO-19 experimental apply flow under the isolated 2.x-owned footprint.")
    _add_passthrough_command(subparsers, "off", "Clear the bounded TWO-19 experimental activation without touching 1.x.")
    _add_passthrough_command(subparsers, "bundle", "Build one deterministic TWO-16 dev bundle.")
    _add_passthrough_command(subparsers, "package-alpha", "Build one reproducible TWO-24 internal-alpha package around a deterministic 2.x bundle.")
    _add_passthrough_command(subparsers, "install", "Install one dev bundle into the isolated user-local 2.x footprint.")
    _add_passthrough_command(subparsers, "uninstall", "Remove one installed dev bundle from the isolated user-local 2.x footprint.")

    packs_parser = subparsers.add_parser("packs", help="Inspect the implemented local 2.x pack surface.")
    packs_subparsers = packs_parser.add_subparsers(dest="packs_command", required=True)
    packs_subparsers.add_parser("list", help="List available 2.x packs.")
    packs_show = packs_subparsers.add_parser("show", help="Show one 2.x pack manifest.")
    packs_show.add_argument("pack_id", help="Pack id under v2/packs/.")

    migrate_parser = subparsers.add_parser("migrate", help="Inspect supported 1.x profiles and draft migration output. This is not runtime compatibility.")
    migrate_subparsers = migrate_parser.add_subparsers(dest="migrate_command", required=True)
    migrate_inspect = migrate_subparsers.add_parser("inspect-1x", help="Inspect one 1.x profile for supported migration mapping.")
    migrate_inspect.add_argument("profile", help="Path to a 1.x profile.")
    migrate_inspect.add_argument("--write-draft", action="store_true", help="Emit a generated 2.x draft migration bundle.")
    migrate_inspect.add_argument("--out-root", help="Override the migration output root.")
    migrate_inspect.add_argument("--compact", action="store_true", help="Emit compact JSON.")

    smoke_parser = subparsers.add_parser("smoke", help="Run a safe 2.x smoke path: resolve, plan, compile, and optionally bounded apply.")
    add_profile_selection_args(smoke_parser)
    smoke_parser.add_argument(
        "--out-root",
        default=str(core_compile.DEFAULT_OUT_ROOT),
        help=f"Output root for generated preview and compile artifacts. Defaults to {core_compile.DEFAULT_OUT_ROOT}.",
    )
    smoke_parser.add_argument(
        "--apply",
        action="store_true",
        help="Also run the bounded TWO-19 apply step after resolve, plan, and compile.",
    )
    smoke_parser.add_argument(
        "--probe-x11",
        action="store_true",
        help="When combined with --apply, allow the explicit bounded X11 probe if the environment permits it.",
    )
    smoke_parser.add_argument(
        "--probe-seconds",
        type=float,
        default=3.0,
        help="Timeout for the explicit X11 probe when --apply --probe-x11 is used.",
    )

    args = parser.parse_args(argv)

    if args.command in {"status", "capabilities"}:
        payload = build_platform_status(cwd=Path.cwd())
        if args.command == "capabilities":
            payload["stage"] = "platform-capabilities"
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0

    if args.command == "resolve":
        return core_resolve.main(_normalize_passthrough(args.args))
    if args.command == "compile":
        return core_compile.main(_normalize_passthrough(args.args))
    if args.command == "plan":
        return core_plan.main(_normalize_passthrough(args.args))
    if args.command == "preview-x11":
        return preview_x11.main(_normalize_passthrough(args.args))
    if args.command == "apply":
        return apply_cli.main(["apply", *_normalize_passthrough(args.args)])
    if args.command == "off":
        return apply_cli.main(["off", *_normalize_passthrough(args.args)])
    if args.command == "bundle":
        return install_cli.main(["bundle", *_normalize_passthrough(args.args)])
    if args.command == "package-alpha":
        return dev_package_alpha.main(_normalize_passthrough(args.args))
    if args.command == "install":
        return install_cli.main(["install", *_normalize_passthrough(args.args)])
    if args.command == "uninstall":
        return install_cli.main(["uninstall", *_normalize_passthrough(args.args)])

    if args.command == "packs":
        if args.packs_command == "list":
            return core_list_packs.main([])
        return core_show_pack.main([args.pack_id])

    if args.command == "migrate":
        migrate_args = [args.profile]
        if args.write_draft:
            migrate_args.append("--write-draft")
        if args.out_root:
            migrate_args.extend(["--out-root", args.out_root])
        if args.compact:
            migrate_args.append("--compact")
        return compat_inspect_1x.main(migrate_args)

    payload = run_smoke_workflow(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        out_root=args.out_root,
        cwd=Path.cwd(),
        apply=args.apply,
        probe_x11=args.probe_x11,
        probe_seconds=args.probe_seconds,
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
    if command == "preview-x11":
        return preview_x11.main(argv[1:])
    if command == "apply":
        return apply_cli.main(["apply", *argv[1:]])
    if command == "off":
        return apply_cli.main(["off", *argv[1:]])
    if command == "bundle":
        return install_cli.main(["bundle", *argv[1:]])
    if command == "package-alpha":
        return dev_package_alpha.main(argv[1:])
    if command == "install":
        return install_cli.main(["install", *argv[1:]])
    if command == "uninstall":
        return install_cli.main(["uninstall", *argv[1:]])
    return None


if __name__ == "__main__":
    raise SystemExit(main())
