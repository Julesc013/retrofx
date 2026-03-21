"""Resolved-profile scaffolding for the initial 2.x core implementation."""

from __future__ import annotations

from v2.core.models.types import Issue, NormalizedProfile, ResolvedProfile


def build_resolved_profile(normalized_profile: NormalizedProfile, warnings: list[Issue]) -> ResolvedProfile:
    data = normalized_profile.data
    color = data["color"]
    typography = data["typography"]
    render = data["render"]
    chrome = data["chrome"]
    session = data["session"]
    report = normalized_profile.report.to_dict()

    resolved = {
        "schema": data["schema"],
        "source": data["source"],
        "pack": data["source"]["origin"].get("pack") if data["source"]["origin"].get("type") == "pack" else None,
        "implementation": {
            "status": "experimental-dev-only",
            "capability_filtering": "not-implemented",
            "target_planning": "not-implemented",
            "artifact_planning": "not-implemented",
            "session_orchestration": "not-implemented",
        },
        "identity": data["identity"],
        "semantics": {
            "color": {
                "semantic": color["semantic"],
                "terminal_ansi": color["terminal"]["ansi"],
                "tty_ansi": color["tty"]["ansi"],
                "mapping_notes": {
                    "terminal": "derived from semantic mapping or monochrome luminance bands, then merged with authored overrides",
                    "tty": "inherits terminal ANSI by default, then merged with authored overrides",
                },
            },
            "typography": typography,
            "render": render,
            "chrome": chrome,
            "session": {
                "requested_targets": session["targets"],
                "apply_mode": session["apply_mode"],
                "persistence": session["persistence"],
            },
        },
        "target_requests": {
            "requested_target_classes": session["targets"],
            "apply_mode": session["apply_mode"],
            "persistence": session["persistence"],
            "status": "pre-capability-filtering",
        },
        "capability_context": {
            "status": "not-implemented",
            "environment_facts": None,
            "adapter_candidates": [],
        },
        "target_plan": {
            "status": "not-implemented",
            "entries": [],
        },
        "artifact_plan": {
            "status": "not-implemented",
            "required": [],
            "optional": [],
        },
        "decisions": {
            "warnings": [warning.to_dict() for warning in warnings],
            "errors": [],
            "normalization": report,
            "notes": [
                "Capability filtering is not implemented in TWO-08.",
                "Target planning is not implemented in TWO-08.",
                "Artifact planning is not implemented in TWO-08.",
            ],
        },
    }
    return ResolvedProfile(data=resolved)
