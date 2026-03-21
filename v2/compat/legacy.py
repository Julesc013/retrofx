"""Legacy RetroFX 1.x profile intake for the experimental 2.x compatibility slice."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any, Mapping

from v2.core.color_utils import is_hex_color, normalize_hex_color, rgb_to_hex
from v2.core.models.types import Issue

REPO_ROOT = Path(__file__).resolve().parents[2]
KNOWN_ROOT_KEYS = {"name", "version", "description", "tags", "author", "license"}
KNOWN_SECTIONS: dict[str, set[str]] = {
    "mode": {"type"},
    "monochrome": {"bands", "phosphor", "custom_rgb", "hotcore"},
    "palette": {"kind", "size", "custom_file"},
    "effects": {"blur_strength", "scanlines", "flicker", "dither", "vignette", "scanline_preset", "transparency"},
    "scope": {"x11", "tty", "tuigreet"},
    "fonts": {"tty", "terminal", "terminal_fallback", "ui"},
    "font_aa": {"antialias", "subpixel"},
    "colors": {"background", "foreground"},
    "rules": set(),
}
ALLOWED_MODES = {"passthrough", "monochrome", "palette"}
ALLOWED_PHOSPHORS = {"green", "amber", "blue", "white", "custom"}
ALLOWED_PALETTE_KINDS = {"vga16", "mono2", "mono4", "mono8", "mono16", "cube32", "cube64", "cube128", "cube256", "custom"}
ALLOWED_DITHER = {"none", "ordered"}
ALLOWED_AA = {"default", "on", "off"}
ALLOWED_SUBPIXEL = {"default", "rgb", "bgr", "none"}
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


@dataclass(slots=True)
class LegacyProfileDocument:
    source_path: str
    source_dir: str
    origin: dict[str, Any]
    data: dict[str, Any]


class LegacyProfileError(Exception):
    """Raised when a 1.x profile cannot be loaded or normalized for migration."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(issue.message)
        self.issue = issue


def load_legacy_profile_document(path: str | Path) -> LegacyProfileDocument:
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="legacy-load-path-missing",
                message=f"1.x profile path does not exist or is not a file: {candidate}",
                path="source",
            )
        )

    resolved_path = candidate.resolve()
    try:
        with resolved_path.open("rb") as handle:
            data = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="legacy-toml-parse-error",
                message=str(exc),
                path="source",
            )
        ) from exc

    if not isinstance(data, dict):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="legacy-invalid-document",
                message="Loaded 1.x profile root is not a TOML table.",
                path="source",
            )
        )

    return LegacyProfileDocument(
        source_path=str(resolved_path),
        source_dir=str(resolved_path.parent),
        origin=_infer_legacy_origin(resolved_path),
        data=data,
    )


def normalize_legacy_profile(document: LegacyProfileDocument) -> dict[str, Any]:
    data = document.data
    unsupported_inputs = _collect_unsupported_inputs(data)

    name = _require_string(data.get("name"), "name")
    version = _normalize_version(data.get("version"))
    description = _optional_string(data.get("description"))
    tags = _normalize_tags(data.get("tags"))
    author = _optional_string(data.get("author"))
    license_name = _optional_string(data.get("license"))

    mode_table = _require_table(data, "mode")
    mode_type = _require_enum(mode_table.get("type"), "mode.type", ALLOWED_MODES)

    effects_table = _require_table(data, "effects")
    effects = {
        "blur_strength": _require_int_range(effects_table.get("blur_strength"), "effects.blur_strength", 0, 6),
        "scanlines": _require_bool(effects_table.get("scanlines"), "effects.scanlines"),
        "flicker": _require_bool(effects_table.get("flicker"), "effects.flicker"),
        "dither": _require_enum(effects_table.get("dither"), "effects.dither", ALLOWED_DITHER),
        "vignette": _require_bool(effects_table.get("vignette"), "effects.vignette"),
        "scanline_preset": _optional_string(effects_table.get("scanline_preset")),
        "transparency": _optional_string(effects_table.get("transparency")),
    }

    scope_table = _require_table(data, "scope")
    scope = {
        "x11": _require_bool(scope_table.get("x11"), "scope.x11"),
        "tty": _require_bool(scope_table.get("tty"), "scope.tty"),
        "tuigreet": _require_bool(scope_table.get("tuigreet"), "scope.tuigreet"),
    }

    monochrome = None
    if mode_type == "monochrome":
        mono_table = _require_table(data, "monochrome")
        phosphor = _require_enum(mono_table.get("phosphor"), "monochrome.phosphor", ALLOWED_PHOSPHORS)
        custom_rgb = _optional_string(mono_table.get("custom_rgb"))
        custom_hex = None
        if phosphor == "custom":
            if not custom_rgb:
                raise LegacyProfileError(
                    Issue(
                        severity="error",
                        code="missing-legacy-custom-rgb",
                        message="`monochrome.custom_rgb` is required when `monochrome.phosphor = \"custom\"`.",
                        path="monochrome.custom_rgb",
                    )
                )
            custom_hex = _normalize_rgb_triplet(custom_rgb)

        monochrome = {
            "bands": _require_int_range(mono_table.get("bands"), "monochrome.bands", 2, 256),
            "phosphor": phosphor,
            "custom_rgb": custom_rgb or None,
            "custom_hex": custom_hex,
            "hotcore": _require_bool(mono_table.get("hotcore"), "monochrome.hotcore"),
        }

    palette = None
    if mode_type == "palette":
        palette_table = _require_table(data, "palette")
        kind = _require_enum(palette_table.get("kind"), "palette.kind", ALLOWED_PALETTE_KINDS)
        size = _require_int_range(palette_table.get("size"), "palette.size", 2, 256)
        custom_file = _optional_string(palette_table.get("custom_file"))
        custom_file_absolute = None

        if kind == "custom":
            if not custom_file:
                raise LegacyProfileError(
                    Issue(
                        severity="error",
                        code="missing-legacy-custom-palette",
                        message="`palette.custom_file` is required when `palette.kind = \"custom\"`.",
                        path="palette.custom_file",
                    )
                )
            if size > 32:
                raise LegacyProfileError(
                    Issue(
                        severity="error",
                        code="legacy-custom-palette-size-too-large",
                        message="1.x custom palettes support size up to 32.",
                        path="palette.size",
                    )
                )

        if kind in STRUCTURED_PALETTE_SIZES and size != STRUCTURED_PALETTE_SIZES[kind]:
            raise LegacyProfileError(
                Issue(
                    severity="error",
                    code="legacy-palette-size-mismatch",
                    message=f"`palette.size` must be {STRUCTURED_PALETTE_SIZES[kind]} for `palette.kind = \"{kind}\"`.",
                    path="palette.size",
                )
            )

        if custom_file:
            resolved = (Path(document.source_dir) / custom_file).resolve()
            custom_file_absolute = str(resolved) if resolved.exists() else None

        palette = {
            "kind": kind,
            "size": size,
            "custom_file": custom_file or None,
            "custom_file_absolute": custom_file_absolute,
        }

    fonts_table = _optional_table(data, "fonts")
    fonts = {
        "tty": _optional_string(fonts_table.get("tty")) if fonts_table else "",
        "terminal": _optional_string(fonts_table.get("terminal")) if fonts_table else "",
        "terminal_fallback": _normalize_string_list(fonts_table.get("terminal_fallback"), "fonts.terminal_fallback")
        if fonts_table
        else [],
        "ui": _optional_string(fonts_table.get("ui")) if fonts_table else "",
    }

    aa_table = _optional_table(data, "font_aa")
    font_aa = {
        "antialias": _require_enum(aa_table.get("antialias"), "font_aa.antialias", ALLOWED_AA)
        if aa_table and "antialias" in aa_table
        else "default",
        "subpixel": _require_enum(aa_table.get("subpixel"), "font_aa.subpixel", ALLOWED_SUBPIXEL)
        if aa_table and "subpixel" in aa_table
        else "default",
    }

    colors_table = _optional_table(data, "colors")
    colors = {
        "background": _normalize_optional_hex(colors_table.get("background"), "colors.background") if colors_table else None,
        "foreground": _normalize_optional_hex(colors_table.get("foreground"), "colors.foreground") if colors_table else None,
    }

    rules_table = _optional_table(data, "rules")
    rules = dict(rules_table) if rules_table else {}

    return {
        "source": {
            "profile_path": document.source_path,
            "profile_dir": document.source_dir,
            "origin": document.origin,
        },
        "legacy_profile": {
            "name": name,
            "version": version,
            "description": description,
            "tags": tags,
            "author": author,
            "license": license_name,
            "mode": {"type": mode_type},
            "monochrome": monochrome,
            "palette": palette,
            "effects": effects,
            "scope": scope,
            "fonts": fonts,
            "font_aa": font_aa,
            "colors": colors,
            "rules": rules,
            "sections_present": sorted([key for key, value in data.items() if isinstance(value, Mapping)]),
        },
        "unsupported_inputs": unsupported_inputs,
    }


def _infer_legacy_origin(resolved_path: Path) -> dict[str, Any]:
    origin = {
        "type": "legacy-standalone-profile",
        "profile_path": str(resolved_path),
        "profile_dir": str(resolved_path.parent),
    }

    try:
        relative = resolved_path.relative_to(REPO_ROOT)
    except ValueError:
        return origin

    parts = relative.parts
    if len(parts) >= 4 and parts[0] == "profiles" and parts[1] == "packs":
        pack_id = parts[2]
        pack_root = REPO_ROOT / "profiles" / "packs" / pack_id
        origin["type"] = "legacy-pack-profile"
        origin["legacy_pack"] = {
            "id": pack_id,
            "root": str(pack_root),
            "profile_relative_path": str(Path(*parts[3:])),
        }
    return origin


def _collect_unsupported_inputs(data: Mapping[str, Any]) -> list[dict[str, Any]]:
    unsupported: list[dict[str, Any]] = []

    for key in sorted(data):
        value = data[key]
        if key in KNOWN_ROOT_KEYS:
            continue
        if key in KNOWN_SECTIONS:
            if not isinstance(value, Mapping):
                unsupported.append(
                    {
                        "legacy_field": key,
                        "status": "unsupported-input-shape",
                        "note": f"`[{key}]` was expected to be a table for compatibility inspection.",
                    }
                )
                continue

            allowed = KNOWN_SECTIONS[key]
            for section_key in sorted(value):
                if section_key not in allowed:
                    unsupported.append(
                        {
                            "legacy_field": f"{key}.{section_key}",
                            "status": "unsupported-or-ignored",
                            "note": "This 1.x field is not part of the first TWO-15 migration slice.",
                        }
                    )
            if key == "rules":
                for section_key in sorted(value):
                    unsupported.append(
                        {
                            "legacy_field": f"rules.{section_key}",
                            "status": "unsupported-or-ignored",
                            "note": "1.x rules remain unsupported in the first 2.x migration slice.",
                        }
                    )
            continue

        unsupported.append(
            {
                "legacy_field": key,
                "status": "unsupported-or-ignored",
                "note": "Unknown or unsupported 1.x top-level field.",
            }
        )

    return unsupported


def _require_table(data: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, Mapping):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="missing-legacy-table",
                message=f"`[{key}]` is required for this 1.x profile shape.",
                path=key,
            )
        )
    return value


def _optional_table(data: Mapping[str, Any], key: str) -> Mapping[str, Any] | None:
    value = data.get(key)
    return value if isinstance(value, Mapping) else None


def _require_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-string",
                message=f"`{path}` must be a non-empty string.",
                path=path,
            )
        )
    return value.strip()


def _normalize_version(value: Any) -> int:
    if value in {1, "1"}:
        return 1
    raise LegacyProfileError(
        Issue(
            severity="error",
            code="unsupported-legacy-version",
            message="Only RetroFX 1.x profile version `1` is supported by the first compatibility slice.",
            path="version",
        )
    )


def _optional_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def _normalize_tags(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-tags",
                message="`tags` must be an array of strings when provided.",
                path="tags",
            )
        )
    return sorted({item.strip() for item in value})


def _normalize_string_list(value: Any, path: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-string-list",
                message=f"`{path}` must be an array of non-empty strings.",
                path=path,
            )
        )
    return [item.strip() for item in value]


def _require_enum(value: Any, path: str, allowed: set[str]) -> str:
    normalized = _require_string(value, path).lower()
    if normalized not in allowed:
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-enum",
                message=f"`{path}` must be one of: {', '.join(sorted(allowed))}.",
                path=path,
            )
        )
    return normalized


def _require_int_range(value: Any, path: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, int):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-int",
                message=f"`{path}` must be an integer.",
                path=path,
            )
        )
    if value < minimum or value > maximum:
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-int-range",
                message=f"`{path}` must be in the range {minimum}..{maximum}.",
                path=path,
            )
        )
    return value


def _require_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-bool",
                message=f"`{path}` must be true or false.",
                path=path,
            )
        )
    return value


def _normalize_optional_hex(value: Any, path: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not is_hex_color(value):
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-color",
                message=f"`{path}` must be a hex color like `#rrggbb`.",
                path=path,
            )
        )
    return normalize_hex_color(value)


def _normalize_rgb_triplet(value: str) -> str:
    raw_parts = [part.strip() for part in value.split(",")]
    if len(raw_parts) != 3:
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-custom-rgb",
                message="`monochrome.custom_rgb` must contain three comma-separated channels.",
                path="monochrome.custom_rgb",
            )
        )

    numeric_parts: list[float] = []
    for part in raw_parts:
        try:
            numeric_parts.append(float(part))
        except ValueError as exc:
            raise LegacyProfileError(
                Issue(
                    severity="error",
                    code="invalid-legacy-custom-rgb",
                    message="`monochrome.custom_rgb` must contain numeric channels.",
                    path="monochrome.custom_rgb",
                )
            ) from exc

    if all(0.0 <= channel <= 1.0 for channel in numeric_parts):
        channels = [round(channel * 255.0) for channel in numeric_parts]
    elif all(0.0 <= channel <= 255.0 for channel in numeric_parts):
        channels = [round(channel) for channel in numeric_parts]
    else:
        raise LegacyProfileError(
            Issue(
                severity="error",
                code="invalid-legacy-custom-rgb-range",
                message="`monochrome.custom_rgb` channels must each be in 0..1 or 0..255.",
                path="monochrome.custom_rgb",
            )
        )

    return rgb_to_hex(channels)
