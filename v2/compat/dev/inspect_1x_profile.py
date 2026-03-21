"""Dev-only RetroFX 1.x compatibility inspection and draft migration output."""

from __future__ import annotations

import argparse
import json

from v2.compat import DEFAULT_MIGRATION_OUT_ROOT, inspect_legacy_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 migrate inspect-1x",
        description="Inspect a RetroFX 1.x profile and emit a deterministic 2.x migration report without changing the 1.x runtime.",
    )
    parser.add_argument("profile", help="Path to a RetroFX 1.x TOML profile.")
    parser.add_argument(
        "--write-draft",
        action="store_true",
        help="Write a generated 2.x draft profile bundle under v2/out/migrations/<profile-id>/.",
    )
    parser.add_argument(
        "--out-root",
        default=str(DEFAULT_MIGRATION_OUT_ROOT),
        help=f"Base output root for optional migration bundles. Defaults to {DEFAULT_MIGRATION_OUT_ROOT}.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of pretty-printed JSON.",
    )
    args = parser.parse_args(argv)

    payload = inspect_legacy_profile(args.profile, out_root=args.out_root, write_draft=args.write_draft)
    print(json.dumps(payload, indent=None if args.compact else 2, sort_keys=False))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
