"""Icon and cursor policy export for the bounded TWO-18 toolkit slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.common import build_toolkit_style_context, toolkit_export_warnings


class IconCursorCompiler:
    target_name = "icon-cursor"
    family_name = "toolkit"
    output_file_name = "policy.json"
    supported_target_classes = ("icons", "cursors")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_toolkit_style_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = toolkit_export_warnings(context, self.supported_target_classes, target_label="icon/cursor")

        artifact = write_target_artifact(
            target_name=self.target_name,
            output_dir=output_dir,
            file_name=self.output_file_name,
            content=self._render(context),
        )
        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=[artifact],
            consumed_sections=[
                "identity",
                "semantics.chrome",
                "semantics.typography",
            ],
            ignored_sections=[
                "semantics.color",
                "semantics.render",
                "semantics.session",
            ],
            warnings=warnings,
            notes=[
                "Deterministic icon and cursor policy artifact from the resolved profile.",
                "This file is intended for later session integration or manual inspection, not live desktop mutation.",
            ],
        )

    def _render(self, context: Any) -> str:
        payload = {
            "schema": "retrofx.icon-cursor/v2alpha1",
            "profile": {
                "id": context.profile_id,
                "name": context.profile_name,
                "theme_hint_name": context.theme_hint_name,
            },
            "advisory_only": True,
            "icon_policy": {
                "theme": context.icon_theme,
                "variant": context.icon_variant,
            },
            "cursor_policy": {
                "theme": context.cursor_theme,
                "size": context.cursor_size,
                "variant": context.cursor_variant,
                "text_color_hint": context.cursor_text,
            },
            "typography_hints": {
                "ui_sans": context.ui_sans,
                "icon_font": context.ui_mono,
            },
            "potential_consumers": {
                "gtk-export": "Uses icon and cursor selections as export hints.",
                "qt-export": "Uses icon and cursor selections as export hints.",
                "wm": "May annotate icon/cursor preferences without claiming ownership.",
            },
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
