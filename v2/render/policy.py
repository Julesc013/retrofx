"""Display-policy interpretation helpers for the early 2.x render slice."""

from __future__ import annotations

from typing import Any, Mapping

DISPLAY_DEFAULTS = {
    "gamma": 1.0,
    "contrast": 1.0,
    "temperature": 6500,
    "black_lift": 0.0,
    "blue_light_reduction": 0.0,
    "tint_bias": None,
}

DISPLAY_FUTURE_CONSUMERS = {
    "gamma": "x11-render",
    "contrast": "x11-render",
    "temperature": "x11-render",
    "black_lift": "x11-render",
    "blue_light_reduction": "display-advisory",
    "tint_bias": "x11-render",
}


def has_non_default_display_policy(display_policy: Mapping[str, Any]) -> bool:
    return any(_is_requested(key, display_policy.get(key)) for key in DISPLAY_DEFAULTS)


def build_display_policy_summary(
    resolved_profile: Mapping[str, Any],
    environment: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    render = dict(resolved_profile.get("semantics", {}).get("render", {}))
    display = dict(render.get("display", {}))
    env = environment or {}
    session_type = str(env.get("session_type", "unknown-headless"))
    executables = dict(env.get("executables", {}))
    picom_available = bool(executables.get("picom"))
    x11_render_host_possible = session_type == "x11" and picom_available

    requested_fields: list[str] = []
    future_target_families: list[str] = []
    warnings: list[str] = []
    per_field: dict[str, Any] = {}

    for field_name, default_value in DISPLAY_DEFAULTS.items():
        value = display.get(field_name, default_value)
        requested = _is_requested(field_name, value)
        if requested:
            requested_fields.append(field_name)

        status, notes = _interpret_field(
            field_name=field_name,
            requested=requested,
            session_type=session_type,
            x11_render_host_possible=x11_render_host_possible,
        )
        future_target_family = DISPLAY_FUTURE_CONSUMERS[field_name]
        if requested and future_target_family not in future_target_families:
            future_target_families.append(future_target_family)
        if requested and status in {"advisory-export-only", "x11-render-export-only", "export-only-non-x11"}:
            warnings.append(
                f"`render.display.{field_name}` is preserved in the resolved model, but the detected `{session_type}` environment still keeps it export-oriented."
            )

        per_field[field_name] = {
            "value": value,
            "default": default_value,
            "requested": requested,
            "status": status,
            "future_target_family": future_target_family,
            "notes": notes,
        }

    overall_status = _overall_status(per_field, requested_fields)
    notes = [
        "Display policy is resolved independently from target-specific emission.",
        "Current TWO-17 support remains capability-aware and explicit; it does not mutate global display state.",
    ]
    if x11_render_host_possible:
        notes.append("The detected X11 environment has `picom`, so the experimental TWO-17 X11 render slice can consume these values during dev-only preview runs.")
    elif session_type == "x11":
        notes.append("The detected X11 environment lacks a known compositor host hint, so display policy remains export-only until `picom` is available.")
    elif session_type == "wayland":
        notes.append("The detected Wayland environment keeps display policy advisory until a truthful Wayland consumer exists.")
    elif session_type in {"tty", "remote-ssh", "unknown-headless"}:
        notes.append("The detected non-GUI environment keeps display policy as export metadata only.")

    return {
        "requested": {key: display.get(key, default) for key, default in DISPLAY_DEFAULTS.items()},
        "requested_fields": requested_fields,
        "overall_status": overall_status,
        "future_target_families": future_target_families,
        "environment_interpretation": {
            "session_type": session_type,
            "x11_render_host_possible": x11_render_host_possible,
            "picom_available": picom_available,
        },
        "per_field": per_field,
        "warnings": warnings,
        "notes": notes,
    }


def _interpret_field(
    *,
    field_name: str,
    requested: bool,
    session_type: str,
    x11_render_host_possible: bool,
) -> tuple[str, list[str]]:
    if not requested:
        return "default-no-op", ["Resolved value matches the schema default."]

    if session_type == "x11" and x11_render_host_possible:
        return "x11-render-live-preview-available", [
            "The TWO-17 X11 render slice can consume this field during dev-only shader preview in an X11 + picom session."
        ]

    if session_type == "x11":
        return "x11-render-export-only", [
            "This field is retained for exported X11 render artifacts, but live preview is unavailable until `picom` is present."
        ]

    if session_type in {"wayland", "tty", "remote-ssh", "unknown-headless"}:
        return "export-only-non-x11", [
            "This field is retained for exported artifacts, but the current environment has no truthful live X11 render path."
        ]

    return "advisory-export-only", [
        "This field is preserved in artifacts, but the detected environment has no truthful live display-policy path."
    ]


def _overall_status(per_field: Mapping[str, Any], requested_fields: list[str]) -> str:
    if not requested_fields:
        return "default-no-op"

    statuses = {str(per_field[field_name]["status"]) for field_name in requested_fields}
    if "x11-render-live-preview-available" in statuses:
        return "x11-render-live-preview-available"
    if statuses == {"x11-render-export-only"}:
        return "x11-render-export-only"
    if statuses == {"export-only-non-x11"}:
        return "export-only-non-x11"
    if statuses == {"advisory-export-only"}:
        return "advisory-export-only"
    return "mixed-advisory"


def _is_requested(field_name: str, value: Any) -> bool:
    default = DISPLAY_DEFAULTS[field_name]
    if default is None:
        return value is not None
    return value != default
