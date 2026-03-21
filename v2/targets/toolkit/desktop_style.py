"""Desktop-style summary export for the bounded TWO-18 toolkit slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.common import (
    build_toolkit_style_context,
    derive_toolkit_emphasis,
    derive_toolkit_palette_roles,
    toolkit_export_warnings,
)


class DesktopStyleCompiler:
    target_name = "desktop-style"
    family_name = "toolkit"
    output_file_name = "desktop-style.json"
    supported_target_classes = ("gtk", "qt", "icons", "cursors")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_toolkit_style_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = toolkit_export_warnings(context, self.supported_target_classes, target_label="desktop-style")

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
                "semantics.color.semantic",
                "semantics.typography",
                "semantics.chrome",
            ],
            ignored_sections=[
                "semantics.color.terminal_ansi",
                "semantics.color.tty_ansi",
                "semantics.render",
                "semantics.session",
            ],
            warnings=warnings,
            notes=[
                "Deterministic aggregate desktop-style bundle for future toolkit/session integration.",
                "This output is explicitly advisory and does not imply live desktop ownership.",
            ],
        )

    def _render(self, context: Any) -> str:
        payload = {
            "schema": "retrofx.desktop-style/v2alpha1",
            "profile": {
                "id": context.profile_id,
                "name": context.profile_name,
                "family": context.family,
                "strictness": context.strictness,
                "theme_hint_name": context.theme_hint_name,
            },
            "advisory_only": True,
            "typography": {
                "ui_sans": context.ui_sans,
                "ui_mono": context.ui_mono,
                "ui_mono_stack": context.ui_mono_stack,
                "terminal_primary": context.terminal_primary,
                "terminal_fallbacks": context.terminal_fallbacks,
                "emoji_policy": context.emoji_policy,
                "aa": {
                    "antialias": context.aa_antialias,
                    "subpixel": context.aa_subpixel,
                    "hinting": context.aa_hinting,
                },
            },
            "icons": {
                "theme": context.icon_theme,
                "variant": context.icon_variant,
            },
            "cursor": {
                "theme": context.cursor_theme,
                "size": context.cursor_size,
                "variant": context.cursor_variant,
            },
            "palette": derive_toolkit_palette_roles(context),
            "emphasis": derive_toolkit_emphasis(context),
            "surface_preferences": {
                "prefer_dark_theme": context.prefer_dark_theme,
                "selection_bg": context.selection_bg,
                "selection_fg": context.selection_fg,
                "status_bg": context.status_bg,
                "status_fg": context.status_fg,
            },
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
