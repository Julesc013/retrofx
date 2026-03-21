"""Experimental picom config compiler for the first 2.x X11 render slice."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.x11.common import build_x11_render_context, build_x11_warnings, relative_shader_path


class X11PicomCompiler:
    target_name = "x11-picom"
    family_name = "x11"
    output_file_name = "picom.conf"
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
            content=self._render(context, output_dir, profile_output_root / "x11-shader"),
        )

        warnings = build_x11_warnings(context, self.supported_target_classes)
        if not context.x11_render["live_preview_possible"]:
            warnings.append("Generated picom config is export-only in the current environment; live preview is unavailable.")

        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=[artifact],
            consumed_sections=[
                "identity",
                "semantics.render.mode",
                "semantics.render.effects",
                "semantics.render.display",
                "semantics.session",
            ],
            ignored_sections=[
                "semantics.color.terminal_ansi",
                "semantics.typography",
                "semantics.chrome",
            ],
            warnings=warnings,
            notes=[
                "Deterministic picom config for the bounded TWO-17 X11 render subset.",
                "This config is only used by the explicit dev-only X11 preview path and does not touch 1.x runtime files.",
            ],
        )

    def _render(self, context, output_dir: Path, shader_dir: Path) -> str:
        blur_strength = int(context.effects.get("blur", 0))
        blur_enabled = "true" if blur_strength > 0 else "false"
        shader_path = relative_shader_path(output_dir, shader_dir, "shader.glsl")
        lines = [
            "# RetroFX 2.x experimental X11 render target: picom",
            f"# profile.id = {context.profile_id}",
            f"# profile.name = {context.profile_name}",
            f"# requested_mode = {context.render_mode}",
            f"# implemented_mode = {context.implemented_mode}",
            '# This file is dev-only and is not wired into the 1.x runtime.',
            "",
            'backend = "glx";',
            "vsync = true;",
            "use-damage = true;",
            'log-level = "warn";',
            "",
            '# Conservative defaults for the early X11 render slice.',
            "mark-wmwin-focused = true;",
            "mark-ovredir-focused = false;",
            "unredir-if-possible = false;",
            "detect-client-opacity = false;",
            "inactive-opacity = 1.0;",
            "active-opacity = 1.0;",
            "frame-opacity = 1.0;",
            "",
            'blur-method = "dual_kawase";',
            f"blur-strength = {blur_strength};",
            f"blur-background = {blur_enabled};",
            f"blur-background-frame = {blur_enabled};",
            "# No exclusion rules are generated in TWO-17.",
            "",
            f'window-shader-fg = "{shader_path}";',
            "",
        ]
        return "\n".join(lines)
