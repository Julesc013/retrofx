"""Qt-facing export artifact for the bounded TWO-18 toolkit slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.common import (
    build_toolkit_style_context,
    build_toolkit_style_summary,
    derive_toolkit_palette_roles,
    derive_toolkit_theme_aliases,
    toolkit_export_warnings,
)


class QtExportCompiler:
    target_name = "qt-export"
    family_name = "toolkit"
    output_file_name = "qt-export.json"
    supported_target_classes = ("qt",)

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_toolkit_style_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = toolkit_export_warnings(context, self.supported_target_classes, target_label="Qt export")

        artifact = write_target_artifact(
            target_name=self.target_name,
            output_dir=output_dir,
            file_name=self.output_file_name,
            content=self._render(resolved_profile),
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
                "Deterministic Qt-facing advisory export from the resolved profile.",
                "This artifact does not claim live Plasma, qt5ct, or qt6ct ownership.",
            ],
        )

    def _render(self, resolved_profile: Mapping[str, Any]) -> str:
        context = build_toolkit_style_context(resolved_profile)
        aliases = derive_toolkit_theme_aliases(context)
        palette = derive_toolkit_palette_roles(context)
        payload = {
            "schema": "retrofx.qt-export/v2alpha1",
            "profile": {
                "id": context.profile_id,
                "name": context.profile_name,
                "family": context.family,
                "strictness": context.strictness,
            },
            "advisory_only": True,
            "style_hints": {
                "qt_style_hint_name": aliases["qt_style_hint_name"],
                "theme_hint_name": aliases["gtk_theme_hint_name"],
                "prefer_dark_theme": context.prefer_dark_theme,
                "emoji_policy": context.emoji_policy,
            },
            "fonts": {
                "ui_sans": context.ui_sans,
                "ui_mono": context.ui_mono,
                "terminal_primary": context.terminal_primary,
                "fallbacks": context.terminal_fallbacks,
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
            "palette": {
                "Window": palette["window"],
                "WindowText": palette["window_text"],
                "Base": palette["base"],
                "AlternateBase": palette["alternate_base"],
                "Text": palette["text"],
                "Button": palette["button"],
                "ButtonText": palette["button_text"],
                "Highlight": palette["highlight"],
                "HighlightedText": palette["highlighted_text"],
                "ToolTipBase": palette["tooltip_base"],
                "ToolTipText": palette["tooltip_text"],
                "Link": palette["link"],
                "LinkVisited": palette["link_visited"],
                "BrightText": palette["bright_text"],
            },
            "summary": build_toolkit_style_summary(
                resolved_profile,
                {"session_type": "export-only", "wm_or_de": "unknown"},
            ),
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
