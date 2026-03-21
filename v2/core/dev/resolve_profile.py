"""Dev-only profile resolver for the initial 2.x core scaffold."""

from __future__ import annotations

import argparse
import json
import sys

from v2.core.dev.profile_input import add_profile_selection_args, run_selected_profile_pipeline
from v2.core.pipeline import IMPLEMENTATION_INFO


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 resolve",
        description="Load, validate, normalize, and resolve a RetroFX 2.x profile in dev-only mode.",
    )
    add_profile_selection_args(parser)
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

    try:
        result = run_selected_profile_pipeline(
            profile=args.profile,
            pack_id=args.pack_id,
            pack_profile_id=args.pack_profile_id,
        )
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "load",
                    "implementation": IMPLEMENTATION_INFO,
                    "warnings": [],
                    "errors": [
                        {
                            "severity": "error",
                            "code": "invalid-profile-selector",
                            "message": str(exc),
                        }
                    ],
                },
                indent=2,
            )
        )
        return 2

    payload = result.to_dict(include_normalized=args.include_normalized)
    json_output = json.dumps(payload, indent=None if args.compact else 2, sort_keys=False)
    print(json_output)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
