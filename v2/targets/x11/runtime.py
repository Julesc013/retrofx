"""Runtime metadata compiler for the first 2.x X11 render slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.x11.common import build_x11_render_context, build_x11_warnings


class X11RenderRuntimeCompiler:
    target_name = "x11-render-runtime"
    family_name = "x11"
    output_file_name = "runtime-metadata.json"
    supported_target_classes = ("x11", "wm")

    def compile(
        self,
        resolved_profile: Mapping[str, Any],
        profile_output_root: Path,
        compile_context: Mapping[str, Any] | None = None,
    ) -> TargetCompileResult:
        context_map = dict(compile_context or {})
        environment = dict(context_map.get("environment", {}))
        display_policy = context_map.get("display_policy")
        x11_render = context_map.get("x11_render")
        context = build_x11_render_context(
            resolved_profile,
            environment=environment,
            display_policy=display_policy,
            x11_render=x11_render,
        )
        output_dir = profile_output_root / self.target_name
        artifact = write_target_artifact(
            target_name=self.target_name,
            output_dir=output_dir,
            file_name=self.output_file_name,
            content=self._render(context),
        )
        warnings = build_x11_warnings(context, self.supported_target_classes)
        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=[artifact],
            consumed_sections=[
                "identity",
                "semantics.render",
                "semantics.session",
            ],
            ignored_sections=[
                "semantics.typography",
                "semantics.chrome",
            ],
            warnings=warnings,
            notes=[
                "Deterministic runtime metadata for the dev-only X11 preview surface.",
                "Live preview state is recorded separately by the explicit preview command and never touches 1.x state paths.",
            ],
        )

    def _render(self, context) -> str:
        payload = {
            "implementation": {
                "status": "experimental-dev-only",
                "prompt": "TWO-17",
                "surface": "x11-render-preview",
            },
            "profile": {
                "id": context.profile_id,
                "name": context.profile_name,
            },
            "render": {
                "requested_mode": context.render_mode,
                "implemented_mode": context.implemented_mode,
                "palette_kind": context.palette_kind,
                "palette_size": context.palette_size,
                "monochrome_bands": context.monochrome_bands,
                "effects": context.effects,
                "display": context.display,
            },
            "x11_render": context.x11_render,
            "artifacts": {
                "shader": "x11-shader/shader.glsl",
                "picom_config": "x11-picom/picom.conf",
                "display_policy": "x11-display-policy/display-policy.json",
            },
            "preview": {
                "command_hint": "picom --config x11-picom/picom.conf",
                "preview_state_file": "x11-render-runtime/preview-state.json",
                "cleanup": "The live probe path never touches 1.x state and only records dev-only preview metadata.",
            },
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
