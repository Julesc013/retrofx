"""Tests for the first real 2.x typography and font-policy outputs."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.compile_targets import compile_profile_to_output
from v2.core.dev.plan_session import plan_profile_session
from v2.core.pipeline import run_profile_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class TypographyTargetTests(unittest.TestCase):
    def test_explicit_terminal_primary_resolves(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-crt.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        typography = resolved["semantics"]["typography"]
        self.assertEqual(typography["terminal_primary"], "Terminus Nerd Font")
        self.assertEqual(typography["console_font"], "Terminus Nerd Font")

    def test_fallback_fonts_resolve_into_terminal_stack(self) -> None:
        result = run_profile_pipeline(FIXTURES / "warm-night-theme-only.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        typography = resolved["semantics"]["typography"]
        self.assertEqual(typography["terminal_fallbacks"], ["DejaVu Sans Mono", "Noto Color Emoji"])
        self.assertEqual(
            typography["terminal_stack"],
            ["Berkeley Mono", "DejaVu Sans Mono", "Noto Color Emoji"],
        )

    def test_fontconfig_output_emits_expected_aa_policy(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpdir,
                target_names=["fontconfig"],
            )
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "fontconfig" / "60-retrofx-fonts.conf"
            fontconfig = output_file.read_text(encoding="utf-8")
            self.assertIn("<family>monospace</family>", fontconfig)
            self.assertIn("<family>Berkeley Mono</family>", fontconfig)
            self.assertIn("<const>none</const>", fontconfig)
            self.assertIn("<const>hintslight</const>", fontconfig)
            self.assertIn("<bool>true</bool>", fontconfig)

    def test_alacritty_output_includes_expected_typography_settings(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "strict-green-crt.toml",
                out_root=tmpdir,
                target_names=["alacritty"],
            )
            self.assertTrue(payload["ok"])
            alacritty = (Path(payload["profile_output_root"]) / "alacritty" / "alacritty.toml").read_text(encoding="utf-8")
            self.assertIn("[font.normal]", alacritty)
            self.assertIn('family = "Terminus Nerd Font"', alacritty)

    def test_default_typography_values_are_filled(self) -> None:
        result = run_profile_pipeline(FIXTURES / "vga-like-palette.toml")
        self.assertTrue(result.ok)
        normalized = result.normalized_profile
        assert normalized is not None
        typography = normalized["typography"]
        self.assertEqual(typography["terminal_primary"], "monospace")
        self.assertEqual(typography["console_font"], "monospace")
        self.assertEqual(typography["ui_sans"], "sans-serif")
        self.assertEqual(typography["ui_mono"], "monospace")
        self.assertEqual(typography["fontconfig_aliases"]["monospace"], ["monospace"])

    def test_invalid_typography_profile_fails_validation(self) -> None:
        result = run_profile_pipeline(FIXTURES / "invalid-typography-profile.toml")
        self.assertFalse(result.ok)
        self.assertEqual(result.stage, "validation")
        codes = {error.code for error in result.errors}
        self.assertIn("invalid-terminal-fallbacks", codes)
        self.assertIn("invalid-enum", codes)

    def test_typography_target_regeneration_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpdir_a,
                target_names=["alacritty", "fontconfig"],
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpdir_b,
                target_names=["alacritty", "fontconfig"],
            )
            self.assertTrue(payload_a["ok"])
            self.assertTrue(payload_b["ok"])
            self.assertEqual(
                [target["artifacts"][0]["content_sha256"] for target in payload_a["compiled_targets"]],
                [target["artifacts"][0]["content_sha256"] for target in payload_b["compiled_targets"]],
            )

    def test_plan_preview_exposes_resolved_typography(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "modern-minimal-wm.toml",
            env={
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "sway",
                "SWAYSOCK": "/tmp/sway.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["profile"]["typography"]["terminal_primary"], "JetBrains Mono")

    def test_dev_compile_entrypoint_includes_resolved_typography(self) -> None:
        with TemporaryDirectory() as tmpdir:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.compile_targets",
                    str(FIXTURES / "strict-green-crt.toml"),
                    "--target",
                    "fontconfig",
                    "--out-root",
                    tmpdir,
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertIn("resolved_typography", payload)
            self.assertEqual(payload["resolved_typography"]["terminal_primary"], "Terminus Nerd Font")


if __name__ == "__main__":
    unittest.main()
