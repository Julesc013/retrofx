"""Dev-only local pack discovery for the experimental RetroFX 2.x scaffold."""

from __future__ import annotations

import argparse
import json

from v2.packs import discover_packs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List the local experimental RetroFX 2.x packs available under v2/packs/.",
    )
    args = parser.parse_args(argv)
    _ = args

    packs = discover_packs()
    payload = {
        "ok": True,
        "stage": "pack-discovery",
        "packs": [
            {
                "id": pack["id"],
                "name": pack["name"],
                "description": pack["description"],
                "family": pack["family"],
                "tags": pack["tags"],
                "profile_count": len(pack["profiles"]),
                "profiles": [profile["id"] for profile in pack["profiles"]],
            }
            for pack in packs
        ],
        "note": "This is a dev-only local pack listing. It does not install or download anything.",
    }
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
