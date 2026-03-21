"""Shared profile-selection helpers for dev-only 2.x entrypoints."""

from __future__ import annotations

import argparse

from v2.core.pipeline import run_pack_profile_pipeline, run_profile_pipeline


def add_profile_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "profile",
        nargs="?",
        help="Path to a RetroFX 2.x TOML profile. Optional when using --pack and --profile-id.",
    )
    parser.add_argument(
        "--pack",
        dest="pack_id",
        help="Resolve the profile from a built-in or local 2.x pack id instead of a direct path.",
    )
    parser.add_argument(
        "--profile-id",
        dest="pack_profile_id",
        help="Profile id inside the selected 2.x pack.",
    )


def run_selected_profile_pipeline(
    *,
    profile: str | None,
    pack_id: str | None,
    pack_profile_id: str | None,
):
    if pack_id or pack_profile_id:
        if not pack_id or not pack_profile_id:
            raise ValueError("Both --pack and --profile-id are required when using pack-aware resolution.")
        return run_pack_profile_pipeline(pack_id, pack_profile_id)

    if not profile:
        raise ValueError("Either a profile path or both --pack and --profile-id are required.")

    return run_profile_pipeline(profile)
