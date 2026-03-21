"""Dev-only pack inspection for the experimental RetroFX 2.x scaffold."""

from __future__ import annotations

import argparse
import json

from v2.packs import PackLoadError, load_pack_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Show a local experimental RetroFX 2.x pack manifest and its profiles.",
    )
    parser.add_argument("pack_id", help="Pack id under v2/packs/.")
    args = parser.parse_args(argv)

    try:
        pack = load_pack_manifest(args.pack_id)
    except PackLoadError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "pack-inspection",
                    "errors": [exc.issue.to_dict()],
                },
                indent=2,
                sort_keys=False,
            )
        )
        return 1

    payload = {
        "ok": True,
        "stage": "pack-inspection",
        "pack": pack,
        "note": "This is a dev-only local pack inspection surface.",
    }
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
