"""Dev-only profile resolver for the initial 2.x core scaffold."""

from __future__ import annotations

import argparse
import json
import sys

from v2.core.pipeline import run_profile_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Load, validate, normalize, and resolve a RetroFX 2.x profile in dev-only mode.",
    )
    parser.add_argument("profile", help="Path to a RetroFX 2.x TOML profile.")
    parser.add_argument(
        "--include-normalized",
        action="store_true",
        help="Include the normalized profile in the JSON output.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of pretty-printed JSON.",
    )
    args = parser.parse_args(argv)

    result = run_profile_pipeline(args.profile)
    payload = result.to_dict(include_normalized=args.include_normalized)
    json_output = json.dumps(payload, indent=None if args.compact else 2, sort_keys=False)
    print(json_output)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

