"""CLI for the experimental RetroFX 2.x bounded apply/off workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from v2.core.dev.profile_input import add_profile_selection_args

from .manager import apply_dev_profile, describe_current_activation, off_dev_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Experimental RetroFX 2.x bounded apply/off helpers. These commands are user-local, reversible, and do not replace the 1.x runtime.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    apply_parser = subparsers.add_parser("apply", help="Stage and activate a bounded 2.x experimental profile in the managed user-local active area.")
    add_profile_selection_args(apply_parser)
    apply_parser.add_argument(
        "--probe-x11",
        action="store_true",
        help="When eligible, run the explicit bounded X11 live probe in addition to staging the active bundle.",
    )
    apply_parser.add_argument(
        "--probe-seconds",
        type=float,
        default=3.0,
        help="Timeout for the explicit X11 live probe. Defaults to 3.0 seconds.",
    )

    off_parser = subparsers.add_parser("off", help="Clear the current 2.x experimental activation without touching 1.x or uninstalling bundles.")
    off_parser.add_argument(
        "--no-op-ok",
        action="store_true",
        help="Ignored compatibility flag; off already treats 'nothing active' as a clean no-op.",
    )

    status_parser = subparsers.add_parser("status", help="Show the current 2.x experimental activation and the user-local install footprint.")
    status_parser.add_argument("--cwd", help="Override the cwd used for repo-local vs installed-dev reporting.")

    args = parser.parse_args(argv)

    if args.command == "apply":
        payload = apply_dev_profile(
            args.profile,
            pack_id=args.pack_id,
            pack_profile_id=args.pack_profile_id,
            probe_x11=args.probe_x11,
            probe_seconds=args.probe_seconds,
        )
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0 if payload["ok"] else 1

    if args.command == "off":
        payload = off_dev_profile()
        print(json.dumps(payload, indent=2, sort_keys=False))
        return 0 if payload["ok"] else 1

    payload = describe_current_activation(cwd=Path(args.cwd).expanduser() if args.cwd else None)
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
