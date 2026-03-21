"""Session-local fontconfig export for the early 2.x typography slice."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.common import TypographyPolicyContext, build_typography_policy_context


class FontconfigCompiler:
    target_name = "fontconfig"
    family_name = "toolkit"
    output_file_name = "60-retrofx-fonts.conf"
    supported_target_classes = ("terminal", "wm")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_typography_policy_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = self._warnings(context)

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
                "semantics.typography.console_font",
                "semantics.typography.terminal_primary",
                "semantics.typography.terminal_fallbacks",
                "semantics.typography.ui_sans",
                "semantics.typography.ui_mono",
                "semantics.typography.aa",
                "semantics.typography.fontconfig_aliases",
            ],
            ignored_sections=[
                "semantics.color",
                "semantics.render",
                "semantics.chrome",
                "semantics.session",
                "semantics.typography.icon_font",
                "semantics.typography.emoji_policy",
            ],
            warnings=warnings,
            notes=[
                "Deterministic session-local fontconfig-style artifact from the resolved profile.",
                "This output is export-oriented only in TWO-12; it does not mutate global desktop font settings.",
            ],
        )

    def _warnings(self, context: TypographyPolicyContext) -> list[str]:
        warnings: list[str] = []
        if not set(context.requested_target_classes).intersection(self.supported_target_classes):
            warnings.append(
                "This typography target was compiled explicitly in dev mode even though the profile's requested target classes do not include terminal or WM outputs directly."
            )
        if context.console_font:
            warnings.append(
                "The resolved console font role is recorded for future TTY integration, but session-local fontconfig output cannot control Linux console fonts."
            )
        if context.icon_font:
            warnings.append("Icon-font selection is not emitted by the session-local fontconfig target in TWO-12.")
        if context.emoji_policy != "inherit":
            warnings.append(
                "Emoji policy is summarized in the fontconfig artifact header, but full emoji fallback orchestration remains future work."
            )
        return warnings

    def _render(self, context: TypographyPolicyContext) -> str:
        lines = [
            '<?xml version="1.0"?>',
            "<!DOCTYPE fontconfig SYSTEM \"fonts.dtd\">",
            "<fontconfig>",
            "  <!-- RetroFX 2.x experimental typography target: fontconfig -->",
            f"  <!-- profile.id = {escape(context.profile_id)} -->",
            f"  <!-- profile.name = {escape(context.profile_name)} -->",
            f"  <!-- terminal_primary = {escape(context.terminal_primary)} -->",
            f"  <!-- ui_sans = {escape(context.ui_sans)} -->",
            f"  <!-- ui_mono = {escape(context.ui_mono)} -->",
            f"  <!-- console_font = {escape(context.console_font)} -->",
            f"  <!-- emoji_policy = {escape(context.emoji_policy)} -->",
        ]

        alias_blocks = self._render_alias_blocks(context.fontconfig_aliases)
        if alias_blocks:
            lines.append("")
            lines.extend(alias_blocks)

        aa_block = self._render_aa_block(context)
        if aa_block:
            lines.append("")
            lines.extend(aa_block)

        lines.append("</fontconfig>")
        lines.append("")
        return "\n".join(lines)

    def _render_alias_blocks(self, aliases: Mapping[str, list[str]]) -> list[str]:
        blocks: list[str] = []
        for family in ("monospace", "sans-serif"):
            candidates = [value for value in aliases.get(family, []) if value and value != family]
            if not candidates:
                continue
            blocks.extend(
                [
                    "  <alias>",
                    f"    <family>{escape(family)}</family>",
                    "    <prefer>",
                    *[f"      <family>{escape(candidate)}</family>" for candidate in candidates],
                    "    </prefer>",
                    "  </alias>",
                ]
            )
        return blocks

    def _render_aa_block(self, context: TypographyPolicyContext) -> list[str]:
        edits: list[str] = []

        antialias_value = {"on": "true", "off": "false"}.get(context.aa_antialias)
        if antialias_value is not None:
            edits.extend(
                [
                    '    <edit mode="assign" name="antialias">',
                    f"      <bool>{antialias_value}</bool>",
                    "    </edit>",
                ]
            )

        if context.aa_subpixel in {"none", "rgb", "bgr", "vrgb", "vbgr"}:
            edits.extend(
                [
                    '    <edit mode="assign" name="rgba">',
                    f"      <const>{escape(context.aa_subpixel)}</const>",
                    "    </edit>",
                ]
            )

        hinting_value = _hinting_bool(context.aa_hinting)
        hintstyle_value = _hintstyle_const(context.aa_hinting)
        if hinting_value is not None:
            edits.extend(
                [
                    '    <edit mode="assign" name="hinting">',
                    f"      <bool>{hinting_value}</bool>",
                    "    </edit>",
                ]
            )
        if hintstyle_value is not None:
            edits.extend(
                [
                    '    <edit mode="assign" name="hintstyle">',
                    f"      <const>{hintstyle_value}</const>",
                    "    </edit>",
                ]
            )

        if not edits:
            return []

        return [
            '  <match target="font">',
            *edits,
            "  </match>",
        ]


def _hinting_bool(value: str) -> str | None:
    if value == "none":
        return "false"
    if value in {"slight", "medium", "full"}:
        return "true"
    return None


def _hintstyle_const(value: str) -> str | None:
    mapping = {
        "none": "hintnone",
        "slight": "hintslight",
        "medium": "hintmedium",
        "full": "hintfull",
    }
    return mapping.get(value)
