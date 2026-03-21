"""Validation primitives for the initial 2.x core scaffold."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from v2.core.color_utils import is_hex_color
from v2.core.models.types import Issue, NormalizedProfile, RawProfile

SUPPORTED_SCHEMA = "retrofx.profile/v2alpha1"
IDENTITY_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
ANSI_SLOT_KEYS = {str(slot) for slot in range(16)}
ALLOWED_STRICTNESS = {"strict-authentic", "modernized-retro", "practical-daily-driver"}
ALLOWED_RENDER_MODES = {"passthrough", "monochrome", "palette"}
ALLOWED_PALETTE_KINDS = {"vga16", "mono2", "mono4", "mono8", "mono16", "cube32", "cube64", "cube128", "cube256", "custom"}
ALLOWED_DITHER = {"none", "ordered"}
ALLOWED_EMOJI_POLICY = {"inherit", "monochrome", "color", "text-only"}
ALLOWED_AA = {"default", "on", "off"}
ALLOWED_SUBPIXEL = {"default", "rgb", "bgr", "vrgb", "vbgr", "none"}
ALLOWED_HINTING = {"default", "none", "slight", "medium", "full"}
ALLOWED_BAR_STYLE = {"minimal", "boxed", "dense", "hidden"}
ALLOWED_LAUNCHER_STYLE = {"minimal", "boxed", "dense", "fullscreen"}
ALLOWED_NOTIFICATION_STYLE = {"minimal", "boxed", "dense", "toast"}
ALLOWED_APPLY_MODE = {"current-session", "export-only", "installed-default", "explicit-only"}
ALLOWED_PERSISTENCE = {"ephemeral", "installed", "export-only"}
ALLOWED_TARGETS = {"tty", "tuigreet", "terminal", "tui", "x11", "wayland", "wm", "gtk", "qt", "icons", "cursors", "notifications", "launcher"}
KNOWN_FAMILIES = {"custom", "crt", "vfd", "dos", "modern-minimal", "warm-night", "terminal"}
STRUCTURED_PALETTE_SIZES = {
    "vga16": 16,
    "mono2": 2,
    "mono4": 4,
    "mono8": 8,
    "mono16": 16,
    "cube32": 32,
    "cube64": 64,
    "cube128": 128,
    "cube256": 256,
}

TOP_LEVEL_KEYS = {"schema", "identity", "color", "typography", "render", "chrome", "session", "compose"}
IDENTITY_KEYS = {"id", "name", "description", "tags", "author", "license", "family", "strictness"}
COLOR_KEYS = {"semantic", "terminal", "tty"}
SEMANTIC_KEYS = {
    "bg0",
    "bg1",
    "bg2",
    "fg0",
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
}
TERMINAL_COLOR_KEYS = {"ansi"}
TYPOGRAPHY_KEYS = {
    "console_font",
    "terminal_primary",
    "terminal_fallbacks",
    "ui_sans",
    "ui_mono",
    "icon_font",
    "emoji_policy",
    "aa",
}
TYPOGRAPHY_AA_KEYS = {"antialias", "subpixel", "hinting"}
RENDER_KEYS = {"mode", "quantization", "palette", "effects", "display"}
RENDER_QUANTIZATION_KEYS = {"bands"}
RENDER_PALETTE_KEYS = {"kind", "size", "source"}
RENDER_EFFECT_KEYS = {"blur", "dither", "scanlines", "flicker", "vignette", "hotcore"}
RENDER_DISPLAY_KEYS = {"gamma", "contrast", "temperature", "black_lift", "blue_light_reduction", "tint_bias"}
CHROME_KEYS = {"gaps", "bar_style", "launcher_style", "notification_style", "icon_theme", "cursor_theme"}
SESSION_KEYS = {"targets", "apply_mode", "persistence"}


def validate_raw_profile(raw_profile: RawProfile) -> tuple[list[Issue], list[Issue]]:
    errors: list[Issue] = []
    warnings: list[Issue] = []
    data = raw_profile.data

    _check_mapping_keys(data, TOP_LEVEL_KEYS, "", errors)

    if "compose" in data:
        errors.append(_error("compose", "unsupported-compose", "The `compose` section is reserved and not implemented yet."))

    schema = data.get("schema")
    if not isinstance(schema, str):
        errors.append(_error("schema", "missing-schema", "`schema` is required and must be a string."))
    elif schema != SUPPORTED_SCHEMA:
        errors.append(_error("schema", "unsupported-schema", f"`schema` must be `{SUPPORTED_SCHEMA}`."))

    identity = _require_table(data, "identity", errors)
    color = _require_table(data, "color", errors)
    semantic = _require_table(color, "semantic", errors, parent="color")

    if identity:
        _check_mapping_keys(identity, IDENTITY_KEYS, "identity", errors)
        _validate_identity(identity, errors, warnings)

    if color:
        _check_mapping_keys(color, COLOR_KEYS, "color", errors)
        _validate_color_sections(color, errors, warnings)

    if semantic:
        _check_mapping_keys(semantic, SEMANTIC_KEYS, "color.semantic", errors)
        _validate_semantic_colors(semantic, errors)

    typography = _optional_table(data, "typography", errors)
    if typography:
        _check_mapping_keys(typography, TYPOGRAPHY_KEYS, "typography", errors)
        _validate_typography(typography, errors)

    render = _optional_table(data, "render", errors)
    if render:
        _check_mapping_keys(render, RENDER_KEYS, "render", errors)
        _validate_render(render, errors)

    chrome = _optional_table(data, "chrome", errors)
    if chrome:
        _check_mapping_keys(chrome, CHROME_KEYS, "chrome", errors)
        _validate_chrome(chrome, errors)

    session = _optional_table(data, "session", errors)
    if session:
        _check_mapping_keys(session, SESSION_KEYS, "session", errors)
        _validate_session(session, errors, warnings)

    return errors, warnings


def validate_normalized_profile(normalized_profile: NormalizedProfile) -> tuple[list[Issue], list[Issue]]:
    errors: list[Issue] = []
    warnings: list[Issue] = []
    data = normalized_profile.data

    render = data["render"]
    session = data["session"]
    palette = render["palette"]

    if render["mode"] == "monochrome":
        bands = render["quantization"]["bands"]
        if bands is None or bands < 2:
            errors.append(_error("render.quantization.bands", "invalid-monochrome-bands", "Monochrome mode requires `render.quantization.bands >= 2`."))

    if render["mode"] == "palette":
        if palette["kind"] is None:
            errors.append(_error("render.palette.kind", "missing-palette-kind", "Palette mode requires `render.palette.kind`."))
        elif palette["kind"] == "custom" and palette["source"] is None:
            errors.append(_error("render.palette.source", "missing-custom-palette-source", "Custom palette mode requires `render.palette.source`."))
        elif palette["kind"] in STRUCTURED_PALETTE_SIZES:
            expected_size = STRUCTURED_PALETTE_SIZES[palette["kind"]]
            if palette["size"] != expected_size:
                errors.append(
                    _error(
                        "render.palette.size",
                        "palette-size-mismatch",
                        f"`render.palette.size` must be {expected_size} for `render.palette.kind = \"{palette['kind']}\"`.",
                    )
                )

    if not session["targets"] and session["apply_mode"] != "export-only":
        errors.append(
            _error(
                "session.targets",
                "missing-session-targets",
                "Non-export-only profiles must declare at least one `session.targets` entry.",
            )
        )

    if session["apply_mode"] == "export-only" and session["persistence"] != "export-only":
        errors.append(
            _error(
                "session.persistence",
                "invalid-export-persistence",
                "`session.apply_mode = \"export-only\"` requires `session.persistence = \"export-only\"`.",
            )
        )

    if session["apply_mode"] == "installed-default" and session["persistence"] == "ephemeral":
        errors.append(
            _error(
                "session.persistence",
                "invalid-installed-persistence",
                "`session.apply_mode = \"installed-default\"` cannot use ephemeral persistence.",
            )
        )

    return errors, warnings


def _validate_identity(identity: Mapping[str, Any], errors: list[Issue], warnings: list[Issue]) -> None:
    profile_id = identity.get("id")
    if not isinstance(profile_id, str) or not profile_id.strip():
        errors.append(_error("identity.id", "missing-identity-id", "`identity.id` is required and must be a non-empty string."))
    elif IDENTITY_ID_RE.match(profile_id.strip().lower()) is None:
        errors.append(
            _error(
                "identity.id",
                "invalid-identity-id",
                "`identity.id` must match `^[a-z0-9][a-z0-9-]{1,63}$`.",
            )
        )

    name = identity.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(_error("identity.name", "missing-identity-name", "`identity.name` is required and must be a non-empty string."))

    tags = identity.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or any(not isinstance(item, str) for item in tags):
            errors.append(_error("identity.tags", "invalid-tags", "`identity.tags` must be a list of strings when provided."))

    family = identity.get("family")
    if family is not None:
        if not isinstance(family, str):
            errors.append(_error("identity.family", "invalid-family", "`identity.family` must be a string when provided."))
        elif family.strip().lower() not in KNOWN_FAMILIES:
            warnings.append(
                Issue(
                    severity="warning",
                    code="unknown-family",
                    message=f"Unknown `identity.family` `{family}`; generic defaults will be used.",
                    path="identity.family",
                )
            )

    strictness = identity.get("strictness")
    if strictness is not None:
        _validate_enum("identity.strictness", strictness, ALLOWED_STRICTNESS, errors)


def _validate_color_sections(color: Mapping[str, Any], errors: list[Issue], warnings: list[Issue]) -> None:
    terminal = _optional_table(color, "terminal", errors, parent="color")
    tty = _optional_table(color, "tty", errors, parent="color")

    if terminal:
        _check_mapping_keys(terminal, TERMINAL_COLOR_KEYS, "color.terminal", errors)
        _validate_ansi_mapping(terminal.get("ansi"), "color.terminal.ansi", errors, warnings)

    if tty:
        _check_mapping_keys(tty, TERMINAL_COLOR_KEYS, "color.tty", errors)
        _validate_ansi_mapping(tty.get("ansi"), "color.tty.ansi", errors, warnings)


def _validate_semantic_colors(semantic: Mapping[str, Any], errors: list[Issue]) -> None:
    for required in ("bg0", "fg0"):
        value = semantic.get(required)
        path = f"color.semantic.{required}"
        if not isinstance(value, str):
            errors.append(_error(path, "missing-semantic-color", f"`{path}` is required and must be a hex color string."))
        elif not is_hex_color(value):
            errors.append(_error(path, "invalid-color", f"`{path}` must be a hex color like `#rrggbb`."))

    for key, value in semantic.items():
        if key in {"bg0", "fg0"}:
            continue
        path = f"color.semantic.{key}"
        if not isinstance(value, str):
            errors.append(_error(path, "invalid-color-type", f"`{path}` must be a string when provided."))
        elif not is_hex_color(value):
            errors.append(_error(path, "invalid-color", f"`{path}` must be a hex color like `#rrggbb`."))


def _validate_typography(typography: Mapping[str, Any], errors: list[Issue]) -> None:
    for key in ("console_font", "terminal_primary", "ui_sans", "ui_mono", "icon_font"):
        value = typography.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(_error(f"typography.{key}", "invalid-typography-value", f"`typography.{key}` must be a string when provided."))

    fallbacks = typography.get("terminal_fallbacks")
    if fallbacks is not None:
        if isinstance(fallbacks, str):
            pass
        elif not isinstance(fallbacks, list) or any(not isinstance(item, str) for item in fallbacks):
            errors.append(
                _error(
                    "typography.terminal_fallbacks",
                    "invalid-terminal-fallbacks",
                    "`typography.terminal_fallbacks` must be a string or list of strings when provided.",
                )
            )

    emoji_policy = typography.get("emoji_policy")
    if emoji_policy is not None:
        _validate_enum("typography.emoji_policy", emoji_policy, ALLOWED_EMOJI_POLICY, errors)

    aa = typography.get("aa")
    if aa is not None:
        if not isinstance(aa, Mapping):
            errors.append(_error("typography.aa", "invalid-aa-table", "`typography.aa` must be a table when provided."))
        else:
            _check_mapping_keys(aa, TYPOGRAPHY_AA_KEYS, "typography.aa", errors)
            if "antialias" in aa:
                _validate_enum("typography.aa.antialias", aa["antialias"], ALLOWED_AA, errors)
            if "subpixel" in aa:
                _validate_enum("typography.aa.subpixel", aa["subpixel"], ALLOWED_SUBPIXEL, errors)
            if "hinting" in aa:
                _validate_enum("typography.aa.hinting", aa["hinting"], ALLOWED_HINTING, errors)


def _validate_render(render: Mapping[str, Any], errors: list[Issue]) -> None:
    mode = render.get("mode")
    if mode is not None:
        _validate_enum("render.mode", mode, ALLOWED_RENDER_MODES, errors)

    quantization = render.get("quantization")
    if quantization is not None:
        if not isinstance(quantization, Mapping):
            errors.append(_error("render.quantization", "invalid-quantization-table", "`render.quantization` must be a table when provided."))
        else:
            _check_mapping_keys(quantization, RENDER_QUANTIZATION_KEYS, "render.quantization", errors)
            bands = quantization.get("bands")
            if bands is not None:
                _validate_int_range("render.quantization.bands", bands, 2, 256, errors)
                if isinstance(mode, str) and mode.strip().lower() == "passthrough":
                    errors.append(
                        _error(
                            "render.quantization.bands",
                            "passthrough-quantization-conflict",
                            "`render.quantization.bands` conflicts with `render.mode = \"passthrough\"`.",
                        )
                    )

    palette = render.get("palette")
    if palette is not None:
        if not isinstance(palette, Mapping):
            errors.append(_error("render.palette", "invalid-palette-table", "`render.palette` must be a table when provided."))
        else:
            _check_mapping_keys(palette, RENDER_PALETTE_KEYS, "render.palette", errors)
            kind = palette.get("kind")
            if kind is not None:
                _validate_enum("render.palette.kind", kind, ALLOWED_PALETTE_KINDS, errors)
                if isinstance(mode, str) and mode.strip().lower() != "palette":
                    errors.append(
                        _error(
                            "render.palette.kind",
                            "palette-mode-conflict",
                            "`render.palette.kind` cannot be authored unless `render.mode = \"palette\"`.",
                        )
                    )
            size = palette.get("size")
            if size is not None:
                _validate_int_range("render.palette.size", size, 2, 256, errors)
            source = palette.get("source")
            if source is not None and not isinstance(source, str):
                errors.append(_error("render.palette.source", "invalid-palette-source", "`render.palette.source` must be a string when provided."))

    effects = render.get("effects")
    if effects is not None:
        if not isinstance(effects, Mapping):
            errors.append(_error("render.effects", "invalid-effects-table", "`render.effects` must be a table when provided."))
        else:
            _check_mapping_keys(effects, RENDER_EFFECT_KEYS, "render.effects", errors)
            if "blur" in effects:
                _validate_int_range("render.effects.blur", effects["blur"], 0, 6, errors)
            if "dither" in effects:
                _validate_enum("render.effects.dither", effects["dither"], ALLOWED_DITHER, errors)
            for flag in ("scanlines", "flicker", "vignette", "hotcore"):
                if flag in effects and not isinstance(effects[flag], bool):
                    errors.append(_error(f"render.effects.{flag}", "invalid-effect-flag", f"`render.effects.{flag}` must be a boolean."))

    display = render.get("display")
    if display is not None:
        if not isinstance(display, Mapping):
            errors.append(_error("render.display", "invalid-display-table", "`render.display` must be a table when provided."))
        else:
            _check_mapping_keys(display, RENDER_DISPLAY_KEYS, "render.display", errors)
            if "gamma" in display:
                _validate_number_range("render.display.gamma", display["gamma"], 0.5, 2.0, errors)
            if "contrast" in display:
                _validate_number_range("render.display.contrast", display["contrast"], 0.5, 2.0, errors)
            if "temperature" in display:
                _validate_int_range("render.display.temperature", display["temperature"], 1000, 12000, errors)
            if "black_lift" in display:
                _validate_number_range("render.display.black_lift", display["black_lift"], -0.2, 0.2, errors)
            if "blue_light_reduction" in display:
                _validate_number_range("render.display.blue_light_reduction", display["blue_light_reduction"], 0.0, 1.0, errors)
            if "tint_bias" in display:
                tint_bias = display["tint_bias"]
                if not isinstance(tint_bias, str) or not is_hex_color(tint_bias):
                    errors.append(_error("render.display.tint_bias", "invalid-tint-bias", "`render.display.tint_bias` must be a hex color when provided."))


def _validate_chrome(chrome: Mapping[str, Any], errors: list[Issue]) -> None:
    if "gaps" in chrome:
        _validate_int_range("chrome.gaps", chrome["gaps"], 0, 64, errors)
    if "bar_style" in chrome:
        _validate_enum("chrome.bar_style", chrome["bar_style"], ALLOWED_BAR_STYLE, errors)
    if "launcher_style" in chrome:
        _validate_enum("chrome.launcher_style", chrome["launcher_style"], ALLOWED_LAUNCHER_STYLE, errors)
    if "notification_style" in chrome:
        _validate_enum("chrome.notification_style", chrome["notification_style"], ALLOWED_NOTIFICATION_STYLE, errors)
    for key in ("icon_theme", "cursor_theme"):
        if key in chrome and not isinstance(chrome[key], str):
            errors.append(_error(f"chrome.{key}", "invalid-chrome-string", f"`chrome.{key}` must be a string when provided."))


def _validate_session(session: Mapping[str, Any], errors: list[Issue], warnings: list[Issue]) -> None:
    targets = session.get("targets")
    if targets is not None:
        if not isinstance(targets, list) or any(not isinstance(item, str) for item in targets):
            errors.append(_error("session.targets", "invalid-session-targets", "`session.targets` must be a list of strings when provided."))
        else:
            normalized_targets = [item.strip().lower() for item in targets]
            invalid = sorted({item for item in normalized_targets if item not in ALLOWED_TARGETS})
            if invalid:
                errors.append(_error("session.targets", "invalid-session-target", f"Unsupported `session.targets` entries: {', '.join(invalid)}."))
            if "x11" in normalized_targets and "wayland" in normalized_targets:
                warnings.append(
                    Issue(
                        severity="warning",
                        code="mixed-session-targets",
                        message="`session.targets` includes both `x11` and `wayland`; runtime selection will remain environment-dependent.",
                        path="session.targets",
                    )
                )

    if "apply_mode" in session:
        _validate_enum("session.apply_mode", session["apply_mode"], ALLOWED_APPLY_MODE, errors)
    if "persistence" in session:
        _validate_enum("session.persistence", session["persistence"], ALLOWED_PERSISTENCE, errors)


def _validate_ansi_mapping(value: Any, path: str, errors: list[Issue], warnings: list[Issue]) -> None:
    if value is None:
        return
    if not isinstance(value, Mapping):
        errors.append(_error(path, "invalid-ansi-table", f"`{path}` must be a table when provided."))
        return

    invalid_keys = sorted(str(key) for key in value.keys() if str(key) not in ANSI_SLOT_KEYS)
    for invalid_key in invalid_keys:
        errors.append(_error(f"{path}.{invalid_key}", "invalid-ansi-slot", f"`{path}` slot keys must be strings `0..15`."))

    for key, slot_value in value.items():
        slot_path = f"{path}.{key}"
        if not isinstance(slot_value, str) or not is_hex_color(slot_value):
            errors.append(_error(slot_path, "invalid-color", f"`{slot_path}` must be a hex color like `#rrggbb`."))

    if value and len(value) < 16:
        warnings.append(
            Issue(
                severity="warning",
                code="partial-ansi-overrides",
                message=f"`{path}` overrides only {len(value)} slots; remaining slots will derive from semantic mapping.",
                path=path,
            )
        )


def _validate_enum(path: str, value: Any, allowed: set[str], errors: list[Issue]) -> None:
    if not isinstance(value, str) or value.strip().lower() not in allowed:
        errors.append(_error(path, "invalid-enum", f"`{path}` must be one of: {', '.join(sorted(allowed))}."))


def _validate_int_range(path: str, value: Any, minimum: int, maximum: int, errors: list[Issue]) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or value > maximum:
        errors.append(_error(path, "invalid-int-range", f"`{path}` must be an integer in the range {minimum}..{maximum}."))


def _validate_number_range(path: str, value: Any, minimum: float, maximum: float, errors: list[Issue]) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < minimum or value > maximum:
        errors.append(_error(path, "invalid-number-range", f"`{path}` must be a number in the range {minimum}..{maximum}."))


def _check_mapping_keys(mapping: Mapping[str, Any], allowed: set[str], parent: str, errors: list[Issue]) -> None:
    for key in mapping:
        if key not in allowed:
            path = f"{parent}.{key}" if parent else key
            errors.append(_error(path, "unknown-key", f"Unknown key `{path}`."))


def _require_table(container: Mapping[str, Any], key: str, errors: list[Issue], *, parent: str = "") -> Mapping[str, Any]:
    value = container.get(key)
    path = f"{parent}.{key}" if parent else key
    if value is None:
        errors.append(_error(path, "missing-table", f"Missing required table `{path}`."))
        return {}
    if not isinstance(value, Mapping):
        errors.append(_error(path, "invalid-table", f"`{path}` must be a table."))
        return {}
    return value


def _optional_table(container: Mapping[str, Any], key: str, errors: list[Issue], *, parent: str = "") -> Mapping[str, Any] | None:
    value = container.get(key)
    path = f"{parent}.{key}" if parent else key
    if value is None:
        return None
    if not isinstance(value, Mapping):
        errors.append(_error(path, "invalid-table", f"`{path}` must be a table."))
        return None
    return value


def _error(path: str, code: str, message: str) -> Issue:
    return Issue(severity="error", code=code, message=message, path=path)
