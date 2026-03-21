"""CLI for the experimental RetroFX 2.x bundle/install flow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from v2.core.dev.profile_input import add_profile_selection_args

from .bundle import build_dev_bundle
from .layout import DEFAULT_BUNDLE_ROOT
from .manager import describe_install_state, install_dev_bundle, uninstall_dev_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Experimental RetroFX 2.x dev bundle/install helpers. These commands are user-local and do not replace the 1.x runtime.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bundle_parser = subparsers.add_parser("bundle", help="Build a deterministic dev bundle from a 2.x profile or pack profile.")
    add_profile_selection_args(bundle_parser)
    bundle_parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Bundle only the selected target. Repeat for multiple targets.",
    )
    bundle_parser.add_argument(
        "--bundle-root",
        default=str(DEFAULT_BUNDLE_ROOT),
        help=f"Bundle output root. Defaults to {DEFAULT_BUNDLE_ROOT}.",
    )

    install_parser = subparsers.add_parser("install", help="Install a generated 2.x dev bundle into the experimental user-local footprint.")
    install_parser.add_argument("bundle", nargs="?", help="Path to a bundle directory or manifest.json.")
    install_parser.add_argument("--bundle-id", help="Install a bundle by id from the bundle root.")
    install_parser.add_argument(
        "--bundle-root",
        default=str(DEFAULT_BUNDLE_ROOT),
        help=f"Bundle lookup root. Defaults to {DEFAULT_BUNDLE_ROOT}.",
    )

    status_parser = subparsers.add_parser("status", help="Show the experimental 2.x user-local install state.")
    status_parser.add_argument(
        "--cwd",
        help="Override the cwd used for repo-local vs installed-dev reporting.",
    )

    uninstall_parser = subparsers.add_parser("uninstall", help="Remove one installed 2.x dev bundle from the experimental user-local footprint.")
    uninstall_parser.add_argument("bundle_id", help="Bundle id to remove from the experimental install root.")

    args = parser.parse_args(argv)

    if args.command == "bundle":
        payload = build_dev_bundle(
            args.profile,
            pack_id=args.pack_id,
            pack_profile_id=args.pack_profile_id,
            bundle_root=args.bundle_root,
            target_names=args.targets,
        )
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0 if payload["ok"] else 1

    if args.command == "install":
        payload = install_dev_bundle(
            args.bundle,
            bundle_id=args.bundle_id,
            bundle_root=args.bundle_root,
        )
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0 if payload["ok"] else 1

    if args.command == "status":
        payload = describe_install_state(cwd=Path(args.cwd).expanduser() if args.cwd else None)
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0

    payload = uninstall_dev_bundle(args.bundle_id)
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
