"""GTK-facing export artifact for the bounded TWO-18 toolkit slice."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.common import (
    ToolkitStyleContext,
    build_toolkit_style_context,
    derive_toolkit_palette_roles,
    derive_toolkit_theme_aliases,
    toolkit_export_warnings,
)


class GtkExportCompiler:
    target_name = "gtk-export"
    family_name = "toolkit"
    output_file_name = "gtk-export.ini"
    supported_target_classes = ("gtk",)

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_toolkit_style_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = toolkit_export_warnings(context, self.supported_target_classes, target_label="GTK export")

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
                "Deterministic GTK-facing advisory export from the resolved profile.",
                "This artifact does not claim live GTK, GNOME, or XSettings ownership.",
            ],
        )

    def _render(self, context: ToolkitStyleContext) -> str:
        aliases = derive_toolkit_theme_aliases(context)
        palette = derive_toolkit_palette_roles(context)
        lines = [
            "; RetroFX 2.x experimental toolkit target: gtk-export",
            "; Advisory export only. Future session integration may translate these values into live GTK settings.",
            f"; profile.id = {context.profile_id}",
            "",
            "[Settings]",
            f"gtk-font-name={context.ui_sans}",
            f"gtk-cursor-theme-name={context.cursor_theme}",
            f"gtk-cursor-theme-size={context.cursor_size}",
            f"gtk-icon-theme-name={context.icon_theme}",
            f"gtk-application-prefer-dark-theme={'true' if context.prefer_dark_theme else 'false'}",
            "",
            "[RetroFX]",
            f"theme-hint-name={aliases['gtk_theme_hint_name']}",
            f"theme-family={aliases['desktop_family']}",
            f"theme-strictness={aliases['desktop_strictness']}",
            f"ui-mono-family={context.ui_mono}",
            f"emoji-policy={context.emoji_policy}",
            f"icon-variant={context.icon_variant}",
            f"cursor-variant={context.cursor_variant}",
            "",
            "[RetroFXPalette]",
            f"window={palette['window']}",
            f"window-text={palette['window_text']}",
            f"base={palette['base']}",
            f"text={palette['text']}",
            f"highlight={palette['highlight']}",
            f"highlighted-text={palette['highlighted_text']}",
            f"tooltip-base={palette['tooltip_base']}",
            f"tooltip-text={palette['tooltip_text']}",
            f"link={palette['link']}",
            "",
        ]
        return "\n".join(lines)
