"""X11 render-policy helpers for the experimental 2.x render slice."""

from __future__ import annotations

from typing import Any, Mapping

from .policy import has_non_default_display_policy

SUPPORTED_X11_RENDER_MODES = {"passthrough", "monochrome", "palette"}
SUPPORTED_X11_PALETTE_KINDS = {"vga16"}


def compositor_required_for_render(render: Mapping[str, Any]) -> bool:
    effects = dict(render.get("effects", {}))
    if str(render.get("mode", "passthrough")) != "passthrough":
        return True
    if int(effects.get("blur", 0)) > 0:
        return True
    if str(effects.get("dither", "none")) != "none":
        return True
    if any(bool(effects.get(flag, False)) for flag in ("scanlines", "flicker", "vignette", "hotcore")):
        return True
    return has_non_default_display_policy(dict(render.get("display", {})))


def build_x11_render_summary(
    resolved_profile: Mapping[str, Any],
    environment: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    semantics = dict(resolved_profile.get("semantics", {}))
    render = dict(semantics.get("render", {}))
    palette = dict(render.get("palette", {}))
    effects = dict(render.get("effects", {}))
    display = dict(render.get("display", {}))

    env = environment or {}
    session_type = str(env.get("session_type", "unknown-headless"))
    executables = dict(env.get("executables", {}))
    picom_available = bool(executables.get("picom"))

    requested_mode = str(render.get("mode", "passthrough"))
    requested_palette_kind = palette.get("kind")
    implemented_mode = requested_mode
    degraded_fields: list[dict[str, str]] = []
    warnings: list[str] = []
    notes: list[str] = [
        "The TWO-17 X11 render slice is bounded on purpose: passthrough, monochrome, and `vga16` palette mode are implemented now.",
        "Live preview remains dev-only and only uses `picom` in the current session when explicitly requested.",
    ]

    if requested_mode == "palette" and requested_palette_kind not in SUPPORTED_X11_PALETTE_KINDS:
        implemented_mode = "passthrough"
        degraded_fields.append(
            {
                "path": "render.palette.kind",
                "requested": str(requested_palette_kind),
                "implemented_as": "passthrough",
                "reason": "TWO-17 only implements `vga16` as a real X11 palette-mode consumer.",
            }
        )
        warnings.append(
            f"`render.palette.kind = \"{requested_palette_kind}\"` is not implemented by the TWO-17 X11 shader path; shader generation degrades to passthrough."
        )

    compositor_required = compositor_required_for_render(render)
    artifacts_available = requested_mode in SUPPORTED_X11_RENDER_MODES
    live_preview_possible = session_type == "x11" and picom_available and artifacts_available
    export_only_reason = ""
    if session_type != "x11":
        export_only_reason = "The detected environment is not X11, so render artifacts remain export-only."
    elif not picom_available:
        export_only_reason = "The detected X11 environment does not appear to have `picom`, so live preview is unavailable."

    if live_preview_possible:
        overall_status = "x11-live-preview-available"
        notes.append("The current X11 session plus `picom` can host the experimental live preview path.")
    elif session_type == "x11":
        overall_status = "x11-export-only"
        warnings.append(export_only_reason)
    else:
        overall_status = "export-only-non-x11"
        if export_only_reason:
            warnings.append(export_only_reason)

    if degraded_fields:
        overall_status = "x11-compile-with-degradation" if session_type == "x11" else "export-only-with-degradation"

    supported_effects: list[str] = []
    if int(effects.get("blur", 0)) > 0:
        supported_effects.append("blur")
    if str(effects.get("dither", "none")) == "ordered":
        supported_effects.append("ordered-dither")
    for flag in ("scanlines", "flicker", "vignette", "hotcore"):
        if bool(effects.get(flag, False)):
            supported_effects.append(flag)

    return {
        "requested_mode": requested_mode,
        "implemented_mode": implemented_mode,
        "requested_palette_kind": requested_palette_kind,
        "requested_palette_size": palette.get("size"),
        "compositor_required": compositor_required,
        "artifacts_available": artifacts_available,
        "live_preview_possible": live_preview_possible,
        "export_only_reason": export_only_reason,
        "overall_status": overall_status,
        "supported_palette_kinds": sorted(SUPPORTED_X11_PALETTE_KINDS),
        "supported_effects_now": supported_effects,
        "degraded_fields": degraded_fields,
        "display_policy_consumed": has_non_default_display_policy(display) or requested_mode != "passthrough",
        "environment": {
            "session_type": session_type,
            "picom_available": picom_available,
        },
        "warnings": warnings,
        "notes": notes,
    }
