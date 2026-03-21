"""RetroFX 1.x -> 2.x compatibility inspection and draft migration output."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from v2.compat.legacy import LegacyProfileError, load_legacy_profile_document, normalize_legacy_profile
from v2.core.color_utils import darken, lighten
from v2.core.pipeline import run_profile_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MIGRATION_OUT_ROOT = REPO_ROOT / "v2" / "out"
IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-15",
    "surface": "legacy-1x-compatibility-inspection",
    "implemented": [
        "1.x profile intake",
        "subset mapping to 2.x draft profiles",
        "lossy and unsupported field reporting",
        "dev-only draft profile emission",
    ],
    "not_implemented": [
        "full runtime compatibility mode",
        "automatic in-place upgrade of 1.x profiles",
        "1.x pack install migration",
        "1.x session or runtime state migration",
        "lossless support for all legacy fields",
    ],
}
LEGACY_TO_V2_RULES = [
    {"legacy_field": "name", "target_field": "identity.name", "mapping_class": "clean", "note": "Direct copy."},
    {"legacy_field": "description", "target_field": "identity.description", "mapping_class": "clean", "note": "Direct copy."},
    {"legacy_field": "tags", "target_field": "identity.tags", "mapping_class": "clean", "note": "Direct copy."},
    {"legacy_field": "author", "target_field": "identity.author", "mapping_class": "clean", "note": "Direct copy."},
    {"legacy_field": "license", "target_field": "identity.license", "mapping_class": "clean", "note": "Direct copy."},
    {"legacy_field": "profile file basename", "target_field": "identity.id", "mapping_class": "degraded", "note": "Slug derived from the 1.x file name or source path."},
    {"legacy_field": "pack context or tags", "target_field": "identity.family", "mapping_class": "degraded", "note": "Family is inferred from legacy tags, mode, palette kind, or pack context."},
    {"legacy_field": "no direct 1.x field", "target_field": "identity.strictness", "mapping_class": "manual", "note": "Defaults to `modernized-retro` in the first migration slice."},
    {"legacy_field": "mode.type", "target_field": "render.mode", "mapping_class": "clean", "note": "Direct mapping for passthrough, monochrome, and palette."},
    {"legacy_field": "monochrome.bands", "target_field": "render.quantization.bands", "mapping_class": "clean", "note": "Direct mapping in monochrome mode."},
    {"legacy_field": "monochrome.phosphor/custom_rgb", "target_field": "color.semantic.*", "mapping_class": "degraded", "note": "Converted into semantic anchor colors and glow intent."},
    {"legacy_field": "monochrome.hotcore", "target_field": "render.effects.hotcore", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "palette.kind", "target_field": "render.palette.kind", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "palette.size", "target_field": "render.palette.size", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "palette.custom_file", "target_field": "render.palette.source", "mapping_class": "degraded", "note": "Converted to a dev-safe absolute source path when resolvable."},
    {"legacy_field": "effects.blur_strength", "target_field": "render.effects.blur", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "effects.scanlines", "target_field": "render.effects.scanlines", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "effects.flicker", "target_field": "render.effects.flicker", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "effects.dither", "target_field": "render.effects.dither", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "effects.vignette", "target_field": "render.effects.vignette", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "effects.scanline_preset", "target_field": None, "mapping_class": "manual", "note": "Not emitted in TWO-15; requires adapter-specific review."},
    {"legacy_field": "effects.transparency", "target_field": None, "mapping_class": "manual", "note": "Not emitted in TWO-15; remains backend-heavy."},
    {"legacy_field": "scope.x11", "target_field": "session.targets", "mapping_class": "degraded", "note": "Mapped to `x11` and compatibility target hints such as `wm` and `terminal`."},
    {"legacy_field": "scope.tty", "target_field": "session.targets", "mapping_class": "clean", "note": "Mapped to `tty` when enabled."},
    {"legacy_field": "scope.tuigreet", "target_field": "session.targets", "mapping_class": "clean", "note": "Mapped to `tuigreet` when enabled."},
    {"legacy_field": "fonts.tty", "target_field": "typography.console_font", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "fonts.terminal", "target_field": "typography.terminal_primary", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "fonts.terminal_fallback", "target_field": "typography.terminal_fallbacks", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "fonts.ui", "target_field": "typography.ui_sans", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "font_aa.antialias", "target_field": "typography.aa.antialias", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "font_aa.subpixel", "target_field": "typography.aa.subpixel", "mapping_class": "clean", "note": "Direct carry-over."},
    {"legacy_field": "colors.background", "target_field": "color.semantic.bg0", "mapping_class": "clean", "note": "Direct carry-over when present."},
    {"legacy_field": "colors.foreground", "target_field": "color.semantic.fg0", "mapping_class": "clean", "note": "Direct carry-over when present."},
    {"legacy_field": "rules.*", "target_field": None, "mapping_class": "unsupported", "note": "Not part of the first 2.x compatibility slice."},
]
PHOSPHOR_PRESETS = {
    "green": {"bg0": "#061008", "fg0": "#92ff84", "accent_primary": "#7dff70", "glow_tint": "#7dff70"},
    "amber": {"bg0": "#120b04", "fg0": "#ffcf82", "accent_primary": "#ffb347", "glow_tint": "#ffb347"},
    "blue": {"bg0": "#081018", "fg0": "#dff3ff", "accent_primary": "#8bc5ff", "glow_tint": "#8bc5ff"},
    "white": {"bg0": "#101010", "fg0": "#efefef", "accent_primary": "#d0d0d0", "glow_tint": "#d0d0d0"},
}
PALETTE_PRESETS = {
    "vga16": {"bg0": "#000000", "fg0": "#c0c0c0", "accent_primary": "#55ffff"},
    "cube32": {"bg0": "#111417", "fg0": "#d8dfe6", "accent_primary": "#6da7ff"},
    "cube64": {"bg0": "#111417", "fg0": "#d8dfe6", "accent_primary": "#6da7ff"},
    "cube128": {"bg0": "#111417", "fg0": "#d8dfe6", "accent_primary": "#6da7ff"},
    "cube256": {"bg0": "#111417", "fg0": "#d8dfe6", "accent_primary": "#6da7ff"},
    "mono2": {"bg0": "#000000", "fg0": "#e6e6e6", "accent_primary": "#e6e6e6"},
    "mono4": {"bg0": "#000000", "fg0": "#e6e6e6", "accent_primary": "#e6e6e6"},
    "mono8": {"bg0": "#000000", "fg0": "#e6e6e6", "accent_primary": "#e6e6e6"},
    "mono16": {"bg0": "#000000", "fg0": "#e6e6e6", "accent_primary": "#e6e6e6"},
    "custom": {"bg0": "#000000", "fg0": "#d0d0d0", "accent_primary": "#d0d0d0"},
}


def inspect_legacy_profile(
    profile_path: str | Path,
    *,
    out_root: str | Path | None = None,
    write_draft: bool = False,
) -> dict[str, Any]:
    try:
        legacy_document = load_legacy_profile_document(profile_path)
        normalized = normalize_legacy_profile(legacy_document)
    except LegacyProfileError as exc:
        return {
            "ok": False,
            "stage": "legacy-load",
            "implementation": IMPLEMENTATION_INFO,
            "source": {"requested_path": str(Path(profile_path).expanduser())},
            "warnings": [],
            "errors": [exc.issue.to_dict()],
            "migration_report": None,
            "emitted_bundle": None,
        }

    migration = _build_migration_report(normalized)
    emitted_bundle = None
    if write_draft:
        chosen_out_root = Path(out_root) if out_root is not None else DEFAULT_MIGRATION_OUT_ROOT
        emitted_bundle = _write_migration_bundle(migration, chosen_out_root)
        migration["draft_validation"] = emitted_bundle["draft_validation"]

    return {
        "ok": True,
        "stage": "migration-inspection",
        "implementation": IMPLEMENTATION_INFO,
        "source": normalized["source"],
        "warnings": migration["warnings"],
        "errors": [],
        "migration_report": migration,
        "emitted_bundle": emitted_bundle,
        "note": "This is a dev-only compatibility inspection surface. It does not replace the 1.x runtime.",
    }


def _build_migration_report(normalized: Mapping[str, Any]) -> dict[str, Any]:
    legacy = normalized["legacy_profile"]
    source = normalized["source"]

    clean: list[dict[str, Any]] = []
    degraded: list[dict[str, Any]] = []
    manual: list[dict[str, Any]] = []
    unsupported: list[dict[str, Any]] = list(normalized["unsupported_inputs"])
    warnings: list[str] = []

    def record(bucket: list[dict[str, Any]], legacy_field: str, target_field: str | None, value: Any, note: str) -> None:
        entry = {"legacy_field": legacy_field, "target_field": target_field, "value": value, "note": note}
        bucket.append(entry)

    profile_id = _slugify(Path(source["profile_path"]).stem)
    family, family_note = _infer_family(legacy, source["origin"])
    strictness = "modernized-retro"

    if source["origin"]["type"] == "legacy-pack-profile":
        record(
            degraded,
            "legacy pack path",
            "source.origin.legacy_pack",
            source["origin"]["legacy_pack"]["id"],
            "Legacy pack origin was inferred from the profile path.",
        )

    record(clean, "name", "identity.name", legacy["name"], "Direct metadata copy from the 1.x profile.")
    record(clean, "description", "identity.description", legacy["description"], "Direct metadata copy from the 1.x profile.")
    record(clean, "tags", "identity.tags", legacy["tags"], "Direct metadata copy from the 1.x profile.")
    record(clean, "author", "identity.author", legacy["author"], "Direct metadata copy from the 1.x profile.")
    record(clean, "license", "identity.license", legacy["license"], "Direct metadata copy from the 1.x profile.")
    record(degraded, "profile file basename", "identity.id", profile_id, "2.x stable ids are inferred from the legacy file name.")
    record(degraded, "tags / pack context", "identity.family", family, family_note)
    record(manual, "no direct 1.x field", "identity.strictness", strictness, "Strictness defaults to `modernized-retro`; review if the profile should be stricter or more practical.")

    identity = {
        "id": profile_id,
        "name": legacy["name"],
        "description": legacy["description"],
        "tags": legacy["tags"],
        "author": legacy["author"],
        "license": legacy["license"],
        "family": family,
        "strictness": strictness,
    }

    semantic = _build_semantic_colors(legacy, clean, degraded)
    render = _build_render_section(legacy, clean, degraded, manual, warnings)
    typography = _build_typography_section(legacy, clean, manual)
    session = _build_session_section(legacy, clean, degraded, manual)

    for entry in list(unsupported):
        if entry["legacy_field"].startswith("rules."):
            warnings.append("1.x `rules.*` fields are ignored in the first 2.x migration slice.")
            break

    if legacy["effects"]["scanline_preset"]:
        record(
            manual,
            "effects.scanline_preset",
            None,
            legacy["effects"]["scanline_preset"],
            "Scanline presets are not emitted in TWO-15; review this adapter-specific intent manually.",
        )
    if legacy["effects"]["transparency"]:
        record(
            manual,
            "effects.transparency",
            None,
            legacy["effects"]["transparency"],
            "Transparency mode remains backend-heavy and is not emitted in TWO-15.",
        )

    if not legacy["fonts"]["terminal"]:
        record(
            manual,
            "no direct 1.x field",
            "typography.terminal_primary",
            "monospace",
            "No `fonts.terminal` value was present, so 2.x will fall back to normal defaults.",
        )

    record(
        manual,
        "no direct 1.x field",
        "typography.aa.hinting",
        "default",
        "1.x had no explicit hinting field; the generated 2.x draft leaves hinting at the default.",
    )
    record(
        manual,
        "no direct 1.x field",
        "typography.ui_mono",
        typography.get("ui_mono", ""),
        "The first migration slice defaults `ui_mono` from the terminal font role when possible.",
    )

    draft_profile = {
        "schema": "retrofx.profile/v2alpha1",
        "identity": identity,
        "color": {"semantic": semantic},
        "typography": typography,
        "render": render,
        "session": session,
    }

    summary = {
        "mapped_cleanly": len(clean),
        "mapped_with_degradation": len(degraded),
        "requires_manual_follow_up": len(manual),
        "unsupported_or_ignored": len(unsupported),
    }

    return {
        "legacy_profile": {
            "name": legacy["name"],
            "version": legacy["version"],
            "mode": legacy["mode"]["type"],
            "description": legacy["description"],
            "tags": legacy["tags"],
            "sections_present": legacy["sections_present"],
            "origin": source["origin"],
        },
        "mapping_contract": {
            "source_schema": "retrofx.profile/v1",
            "target_schema": "retrofx.profile/v2alpha1",
            "mapping_rule_count": len(LEGACY_TO_V2_RULES),
        },
        "proposed_identity": {
            "id": identity["id"],
            "name": identity["name"],
            "family": identity["family"],
            "strictness": identity["strictness"],
        },
        "mapping_summary": summary,
        "mapped_cleanly": clean,
        "mapped_with_degradation": degraded,
        "requires_manual_follow_up": manual,
        "unsupported_or_ignored": unsupported,
        "warnings": warnings,
        "draft_profile": draft_profile,
        "draft_validation": None,
    }


def _build_semantic_colors(
    legacy: Mapping[str, Any],
    clean: list[dict[str, Any]],
    degraded: list[dict[str, Any]],
) -> dict[str, str]:
    colors = legacy["colors"]
    mode = legacy["mode"]["type"]

    if colors["background"]:
        bg0 = colors["background"]
        clean.append(
            {
                "legacy_field": "colors.background",
                "target_field": "color.semantic.bg0",
                "value": bg0,
                "note": "Direct 1.x color anchor mapping.",
            }
        )
    else:
        bg0 = _derive_default_bg0(legacy)
        degraded.append(
            {
                "legacy_field": "mode / phosphor / palette defaults",
                "target_field": "color.semantic.bg0",
                "value": bg0,
                "note": "2.x background anchor was derived because the 1.x profile did not set `colors.background`.",
            }
        )

    if colors["foreground"]:
        fg0 = colors["foreground"]
        clean.append(
            {
                "legacy_field": "colors.foreground",
                "target_field": "color.semantic.fg0",
                "value": fg0,
                "note": "Direct 1.x color anchor mapping.",
            }
        )
    else:
        fg0 = _derive_default_fg0(legacy)
        degraded.append(
            {
                "legacy_field": "mode / phosphor / palette defaults",
                "target_field": "color.semantic.fg0",
                "value": fg0,
                "note": "2.x foreground anchor was derived because the 1.x profile did not set `colors.foreground`.",
            }
        )

    semantic = {"bg0": bg0, "fg0": fg0}
    if mode == "monochrome":
        accent_primary = _derive_monochrome_accent(legacy, fg0)
        semantic["accent_primary"] = accent_primary
        semantic["glow_tint"] = accent_primary
        degraded.append(
            {
                "legacy_field": "monochrome.phosphor/custom_rgb",
                "target_field": "color.semantic.accent_primary",
                "value": accent_primary,
                "note": "Monochrome phosphor hue was converted into reusable 2.x semantic accent intent.",
            }
        )
    elif mode == "palette":
        accent_primary = _derive_palette_accent(legacy, fg0)
        semantic["accent_primary"] = accent_primary
        degraded.append(
            {
                "legacy_field": "palette.kind",
                "target_field": "color.semantic.accent_primary",
                "value": accent_primary,
                "note": "Palette mode was collapsed into a primary semantic accent for the draft 2.x profile.",
            }
        )

    return semantic


def _build_render_section(
    legacy: Mapping[str, Any],
    clean: list[dict[str, Any]],
    degraded: list[dict[str, Any]],
    manual: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    render = {
        "mode": legacy["mode"]["type"],
        "effects": {
            "blur": legacy["effects"]["blur_strength"],
            "dither": legacy["effects"]["dither"],
            "scanlines": legacy["effects"]["scanlines"],
            "flicker": legacy["effects"]["flicker"],
            "vignette": legacy["effects"]["vignette"],
            "hotcore": bool(legacy["monochrome"]["hotcore"]) if legacy["monochrome"] else False,
        },
    }

    clean.extend(
        [
            {"legacy_field": "mode.type", "target_field": "render.mode", "value": render["mode"], "note": "Direct mode mapping."},
            {"legacy_field": "effects.blur_strength", "target_field": "render.effects.blur", "value": render["effects"]["blur"], "note": "Direct effect mapping."},
            {"legacy_field": "effects.scanlines", "target_field": "render.effects.scanlines", "value": render["effects"]["scanlines"], "note": "Direct effect mapping."},
            {"legacy_field": "effects.flicker", "target_field": "render.effects.flicker", "value": render["effects"]["flicker"], "note": "Direct effect mapping."},
            {"legacy_field": "effects.dither", "target_field": "render.effects.dither", "value": render["effects"]["dither"], "note": "Direct effect mapping."},
            {"legacy_field": "effects.vignette", "target_field": "render.effects.vignette", "value": render["effects"]["vignette"], "note": "Direct effect mapping."},
        ]
    )

    if legacy["monochrome"]:
        render["quantization"] = {"bands": legacy["monochrome"]["bands"]}
        clean.append(
            {
                "legacy_field": "monochrome.bands",
                "target_field": "render.quantization.bands",
                "value": legacy["monochrome"]["bands"],
                "note": "Direct monochrome quantization mapping.",
            }
        )
        clean.append(
            {
                "legacy_field": "monochrome.hotcore",
                "target_field": "render.effects.hotcore",
                "value": legacy["monochrome"]["hotcore"],
                "note": "Direct hotcore effect mapping.",
            }
        )

    if legacy["palette"]:
        palette = legacy["palette"]
        source = palette["custom_file_absolute"] or palette["custom_file"]
        render["palette"] = {"kind": palette["kind"], "size": palette["size"]}
        clean.append(
            {
                "legacy_field": "palette.kind",
                "target_field": "render.palette.kind",
                "value": palette["kind"],
                "note": "Direct palette kind mapping.",
            }
        )
        clean.append(
            {
                "legacy_field": "palette.size",
                "target_field": "render.palette.size",
                "value": palette["size"],
                "note": "Direct palette size mapping.",
            }
        )

        if source:
            render["palette"]["source"] = source
            note = "Custom palette path was resolved to an absolute source path for safe draft emission." if palette["custom_file_absolute"] else "Custom palette path was preserved textually because it could not be resolved."
            degraded.append(
                {
                    "legacy_field": "palette.custom_file",
                    "target_field": "render.palette.source",
                    "value": source,
                    "note": note,
                }
            )
            if not palette["custom_file_absolute"]:
                warnings.append("Legacy custom palette path could not be resolved; review `render.palette.source` in the generated draft.")

    return render


def _build_typography_section(
    legacy: Mapping[str, Any],
    clean: list[dict[str, Any]],
    manual: list[dict[str, Any]],
) -> dict[str, Any]:
    fonts = legacy["fonts"]
    aa = legacy["font_aa"]
    typography: dict[str, Any] = {}

    if fonts["tty"]:
        typography["console_font"] = fonts["tty"]
        clean.append(
            {
                "legacy_field": "fonts.tty",
                "target_field": "typography.console_font",
                "value": fonts["tty"],
                "note": "Direct typography mapping.",
            }
        )
    if fonts["terminal"]:
        typography["terminal_primary"] = fonts["terminal"]
        clean.append(
            {
                "legacy_field": "fonts.terminal",
                "target_field": "typography.terminal_primary",
                "value": fonts["terminal"],
                "note": "Direct typography mapping.",
            }
        )
        typography["ui_mono"] = fonts["terminal"]
    if fonts["terminal_fallback"]:
        typography["terminal_fallbacks"] = fonts["terminal_fallback"]
        clean.append(
            {
                "legacy_field": "fonts.terminal_fallback",
                "target_field": "typography.terminal_fallbacks",
                "value": fonts["terminal_fallback"],
                "note": "Direct typography mapping.",
            }
        )
    if fonts["ui"]:
        typography["ui_sans"] = fonts["ui"]
        clean.append(
            {
                "legacy_field": "fonts.ui",
                "target_field": "typography.ui_sans",
                "value": fonts["ui"],
                "note": "Direct typography mapping.",
            }
        )

    if aa["antialias"] != "default" or aa["subpixel"] != "default":
        typography["aa"] = {"antialias": aa["antialias"], "subpixel": aa["subpixel"]}

    clean.append(
        {
            "legacy_field": "font_aa.antialias",
            "target_field": "typography.aa.antialias",
            "value": aa["antialias"],
            "note": "Direct font antialias mapping.",
        }
    )
    clean.append(
        {
            "legacy_field": "font_aa.subpixel",
            "target_field": "typography.aa.subpixel",
            "value": aa["subpixel"],
            "note": "Direct font subpixel mapping.",
        }
    )

    if "ui_mono" not in typography:
        manual.append(
            {
                "legacy_field": "no direct 1.x field",
                "target_field": "typography.ui_mono",
                "value": "",
                "note": "No terminal font was available to seed `ui_mono`; the 2.x normalizer will derive this later.",
            }
        )

    return typography


def _build_session_section(
    legacy: Mapping[str, Any],
    clean: list[dict[str, Any]],
    degraded: list[dict[str, Any]],
    manual: list[dict[str, Any]],
) -> dict[str, Any]:
    scope = legacy["scope"]
    targets: list[str] = []

    if scope["x11"]:
        for target in ("x11", "wm", "terminal"):
            if target not in targets:
                targets.append(target)
        degraded.append(
            {
                "legacy_field": "scope.x11",
                "target_field": "session.targets",
                "value": targets.copy(),
                "note": "2.x draft adds `x11`, `wm`, and `terminal` to preserve the broader 1.x X11 and export posture.",
            }
        )
    if scope["tty"]:
        targets.append("tty")
        clean.append(
            {
                "legacy_field": "scope.tty",
                "target_field": "session.targets",
                "value": "tty",
                "note": "Direct target-class mapping.",
            }
        )
    if scope["tuigreet"]:
        targets.append("tuigreet")
        clean.append(
            {
                "legacy_field": "scope.tuigreet",
                "target_field": "session.targets",
                "value": "tuigreet",
                "note": "Direct target-class mapping.",
            }
        )

    if targets:
        apply_mode = "current-session"
        persistence = "ephemeral"
    else:
        apply_mode = "export-only"
        persistence = "export-only"
        manual.append(
            {
                "legacy_field": "scope.*",
                "target_field": "session.apply_mode",
                "value": apply_mode,
                "note": "No legacy runtime scope was enabled, so the 2.x draft defaults to export-only posture.",
            }
        )

    manual.append(
        {
            "legacy_field": "implicit 1.x runtime posture",
            "target_field": "session.persistence",
            "value": persistence,
            "note": "2.x lifecycle policy is inferred because 1.x did not encode apply and persistence separately.",
        }
    )

    return {"targets": targets, "apply_mode": apply_mode, "persistence": persistence}


def _infer_family(legacy: Mapping[str, Any], origin: Mapping[str, Any]) -> tuple[str, str]:
    tags = {tag.lower() for tag in legacy["tags"]}
    mode = legacy["mode"]["type"]
    palette = legacy["palette"]
    monochrome = legacy["monochrome"]

    if "warm-night" in tags:
        return "warm-night", "Family was inferred from the legacy `warm-night` tag."
    if {"modern", "minimal"} & tags:
        return "modern-minimal", "Family was inferred from modern/minimal legacy tags."
    if "vfd" in tags or (monochrome and monochrome["phosphor"] == "custom" and "display" in tags):
        return "vfd", "Family was inferred from legacy VFD/custom display tags."
    if "crt" in tags or (monochrome and monochrome["phosphor"] in {"green", "amber", "blue"}):
        return "crt", "Family was inferred from legacy CRT tags or phosphor mode."
    if "dos" in tags or "vga16" in tags or (palette and palette["kind"] == "vga16"):
        return "dos", "Family was inferred from legacy DOS/VGA palette context."
    if "terminal" in tags or "unix" in tags or (palette and palette["kind"].startswith("cube")):
        return "terminal", "Family was inferred from terminal/unix palette context."
    if origin.get("type") == "legacy-pack-profile" and origin.get("legacy_pack", {}).get("id") == "core":
        return "custom", "Legacy pack context identified the core pack, but no stronger family hint was present."
    if mode == "passthrough":
        return "modern-minimal", "Passthrough legacy profiles default to a minimal modern family hint."
    return "custom", "No strong legacy family hint was available, so the draft uses `custom`."


def _derive_default_bg0(legacy: Mapping[str, Any]) -> str:
    if legacy["monochrome"]:
        phosphor = legacy["monochrome"]["phosphor"]
        if phosphor == "custom" and legacy["monochrome"]["custom_hex"]:
            return darken(legacy["monochrome"]["custom_hex"], 0.92)
        return PHOSPHOR_PRESETS.get(phosphor, PHOSPHOR_PRESETS["white"])["bg0"]
    if legacy["palette"]:
        return PALETTE_PRESETS.get(legacy["palette"]["kind"], PALETTE_PRESETS["custom"])["bg0"]
    return "#101010"


def _derive_default_fg0(legacy: Mapping[str, Any]) -> str:
    if legacy["monochrome"]:
        phosphor = legacy["monochrome"]["phosphor"]
        if phosphor == "custom" and legacy["monochrome"]["custom_hex"]:
            return legacy["monochrome"]["custom_hex"]
        return PHOSPHOR_PRESETS.get(phosphor, PHOSPHOR_PRESETS["white"])["fg0"]
    if legacy["palette"]:
        return PALETTE_PRESETS.get(legacy["palette"]["kind"], PALETTE_PRESETS["custom"])["fg0"]
    return "#efefef"


def _derive_monochrome_accent(legacy: Mapping[str, Any], fg0: str) -> str:
    if legacy["monochrome"]["phosphor"] == "custom" and legacy["monochrome"]["custom_hex"]:
        return lighten(legacy["monochrome"]["custom_hex"], 0.08)
    preset = PHOSPHOR_PRESETS.get(legacy["monochrome"]["phosphor"])
    return preset["accent_primary"] if preset else fg0


def _derive_palette_accent(legacy: Mapping[str, Any], fg0: str) -> str:
    preset = PALETTE_PRESETS.get(legacy["palette"]["kind"])
    return preset["accent_primary"] if preset else fg0


def _slugify(value: str) -> str:
    slug = []
    previous_dash = False
    for character in value.lower():
        if character.isalnum():
            slug.append(character)
            previous_dash = False
        else:
            if not previous_dash:
                slug.append("-")
                previous_dash = True
    return "".join(slug).strip("-") or "legacy-profile"


def _write_migration_bundle(migration: Mapping[str, Any], out_root: Path) -> dict[str, Any]:
    profile_id = migration["proposed_identity"]["id"]
    migration_root = out_root / "migrations" / profile_id
    migration_root.mkdir(parents=True, exist_ok=True)

    draft_path = migration_root / "draft-profile.toml"
    draft_content = _render_draft_profile_toml(migration["draft_profile"], migration["warnings"])
    draft_path.write_text(draft_content, encoding="utf-8")
    draft_validation = run_profile_pipeline(draft_path)

    report_payload = {
        "proposed_identity": migration["proposed_identity"],
        "mapping_summary": migration["mapping_summary"],
        "mapped_cleanly": migration["mapped_cleanly"],
        "mapped_with_degradation": migration["mapped_with_degradation"],
        "requires_manual_follow_up": migration["requires_manual_follow_up"],
        "unsupported_or_ignored": migration["unsupported_or_ignored"],
        "warnings": migration["warnings"],
        "draft_validation": draft_validation.to_dict(include_normalized=False),
    }
    report_content = json.dumps(report_payload, indent=2, sort_keys=False) + "\n"
    report_path = migration_root / "migration-report.json"
    report_path.write_text(report_content, encoding="utf-8")

    summary_content = _render_migration_summary(migration, draft_validation)
    summary_path = migration_root / "summary.txt"
    summary_path.write_text(summary_content, encoding="utf-8")

    return {
        "output_dir": str(migration_root),
        "artifacts": [
            _artifact_metadata(draft_path, draft_content),
            _artifact_metadata(report_path, report_content),
            _artifact_metadata(summary_path, summary_content),
        ],
        "draft_validation": draft_validation.to_dict(include_normalized=False),
    }


def _artifact_metadata(path: Path, content: str) -> dict[str, Any]:
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "file_name": path.name,
        "output_path": str(path),
        "content_sha256": digest,
        "byte_count": len(content.encode("utf-8")),
    }


def _render_migration_summary(migration: Mapping[str, Any], draft_validation: Any) -> str:
    lines = [
        "RetroFX 2.x Legacy Migration Summary",
        f"profile.id: {migration['proposed_identity']['id']}",
        f"profile.name: {migration['proposed_identity']['name']}",
        f"family: {migration['proposed_identity']['family']}",
        f"strictness: {migration['proposed_identity']['strictness']}",
        f"mapped_cleanly: {migration['mapping_summary']['mapped_cleanly']}",
        f"mapped_with_degradation: {migration['mapping_summary']['mapped_with_degradation']}",
        f"requires_manual_follow_up: {migration['mapping_summary']['requires_manual_follow_up']}",
        f"unsupported_or_ignored: {migration['mapping_summary']['unsupported_or_ignored']}",
        f"draft_validation_ok: {draft_validation.ok}",
        "",
    ]
    if migration["warnings"]:
        lines.append("warnings:")
        for warning in migration["warnings"]:
            lines.append(f"  - {warning}")
        lines.append("")
    if migration["requires_manual_follow_up"]:
        lines.append("manual_follow_up:")
        for entry in migration["requires_manual_follow_up"]:
            lines.append(f"  - {entry['legacy_field']}: {entry['note']}")
        lines.append("")
    if migration["unsupported_or_ignored"]:
        lines.append("unsupported_or_ignored:")
        for entry in migration["unsupported_or_ignored"]:
            lines.append(f"  - {entry['legacy_field']}: {entry['note']}")
        lines.append("")
    return "\n".join(lines)


def _render_draft_profile_toml(draft_profile: Mapping[str, Any], warnings: list[str]) -> str:
    lines = [
        "# RetroFX 2.x generated draft profile from a 1.x source.",
        "# Experimental dev-only migration output; review before using.",
    ]
    for warning in warnings:
        lines.append(f"# warning: {warning}")
    lines.append("")
    lines.append(f'schema = "{draft_profile["schema"]}"')
    lines.append("")

    _emit_table(lines, "identity", draft_profile["identity"], order=["id", "name", "description", "tags", "author", "license", "family", "strictness"])
    _emit_table(lines, "color.semantic", draft_profile["color"]["semantic"], order=["bg0", "bg1", "bg2", "fg0", "fg1", "fg2", "accent_primary", "accent_info", "accent_success", "accent_warn", "accent_error", "accent_muted", "border_active", "border_inactive", "selection_bg", "selection_fg", "glow_tint", "cursor", "cursor_text"])

    if draft_profile["typography"]:
        _emit_table(lines, "typography", draft_profile["typography"], order=["console_font", "terminal_primary", "terminal_fallbacks", "ui_sans", "ui_mono", "emoji_policy"])
        if "aa" in draft_profile["typography"]:
            _emit_table(lines, "typography.aa", draft_profile["typography"]["aa"], order=["antialias", "subpixel", "hinting"])

    _emit_table(lines, "render", draft_profile["render"], order=["mode"])
    if "quantization" in draft_profile["render"]:
        _emit_table(lines, "render.quantization", draft_profile["render"]["quantization"], order=["bands"])
    if "palette" in draft_profile["render"]:
        _emit_table(lines, "render.palette", draft_profile["render"]["palette"], order=["kind", "size", "source"])
    _emit_table(lines, "render.effects", draft_profile["render"]["effects"], order=["blur", "dither", "scanlines", "flicker", "vignette", "hotcore"])

    _emit_table(lines, "session", draft_profile["session"], order=["targets", "apply_mode", "persistence"])
    return "\n".join(lines).rstrip() + "\n"


def _emit_table(lines: list[str], name: str, mapping: Mapping[str, Any], *, order: list[str] | None = None) -> None:
    filtered_items = [(key, mapping[key]) for key in (order or list(mapping.keys())) if key in mapping and _include_in_toml(mapping[key])]
    if not filtered_items:
        return
    lines.append(f"[{name}]")
    for key, value in filtered_items:
        lines.append(f"{key} = {_toml_value(value)}")
    lines.append("")


def _include_in_toml(value: Any) -> bool:
    if value is None:
        return False
    if value == "":
        return False
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, Mapping):
        return any(_include_in_toml(item) for item in value.values())
    return True


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        rendered = f"{value:.6f}".rstrip("0").rstrip(".")
        return rendered if rendered else "0"
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    raise TypeError(f"Unsupported TOML value: {value!r}")
