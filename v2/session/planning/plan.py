"""Capability-aware session planning for the early 2.x dev scaffold."""

from __future__ import annotations

from typing import Any, Mapping

from v2.targets import TARGET_COMPILERS, list_target_families, list_targets

TARGET_RULES = {
    "alacritty": {
        "preferred_session_types": {"tty", "x11", "wayland", "remote-ssh"},
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
    "gtk": "Toolkit export targets are not implemented yet in 2.x.",
    "qt": "Toolkit export targets are not implemented yet in 2.x.",
    "icons": "Icon-policy targets are not implemented yet in 2.x.",
    "cursors": "Cursor-policy targets are not implemented yet in 2.x.",
    "notifications": "Notification targets are not implemented yet in 2.x.",
    "launcher": "Launcher targets are not implemented yet in 2.x.",
}


def build_session_plan(resolved_profile: Mapping[str, Any], environment: Mapping[str, Any]) -> dict[str, Any]:
    requested_target_classes = list(resolved_profile["semantics"]["session"]["requested_targets"])
    apply_mode = str(resolved_profile["semantics"]["session"]["apply_mode"])
    persistence = str(resolved_profile["semantics"]["session"]["persistence"])
    render_mode = str(resolved_profile["semantics"]["render"]["mode"])
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
        "TWO-11 planning is preview-only and does not mutate the current session.",
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
            "Resolved render intent is present, but TWO-11 planning can only preview terminal/TUI and WM theme/config targets."
        )

    if apply_mode != "export-only":
        warnings.append(
            f"`session.apply_mode = \"{apply_mode}\"` is previewed only; live apply/install orchestration is not implemented yet."
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
) -> dict[str, Any]:
    rules = TARGET_RULES[target_name]
    session_type = str(environment["session_type"])
    wm_or_de = str(environment["wm_or_de"])
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

    if apply_mode == "current-session":
        if _can_preview_apply_now(rules, session_type, wm_or_de):
            plan_action = "compile-and-apply-preview"
            status_class = "partial"
            reasons.append("This target would be a current-session apply candidate once live orchestration exists.")
            warnings.append("Preview only: TWO-11 does not execute current-session side effects.")
        elif aligned:
            warnings.append(
                "Current-session intent is requested, but this target remains export-only until live session orchestration exists."
            )
    elif apply_mode in {"installed-default", "explicit-only"} and aligned:
        warnings.append(
            f"`session.apply_mode = \"{apply_mode}\"` is not implemented; this target remains an export-only preview in TWO-11."
        )

    if target_name in {"i3", "sway", "waybar"} and session_type not in {"x11", "wayland"}:
        warnings.append("WM targets can be generated here, but the current environment does not look like a live GUI WM session.")

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
        "current_session_apply_preview_possible": session_type in {"x11", "wayland"},
        "x11_render_path_hint": {
            "environment_capable": session_type == "x11",
            "picom_available": bool(executables.get("picom")),
            "possible_if_implemented": x11_render_possible,
            "implemented_now": False,
            "reason": (
                "The detected environment could host an X11 compositor path, but TWO-11 still lacks the X11 render family."
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
