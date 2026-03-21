"""Advisory X11/render-adjacent display-policy compiler for the early 2.x scaffold."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.render import build_display_policy_summary
from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult


class X11DisplayPolicyCompiler:
    target_name = "x11-display-policy"
    family_name = "x11"
    output_file_name = "display-policy.json"
    supported_target_classes = ("x11", "wayland", "wm")

    def compile(
        self,
        resolved_profile: Mapping[str, Any],
        profile_output_root: Path,
        compile_context: Mapping[str, Any] | None = None,
    ) -> TargetCompileResult:
        context = dict(compile_context or {})
        environment = dict(context.get("environment", {}))
        display_policy = build_display_policy_summary(resolved_profile, environment)
        output_dir = profile_output_root / self.target_name

        artifacts = [
            write_target_artifact(
                target_name=self.target_name,
                output_dir=output_dir,
                file_name=self.output_file_name,
                content=self._render_json(resolved_profile, environment, display_policy),
            ),
            write_target_artifact(
                target_name=self.target_name,
                output_dir=output_dir,
                file_name="x11-render-policy.env",
                content=self._render_env(resolved_profile, environment, display_policy),
            ),
        ]

        warnings = list(display_policy["warnings"])
        if display_policy["overall_status"] != "future-render-consumer":
            warnings.append(
                "This display-policy target remains advisory/export-only in TWO-13; no live display transform runtime exists yet."
            )

        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=artifacts,
            consumed_sections=[
                "identity",
                "semantics.render.display",
                "semantics.session",
            ],
            ignored_sections=[
                "semantics.color",
                "semantics.typography",
                "semantics.chrome",
                "semantics.render.quantization",
                "semantics.render.palette",
                "semantics.render.effects",
            ],
            warnings=warnings,
            notes=[
                "Deterministic advisory display-policy artifacts from the resolved profile.",
                "The JSON artifact is for explainability; the env artifact is a future-consumer stub for render-capable X11 integration.",
            ],
        )

    def _render_json(
        self,
        resolved_profile: Mapping[str, Any],
        environment: Mapping[str, Any],
        display_policy: Mapping[str, Any],
    ) -> str:
        payload = {
            "implementation": {
                "status": "experimental-dev-only",
                "prompt": "TWO-13",
                "mode": "export-only-dev",
            },
            "profile": {
                "id": resolved_profile["identity"]["id"],
                "name": resolved_profile["identity"]["name"],
            },
            "environment": {
                "session_type": environment.get("session_type", "unknown-headless"),
                "wm_or_de": environment.get("wm_or_de", "unknown"),
                "context_class": environment.get("context_class", "unknown"),
                "x11_render_host_possible": display_policy["environment_interpretation"]["x11_render_host_possible"],
            },
            "display_policy": display_policy,
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    def _render_env(
        self,
        resolved_profile: Mapping[str, Any],
        environment: Mapping[str, Any],
        display_policy: Mapping[str, Any],
    ) -> str:
        requested = dict(display_policy["requested"])
        fields = ",".join(display_policy["requested_fields"])
        lines = [
            "# RetroFX 2.x experimental X11/display-policy export",
            f"# profile.id={resolved_profile['identity']['id']}",
            f"# profile.name={resolved_profile['identity']['name']}",
            f"RETROFX_DISPLAY_POLICY_STATUS={display_policy['overall_status']}",
            f"RETROFX_DISPLAY_POLICY_SESSION_TYPE={environment.get('session_type', 'unknown-headless')}",
            f"RETROFX_DISPLAY_POLICY_REQUESTED_FIELDS={fields}",
            f"RETROFX_DISPLAY_GAMMA={requested['gamma']}",
            f"RETROFX_DISPLAY_CONTRAST={requested['contrast']}",
            f"RETROFX_DISPLAY_TEMPERATURE={requested['temperature']}",
            f"RETROFX_DISPLAY_BLACK_LIFT={requested['black_lift']}",
            f"RETROFX_DISPLAY_BLUE_LIGHT_REDUCTION={requested['blue_light_reduction']}",
            f"RETROFX_DISPLAY_TINT_BIAS={requested['tint_bias'] or ''}",
            "",
        ]
        return "\n".join(lines)
