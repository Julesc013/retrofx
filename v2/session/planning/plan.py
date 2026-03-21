"""Capability-aware session planning for the early 2.x dev scaffold."""

from __future__ import annotations

from typing import Any, Mapping

from v2.render import build_display_policy_summary, build_x11_render_summary
from v2.targets import TARGET_COMPILERS, list_target_families, list_targets
from v2.targets.toolkit.common import build_toolkit_style_summary

TARGET_RULES = {
    "alacritty": {
        "preferred_session_types": {"tty", "x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "fontconfig": {
        "preferred_session_types": {"x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "gtk-export": {
        "preferred_session_types": {"x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "qt-export": {
        "preferred_session_types": {"x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "icon-cursor": {
        "preferred_session_types": {"x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "desktop-style": {
        "preferred_session_types": {"x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "kitty": {
        "preferred_session_types": {"tty", "x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "tmux": {
        "preferred_session_types": {"tty", "x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "vim": {
        "preferred_session_types": {"tty", "x11", "wayland", "remote-ssh"},
        "apply_preview_session_types": set(),
    },
    "xresources": {
        "preferred_session_types": {"x11"},
        "apply_preview_session_types": {"x11"},
    },
    "x11-display-policy": {
        "preferred_session_types": {"x11", "wayland"},
        "apply_preview_session_types": set(),
    },
    "x11-picom": {
        "preferred_session_types": {"x11"},
        "apply_preview_session_types": {"x11"},
        "requires_executables": {"picom"},
    },
    "x11-render-runtime": {
        "preferred_session_types": {"x11"},
        "apply_preview_session_types": {"x11"},
        "requires_executables": {"picom"},
    },
    "x11-shader": {
        "preferred_session_types": {"x11"},
        "apply_preview_session_types": set(),
    },
    "i3": {
        "preferred_session_types": {"x11"},
        "apply_preview_session_types": {"x11"},
        "apply_preview_wm_or_de": {"i3"},
    },
    "sway": {
        "preferred_session_types": {"wayland"},
        "apply_preview_session_types": {"wayland"},
        "apply_preview_wm_or_de": {"sway"},
    },
    "waybar": {
        "preferred_session_types": {"wayland"},
        "apply_preview_session_types": set(),
    },
}

FUTURE_ONLY_HINTS = {
    "tty": "TTY target compilers are not implemented yet in 2.x.",
    "tuigreet": "Tuigreet/login target compilers are not implemented yet in 2.x.",
    "notifications": "Notification targets are not implemented yet in 2.x.",
    "launcher": "Launcher targets are not implemented yet in 2.x.",
}


def build_session_plan(resolved_profile: Mapping[str, Any], environment: Mapping[str, Any]) -> dict[str, Any]:
    requested_target_classes = list(resolved_profile["semantics"]["session"]["requested_targets"])
    apply_mode = str(resolved_profile["semantics"]["session"]["apply_mode"])
    persistence = str(resolved_profile["semantics"]["session"]["persistence"])
    render_mode = str(resolved_profile["semantics"]["render"]["mode"])
    display_policy = build_display_policy_summary(resolved_profile, environment)
    x11_render = build_x11_render_summary(resolved_profile, environment)
    toolkit_style = build_toolkit_style_summary(resolved_profile, environment)
    implemented_families = list_target_families()
    implemented_targets = list_targets()
    implemented_target_classes = sorted(
        {
            target_class
            for compiler in TARGET_COMPILERS.values()
            for target_class in getattr(compiler, "supported_target_classes", ())
        }
    )

    family_entries: dict[str, list[dict[str, Any]]] = {}
    target_entries: list[dict[str, Any]] = []
    compile_targets: list[str] = []
    export_only_targets: list[str] = []
    apply_preview_targets: list[str] = []
    degraded_targets: list[str] = []
    skipped_targets: list[dict[str, Any]] = []
    warnings: list[str] = []
    notes: list[str] = [
        "TWO-18 planning is preview-only and does not mutate the current session unless the explicit dev-only X11 live probe is requested.",
        "Capability filtering currently reasons over implemented target families only.",
    ]

    for target_name in implemented_targets:
        compiler = TARGET_COMPILERS[target_name]
        requested_by = sorted(set(requested_target_classes).intersection(getattr(compiler, "supported_target_classes", ())))
        if not requested_by:
            continue

        entry = _build_target_entry(
            target_name=target_name,
            compiler=compiler,
            requested_by=requested_by,
            environment=environment,
            apply_mode=apply_mode,
            x11_render=x11_render,
        )
        target_entries.append(entry)
        family_entries.setdefault(entry["family_name"], []).append(entry)

        if entry["plan_action"] == "compile-and-export":
            compile_targets.append(target_name)
            export_only_targets.append(target_name)
        elif entry["plan_action"] == "compile-and-apply-preview":
            compile_targets.append(target_name)
            apply_preview_targets.append(target_name)
        elif entry["plan_action"] == "compile-but-degraded":
            compile_targets.append(target_name)
            degraded_targets.append(target_name)
        elif entry["plan_action"] == "skipped-unsupported":
            skipped_targets.append(entry)

        warnings.extend(entry["warnings"])

    for requested_class in requested_target_classes:
        if requested_class in implemented_target_classes:
            continue
        skipped_entry = {
            "kind": "requested-target-class",
            "requested_target_class": requested_class,
            "status_class": "unsupported",
            "plan_action": "skipped-unsupported",
            "reason": FUTURE_ONLY_HINTS.get(
                requested_class,
                f"No implemented 2.x target compilers currently satisfy requested target class `{requested_class}`.",
            ),
        }
        skipped_targets.append(skipped_entry)
        warnings.append(skipped_entry["reason"])

    if render_mode != "passthrough":
        warnings.append(
            "Resolved render intent is present and TWO-17 can now emit bounded X11 render artifacts, but live preview remains explicit and experimental."
        )
    if environment["session_type"] == "wayland" and environment["wm_or_de"] in {"gnome", "plasma", "unknown"}:
        warnings.append(
            f"Wayland `{environment['wm_or_de']}` sessions are not part of the currently validated broader-alpha set; treat GUI-facing outputs here as export-oriented validation only."
        )
    if display_policy["requested_fields"]:
        warnings.extend(display_policy["warnings"])
    warnings.extend(x11_render["warnings"])
    warnings.extend(toolkit_style["warnings"])

    if apply_mode != "export-only":
        warnings.append(
            f"`session.apply_mode = \"{apply_mode}\"` is previewed only; live apply/install orchestration is still not implemented beyond the dev-only X11 probe path and export-only toolkit artifacts."
        )

    environment_capabilities = _summarize_environment_capabilities(environment)

    family_plan_summary = {
        family_name: {
            "targets": [entry["target_name"] for entry in entries],
            "plan_actions": [entry["plan_action"] for entry in entries],
        }
        for family_name, entries in sorted(family_entries.items())
    }

    return {
        "requested_targets": requested_target_classes,
        "implemented_targets": implemented_targets,
        "implemented_target_families": implemented_families,
        "implemented_target_classes": implemented_target_classes,
        "session_policy": {
            "apply_mode": apply_mode,
            "persistence": persistence,
        },
        "display_policy": display_policy,
        "x11_render": x11_render,
        "toolkit_style": toolkit_style,
        "environment_capabilities": environment_capabilities,
        "family_plans": family_plan_summary,
        "target_entries": target_entries,
        "compile_targets": compile_targets,
        "export_only_targets": export_only_targets,
        "apply_preview_targets": apply_preview_targets,
        "degraded_targets": degraded_targets,
        "skipped_targets": skipped_targets,
        "warnings": _dedupe(warnings),
        "notes": notes,
    }


def _build_target_entry(
    *,
    target_name: str,
    compiler: Any,
    requested_by: list[str],
    environment: Mapping[str, Any],
    apply_mode: str,
    x11_render: Mapping[str, Any],
) -> dict[str, Any]:
    rules = TARGET_RULES[target_name]
    session_type = str(environment["session_type"])
    wm_or_de = str(environment["wm_or_de"])
    executables = dict(environment.get("executables", {}))
    reasons: list[str] = []
    warnings: list[str] = []
    plan_action = "compile-and-export"
    status_class = "export-only"

    aligned = session_type in rules["preferred_session_types"]
    if not aligned:
        plan_action = "compile-but-degraded"
        status_class = "partial"
        reasons.append(
            f"Current environment `{session_type}` is not the preferred live context for target `{target_name}`, so the plan stays as a degraded export preview."
        )
    else:
        reasons.append(f"Target `{target_name}` is meaningful in the detected `{session_type}` environment.")

    missing_executables = sorted(name for name in rules.get("requires_executables", set()) if not executables.get(name))
    if missing_executables:
        reasons.append(
            f"Missing executable prerequisites for live preview: {', '.join(missing_executables)}."
        )
        warnings.append(
            f"Target `{target_name}` remains export-only because required executable(s) are unavailable: {', '.join(missing_executables)}."
        )

    if apply_mode == "current-session":
        if _can_preview_apply_now(rules, session_type, wm_or_de) and not missing_executables:
            plan_action = "compile-and-apply-preview"
            status_class = "partial"
            reasons.append("This target would be a current-session apply candidate once live orchestration exists.")
            warnings.append("Preview only: TWO-17 only supports an explicit dev-only X11 live probe and does not take over the current session.")
        elif aligned:
            warnings.append(
                "Current-session intent is requested, but this target remains export-only until live session orchestration exists."
            )
    elif apply_mode in {"installed-default", "explicit-only"} and aligned:
        warnings.append(
            f"`session.apply_mode = \"{apply_mode}\"` is not implemented; this target remains an export-only preview in TWO-17."
        )

    if target_name in {"i3", "sway", "waybar"} and session_type not in {"x11", "wayland"}:
        warnings.append("WM targets can be generated here, but the current environment does not look like a live GUI WM session.")

    if target_name in {"x11-shader", "x11-picom", "x11-render-runtime"}:
        reasons.append(
            f"Requested render mode `{x11_render['requested_mode']}` currently compiles as `{x11_render['implemented_mode']}` in the bounded TWO-17 X11 slice."
        )
        if x11_render["degraded_fields"]:
            plan_action = "compile-but-degraded"
            status_class = "partial"
            warnings.extend(
                f"{degraded['path']} degraded from `{degraded['requested']}` to `{degraded['implemented_as']}`."
                for degraded in x11_render["degraded_fields"]
            )
        if target_name == "x11-shader":
            reasons.append("Shader output is always an artifact step; live preview is mediated through the paired picom/runtime targets.")

    return {
        "kind": "concrete-target",
        "target_name": target_name,
        "family_name": str(compiler.family_name),
        "supported_target_classes": list(getattr(compiler, "supported_target_classes", ())),
        "requested_by": requested_by,
        "status_class": status_class,
        "plan_action": plan_action,
        "current_implementation_mode": "export-only-dev",
        "apply_preview_candidate": plan_action == "compile-and-apply-preview",
        "reasons": reasons,
        "warnings": warnings,
    }


def _can_preview_apply_now(rules: Mapping[str, Any], session_type: str, wm_or_de: str) -> bool:
    apply_session_types = rules.get("apply_preview_session_types", set())
    if session_type not in apply_session_types:
        return False
    required_wm = rules.get("apply_preview_wm_or_de")
    if required_wm and wm_or_de not in required_wm:
        return False
    return True


def _summarize_environment_capabilities(environment: Mapping[str, Any]) -> dict[str, Any]:
    session_type = str(environment["session_type"])
    executables = dict(environment.get("executables", {}))
    x11_render_possible = session_type == "x11" and bool(executables.get("picom"))
    return {
        "terminal_family_meaningful_now": session_type in {"tty", "x11", "wayland", "remote-ssh"},
        "wm_family_meaningful_now": session_type in {"x11", "wayland"},
        "toolkit_family_meaningful_now": session_type in {"x11", "wayland", "remote-ssh"},
        "current_session_apply_preview_possible": session_type in {"x11", "wayland"},
        "x11_render_path_hint": {
            "environment_capable": session_type == "x11",
            "picom_available": bool(executables.get("picom")),
            "possible_if_implemented": x11_render_possible,
            "implemented_now": True,
            "reason": (
                "The detected environment can host the bounded TWO-17 X11 render slice, including the explicit dev-only live probe path."
                if session_type == "x11"
                else "The detected environment is not an X11 session."
            ),
        },
    }


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
