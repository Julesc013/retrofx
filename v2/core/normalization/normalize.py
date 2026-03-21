"""Normalization layer for the initial 2.x core scaffold."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from v2.core.color_utils import darken, lighten, mix_colors, normalize_hex_color, pick_best_contrast
from v2.core.models.types import NormalizationReport, NormalizedProfile, RawProfile
from v2.core.validation.validator import STRUCTURED_PALETTE_SIZES

FAMILY_COLOR_DEFAULTS = {
    "crt": {
        "accent_primary": "#7dff70",
        "accent_info": "#74ff68",
        "accent_success": "#7dff70",
        "accent_warn": "#d7e973",
        "accent_error": "#ff9c72",
    },
    "vfd": {
        "accent_primary": "#ffb347",
        "accent_info": "#ffd08a",
        "accent_success": "#ffc56b",
        "accent_warn": "#ffca75",
        "accent_error": "#ff8f6b",
    },
    "dos": {
        "accent_primary": "#55ffff",
        "accent_info": "#0000aa",
        "accent_success": "#00aa00",
        "accent_warn": "#aa5500",
        "accent_error": "#aa0000",
    },
    "modern-minimal": {
        "accent_primary": "#d0d0d0",
        "accent_info": "#c8c8c8",
        "accent_success": "#bababa",
        "accent_warn": "#c2c2c2",
        "accent_error": "#969696",
    },
    "warm-night": {
        "accent_primary": "#d9a066",
        "accent_info": "#8ab4c7",
        "accent_success": "#9ec48d",
        "accent_warn": "#d8b16a",
        "accent_error": "#c97b6b",
    },
    "terminal": {
        "accent_primary": "#79a6ff",
        "accent_info": "#6ac1e8",
        "accent_success": "#8dc891",
        "accent_warn": "#d7b16b",
        "accent_error": "#d17b7b",
    },
}

FAMILY_BLUR_DEFAULTS = {
    "crt": {"strict-authentic": 3, "modernized-retro": 2, "practical-daily-driver": 1},
    "vfd": {"strict-authentic": 2, "modernized-retro": 2, "practical-daily-driver": 1},
}

SEMANTIC_DEFAULT_KEYS = [
    "bg1",
    "bg2",
    "fg1",
    "fg2",
    "accent_primary",
    "accent_info",
    "accent_success",
    "accent_warn",
    "accent_error",
    "accent_muted",
    "border_active",
    "border_inactive",
    "selection_bg",
    "selection_fg",
    "glow_tint",
    "cursor",
    "cursor_text",
]

TERMINAL_SLOT_SOURCES = {
    "0": "bg0",
    "1": "accent_error",
    "2": "accent_success",
    "3": "accent_warn",
    "4": "accent_info",
    "5": "accent_primary",
    "6": "accent_muted",
    "7": "fg1",
    "8": "bg2",
    "9": "accent_error+bright",
    "10": "accent_success+bright",
    "11": "accent_warn+bright",
    "12": "accent_info+bright",
    "13": "accent_primary+bright",
    "14": "accent_muted+bright",
    "15": "fg0",
}

MONO_SLOT_LEVELS = {
    "0": 0.00,
    "1": 0.45,
    "2": 0.58,
    "3": 0.63,
    "4": 0.68,
    "5": 0.74,
    "6": 0.52,
    "7": 0.82,
    "8": 0.22,
    "9": 0.55,
    "10": 0.70,
    "11": 0.78,
    "12": 0.84,
    "13": 0.88,
    "14": 0.93,
    "15": 1.00,
}


def normalize_profile(raw_profile: RawProfile) -> NormalizedProfile:
    report = NormalizationReport()
    data = raw_profile.data

    identity = _normalize_identity(data.get("identity", {}))
    render = _normalize_render(data.get("render", {}), raw_profile, identity, report)
    color = _normalize_color(data.get("color", {}), identity, render, report)
    typography = _normalize_typography(data.get("typography", {}), report)
    chrome = _normalize_chrome(data.get("chrome", {}))
    session = _normalize_session(data.get("session", {}))

    normalized = {
        "schema": str(data.get("schema", "")).strip(),
        "source": {
            "profile_path": raw_profile.source_path,
            "profile_dir": raw_profile.source_dir,
            "origin": raw_profile.origin,
        },
        "identity": identity,
        "color": color,
        "typography": typography,
        "render": render,
        "chrome": chrome,
        "session": session,
        "compose": None,
        "normalization": report.to_dict(),
    }
    return NormalizedProfile(data=normalized, report=report)


def _normalize_identity(raw_identity: Any) -> dict[str, Any]:
    identity = raw_identity if isinstance(raw_identity, dict) else {}
    tags = identity.get("tags", [])
    if isinstance(tags, list):
        normalized_tags = _dedupe([str(tag).strip() for tag in tags if str(tag).strip()])
    else:
        normalized_tags = []

    return {
        "id": str(identity.get("id", "")).strip().lower(),
        "name": str(identity.get("name", "")).strip(),
        "description": str(identity.get("description", "")).strip(),
        "tags": normalized_tags,
        "author": str(identity.get("author", "")).strip(),
        "license": str(identity.get("license", "")).strip(),
        "family": str(identity.get("family", "custom")).strip().lower() or "custom",
        "strictness": str(identity.get("strictness", "modernized-retro")).strip().lower() or "modernized-retro",
    }


def _normalize_render(raw_render: Any, raw_profile: RawProfile, identity: dict[str, Any], report: NormalizationReport) -> dict[str, Any]:
    render = raw_render if isinstance(raw_render, dict) else {}
    mode = str(render.get("mode", "passthrough")).strip().lower() or "passthrough"

    quantization = render.get("quantization", {})
    quantization = quantization if isinstance(quantization, dict) else {}
    bands = quantization.get("bands")
    if mode == "monochrome" and bands is None:
        bands = 8
        report.notes.append("Defaulted `render.quantization.bands` to 8 for monochrome mode.")

    palette = render.get("palette", {})
    palette = palette if isinstance(palette, dict) else {}
    palette_kind = _lower_or_none(palette.get("kind"))
    palette_size = palette.get("size")
    if palette_size is None and palette_kind in STRUCTURED_PALETTE_SIZES:
        palette_size = STRUCTURED_PALETTE_SIZES[palette_kind]
        report.notes.append(f"Derived `render.palette.size` as {palette_size} from `render.palette.kind = \"{palette_kind}\"`.")

    palette_source = None
    if isinstance(palette.get("source"), str) and palette.get("source", "").strip():
        authored = palette["source"].strip()
        absolute = _normalize_path_like(authored, raw_profile, report)
        palette_source = {
            "authored": authored,
            "absolute": absolute,
        }

    effects = render.get("effects", {})
    effects = effects if isinstance(effects, dict) else {}
    effects_normalized = {
        "blur": effects.get("blur", _default_blur(identity["family"], identity["strictness"])),
        "dither": str(effects.get("dither", "none")).strip().lower() or "none",
        "scanlines": bool(effects.get("scanlines", False)),
        "flicker": bool(effects.get("flicker", False)),
        "vignette": bool(effects.get("vignette", False)),
        "hotcore": bool(effects.get("hotcore", False)),
    }

    display = render.get("display", {})
    display = display if isinstance(display, dict) else {}
    tint_bias = display.get("tint_bias")
    display_normalized = {
        "gamma": _normalize_float(display.get("gamma"), 1.0),
        "contrast": _normalize_float(display.get("contrast"), 1.0),
        "temperature": _normalize_int(display.get("temperature"), 6500),
        "black_lift": _normalize_float(display.get("black_lift"), 0.0),
        "blue_light_reduction": _normalize_float(display.get("blue_light_reduction"), 0.0),
        "tint_bias": normalize_hex_color(tint_bias) if isinstance(tint_bias, str) and tint_bias.strip() else None,
    }

    return {
        "mode": mode,
        "quantization": {"bands": bands},
        "palette": {
            "kind": palette_kind,
            "size": palette_size,
            "source": palette_source,
        },
        "effects": effects_normalized,
        "display": display_normalized,
    }


def _normalize_color(raw_color: Any, identity: dict[str, Any], render: dict[str, Any], report: NormalizationReport) -> dict[str, Any]:
    color = raw_color if isinstance(raw_color, dict) else {}
    semantic_raw = color.get("semantic", {})
    semantic_raw = semantic_raw if isinstance(semantic_raw, dict) else {}

    semantic: dict[str, str] = {}
    for key, value in semantic_raw.items():
        if isinstance(value, str) and value.strip():
            semantic[key] = normalize_hex_color(value)

    defaults = FAMILY_COLOR_DEFAULTS.get(identity["family"], {})

    semantic["bg0"] = semantic.get("bg0", "#000000")
    semantic["fg0"] = semantic.get("fg0", "#ffffff")
    semantic = _derive_semantic_defaults(semantic, defaults, render["mode"], report)

    terminal_overrides = _normalize_ansi_overrides(color.get("terminal"))
    terminal_ansi = _build_terminal_ansi(semantic, render, terminal_overrides, report)
    tty_overrides = _normalize_ansi_overrides(color.get("tty"))
    tty_ansi = _build_tty_ansi(terminal_ansi, tty_overrides, report)

    return {
        "semantic": semantic,
        "terminal": {"ansi": terminal_ansi},
        "tty": {"ansi": tty_ansi},
    }


def _derive_semantic_defaults(
    semantic: dict[str, str],
    family_defaults: dict[str, str],
    render_mode: str,
    report: NormalizationReport,
) -> dict[str, str]:
    if "bg1" not in semantic:
        semantic["bg1"] = lighten(semantic["bg0"], 0.08)
        report.derived_semantic_tokens.append("bg1")
    if "bg2" not in semantic:
        semantic["bg2"] = lighten(semantic["bg1"], 0.08)
        report.derived_semantic_tokens.append("bg2")
    if "fg1" not in semantic:
        semantic["fg1"] = mix_colors(semantic["fg0"], semantic["bg0"], 0.74)
        report.derived_semantic_tokens.append("fg1")
    if "fg2" not in semantic:
        semantic["fg2"] = mix_colors(semantic["fg0"], semantic["bg0"], 0.52)
        report.derived_semantic_tokens.append("fg2")

    accent_primary_missing = "accent_primary" not in semantic
    semantic["accent_primary"] = semantic.get("accent_primary", family_defaults.get("accent_primary", semantic["fg0"]))
    if accent_primary_missing:
        report.derived_semantic_tokens.append("accent_primary")

    for key in ("accent_info", "accent_success", "accent_warn", "accent_error"):
        if key not in semantic:
            semantic[key] = family_defaults.get(key, semantic["accent_primary"])
            report.derived_semantic_tokens.append(key)

    if "accent_muted" not in semantic:
        semantic["accent_muted"] = mix_colors(semantic["accent_primary"], semantic["bg1"], 0.55)
        report.derived_semantic_tokens.append("accent_muted")
    if "border_active" not in semantic:
        semantic["border_active"] = semantic["accent_muted"]
        report.derived_semantic_tokens.append("border_active")
    if "border_inactive" not in semantic:
        semantic["border_inactive"] = semantic["bg2"]
        report.derived_semantic_tokens.append("border_inactive")
    if "selection_bg" not in semantic:
        semantic["selection_bg"] = semantic["accent_primary"]
        report.derived_semantic_tokens.append("selection_bg")
    if "selection_fg" not in semantic:
        semantic["selection_fg"] = pick_best_contrast(semantic["selection_bg"], (semantic["bg0"], semantic["fg0"]))
        report.derived_semantic_tokens.append("selection_fg")
    if "glow_tint" not in semantic:
        semantic["glow_tint"] = semantic["fg0"] if render_mode == "monochrome" else semantic["accent_primary"]
        report.derived_semantic_tokens.append("glow_tint")
    if "cursor" not in semantic:
        semantic["cursor"] = semantic["fg0"]
        report.derived_semantic_tokens.append("cursor")
    if "cursor_text" not in semantic:
        semantic["cursor_text"] = pick_best_contrast(semantic["cursor"], (semantic["bg0"], semantic["fg0"]))
        report.derived_semantic_tokens.append("cursor_text")

    return semantic


def _normalize_ansi_overrides(container: Any) -> dict[str, str]:
    if not isinstance(container, dict):
        return {}
    ansi = container.get("ansi")
    if not isinstance(ansi, dict):
        return {}
    return {str(slot): normalize_hex_color(value) for slot, value in ansi.items() if isinstance(value, str)}


def _build_terminal_ansi(
    semantic: dict[str, str],
    render: dict[str, Any],
    overrides: dict[str, str],
    report: NormalizationReport,
) -> dict[str, str]:
    if render["mode"] == "monochrome":
        base = _monochrome_ansi_from_semantics(semantic, render["quantization"]["bands"] or 8)
        report.notes.append("Derived terminal ANSI palette from monochrome luminance bands.")
    else:
        base = {
            "0": semantic["bg0"],
            "1": semantic["accent_error"],
            "2": semantic["accent_success"],
            "3": semantic["accent_warn"],
            "4": semantic["accent_info"],
            "5": semantic["accent_primary"],
            "6": semantic["accent_muted"],
            "7": semantic["fg1"],
            "8": semantic["bg2"],
            "9": lighten(semantic["accent_error"], 0.18),
            "10": lighten(semantic["accent_success"], 0.18),
            "11": lighten(semantic["accent_warn"], 0.18),
            "12": lighten(semantic["accent_info"], 0.18),
            "13": lighten(semantic["accent_primary"], 0.18),
            "14": lighten(semantic["accent_muted"], 0.18),
            "15": semantic["fg0"],
        }
        report.notes.append("Derived terminal ANSI palette from semantic token mapping.")

    for slot in sorted(base, key=int):
        if slot not in overrides:
            report.derived_terminal_slots.append(slot)
    return {slot: overrides.get(slot, base[slot]) for slot in sorted(base, key=int)}


def _build_tty_ansi(terminal_ansi: dict[str, str], overrides: dict[str, str], report: NormalizationReport) -> dict[str, str]:
    for slot in sorted(terminal_ansi, key=int):
        if slot not in overrides:
            report.derived_tty_slots.append(slot)
    return {slot: overrides.get(slot, terminal_ansi[slot]) for slot in sorted(terminal_ansi, key=int)}


def _monochrome_ansi_from_semantics(semantic: dict[str, str], bands: int) -> dict[str, str]:
    band_count = max(2, min(16, int(bands)))

    def _band_color(level: float) -> str:
        band_index = round(level * (band_count - 1))
        band_level = band_index / (band_count - 1)
        return mix_colors(semantic["fg0"], semantic["bg0"], band_level)

    return {slot: _band_color(level) for slot, level in MONO_SLOT_LEVELS.items()}


def _normalize_typography(raw_typography: Any, report: NormalizationReport) -> dict[str, Any]:
    typography = raw_typography if isinstance(raw_typography, dict) else {}

    fallbacks = typography.get("terminal_fallbacks", [])
    if isinstance(fallbacks, str):
        fallback_list = [fallbacks.strip()] if fallbacks.strip() else []
    elif isinstance(fallbacks, list):
        fallback_list = [str(item).strip() for item in fallbacks if str(item).strip()]
    else:
        fallback_list = []

    aa = typography.get("aa", {})
    aa = aa if isinstance(aa, dict) else {}

    terminal_primary = _normalize_font_role(
        role_name="terminal_primary",
        authored_value=typography.get("terminal_primary"),
        default_value="monospace",
        report=report,
    )
    console_font = _normalize_font_role(
        role_name="console_font",
        authored_value=typography.get("console_font"),
        default_value=terminal_primary,
        report=report,
    )
    ui_sans = _normalize_font_role(
        role_name="ui_sans",
        authored_value=typography.get("ui_sans"),
        default_value="sans-serif",
        report=report,
    )
    ui_mono = _normalize_font_role(
        role_name="ui_mono",
        authored_value=typography.get("ui_mono"),
        default_value=terminal_primary,
        report=report,
    )
    icon_font = _normalize_font_role(
        role_name="icon_font",
        authored_value=typography.get("icon_font"),
        default_value="",
        report=report,
    )
    terminal_fallbacks = [value for value in _dedupe(fallback_list) if value and value != terminal_primary]
    terminal_stack = _dedupe([terminal_primary, *terminal_fallbacks])
    ui_mono_stack = _dedupe([ui_mono, terminal_primary, *terminal_fallbacks])
    report.derived_typography_roles.extend(
        [
            "terminal_stack",
            "ui_mono_stack",
            "fontconfig_aliases.monospace",
            "fontconfig_aliases.sans-serif",
        ]
    )

    return {
        "console_font": console_font,
        "terminal_primary": terminal_primary,
        "terminal_fallbacks": terminal_fallbacks,
        "terminal_stack": terminal_stack,
        "ui_sans": ui_sans,
        "ui_mono": ui_mono,
        "ui_mono_stack": ui_mono_stack,
        "icon_font": icon_font,
        "emoji_policy": str(typography.get("emoji_policy", "inherit")).strip().lower() or "inherit",
        "aa": {
            "antialias": str(aa.get("antialias", "default")).strip().lower() or "default",
            "subpixel": str(aa.get("subpixel", "default")).strip().lower() or "default",
            "hinting": str(aa.get("hinting", "default")).strip().lower() or "default",
        },
        "fontconfig_aliases": {
            "monospace": ui_mono_stack,
            "sans-serif": [ui_sans],
        },
    }


def _normalize_font_role(
    *,
    role_name: str,
    authored_value: Any,
    default_value: str,
    report: NormalizationReport,
) -> str:
    normalized = str(authored_value or "").strip()
    if normalized:
        return normalized

    if default_value:
        report.derived_typography_roles.append(role_name)
        report.notes.append(f"Defaulted `typography.{role_name}` to `{default_value}`.")
    return default_value


def _normalize_chrome(raw_chrome: Any) -> dict[str, Any]:
    chrome = raw_chrome if isinstance(raw_chrome, dict) else {}
    return {
        "gaps": chrome.get("gaps", 0),
        "bar_style": str(chrome.get("bar_style", "minimal")).strip().lower() or "minimal",
        "launcher_style": str(chrome.get("launcher_style", "minimal")).strip().lower() or "minimal",
        "notification_style": str(chrome.get("notification_style", "minimal")).strip().lower() or "minimal",
        "icon_theme": str(chrome.get("icon_theme", "")).strip(),
        "icon_variant": str(chrome.get("icon_variant", "")).strip(),
        "cursor_theme": str(chrome.get("cursor_theme", "")).strip(),
        "cursor_size": _normalize_int(chrome.get("cursor_size"), 24),
        "cursor_variant": str(chrome.get("cursor_variant", "")).strip(),
    }


def _normalize_session(raw_session: Any) -> dict[str, Any]:
    session = raw_session if isinstance(raw_session, dict) else {}
    targets_raw = session.get("targets", [])
    if isinstance(targets_raw, list):
        targets = _dedupe([str(target).strip().lower() for target in targets_raw if str(target).strip()])
    else:
        targets = []

    apply_mode = str(session.get("apply_mode", "current-session")).strip().lower() or "current-session"
    persistence = str(session.get("persistence", "")).strip().lower()
    if not persistence:
        persistence = {
            "current-session": "ephemeral",
            "installed-default": "installed",
            "export-only": "export-only",
            "explicit-only": "ephemeral",
        }.get(apply_mode, "ephemeral")

    return {
        "targets": targets,
        "apply_mode": apply_mode,
        "persistence": persistence,
    }


def _normalize_path_like(authored: str, raw_profile: RawProfile, report: NormalizationReport) -> str:
    authored_path = Path(authored).expanduser()
    if authored_path.is_absolute():
        absolute = authored_path.resolve()
    else:
        absolute = (Path(raw_profile.source_dir) / authored_path).resolve()
    report.path_normalizations.append({"authored": authored, "absolute": str(absolute)})
    return str(absolute)


def _normalize_float(value: Any, default: float) -> float:
    if isinstance(value, bool) or value is None:
        return default
    if isinstance(value, (int, float)):
        return round(float(value), 4)
    return default


def _normalize_int(value: Any, default: int) -> int:
    if isinstance(value, bool) or value is None:
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(round(value))
    return default


def _default_blur(family: str, strictness: str) -> int:
    return FAMILY_BLUR_DEFAULTS.get(family, {}).get(strictness, 0)


def _lower_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower() or None


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered
