"""Tests for the first real 2.x terminal/TUI compilers."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.compile_targets import compile_profile_to_output

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class TerminalTargetCompilerTests(unittest.TestCase):
    def test_xresources_is_emitted_for_valid_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "strict-green-crt.toml", out_root=tmpdir, target_names=["xresources"])
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "xresources" / "Xresources"
            self.assertTrue(output_file.is_file())

    def test_alacritty_is_emitted_for_valid_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "strict-green-crt.toml", out_root=tmpdir, target_names=["alacritty"])
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "alacritty" / "alacritty.toml"
            self.assertTrue(output_file.is_file())

    def test_emitted_files_contain_expected_sections(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "strict-green-crt.toml",
                out_root=tmpdir,
                target_names=["xresources", "alacritty"],
            )
            self.assertTrue(payload["ok"])
            xresources = (Path(payload["profile_output_root"]) / "xresources" / "Xresources").read_text(encoding="utf-8")
            alacritty = (Path(payload["profile_output_root"]) / "alacritty" / "alacritty.toml").read_text(encoding="utf-8")
            self.assertIn("*foreground:", xresources)
            self.assertIn("*color15:", xresources)
            self.assertIn("[colors.primary]", alacritty)
            self.assertIn("[colors.normal]", alacritty)
            self.assertIn("[colors.bright]", alacritty)

    def test_malformed_profile_fails_before_target_emission(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "malformed-profile.toml", out_root=tmpdir, target_names=["xresources"])
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["stage"], "validation")
            self.assertEqual(payload["compiled_targets"], [])
            self.assertIsNone(payload["profile_output_root"])

    def test_deterministic_regeneration_produces_same_content(self) -> None:
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "vga-like-palette.toml",
                out_root=tmpdir_a,
                target_names=["xresources", "alacritty"],
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "vga-like-palette.toml",
                out_root=tmpdir_b,
                target_names=["xresources", "alacritty"],
            )
            self.assertTrue(payload_a["ok"])
            self.assertTrue(payload_b["ok"])
            self.assertEqual(
                [target["artifacts"][0]["content_sha256"] for target in payload_a["compiled_targets"]],
                [target["artifacts"][0]["content_sha256"] for target in payload_b["compiled_targets"]],
            )

    def test_terminal_overrides_are_emitted(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "terminal-overrides.toml",
                out_root=tmpdir,
                target_names=["xresources", "alacritty"],
            )
            self.assertTrue(payload["ok"])
            xresources = (Path(payload["profile_output_root"]) / "xresources" / "Xresources").read_text(encoding="utf-8")
            alacritty = (Path(payload["profile_output_root"]) / "alacritty" / "alacritty.toml").read_text(encoding="utf-8")
            self.assertIn("*color1: #ff3355", xresources)
            self.assertIn('red = "#ff3355"', alacritty)
            self.assertIn('magenta = "#c792ea"', alacritty)

    def test_default_heavy_profile_compiles_from_derived_tokens(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpdir,
                target_names=["xresources", "alacritty"],
            )
            self.assertTrue(payload["ok"])
            xresources = (Path(payload["profile_output_root"]) / "xresources" / "Xresources").read_text(encoding="utf-8")
            self.assertIn("*color0: #16120f", xresources)
            self.assertIn("*highlightColor:", xresources)

    def test_dev_compile_entrypoint_emits_json(self) -> None:
        with TemporaryDirectory() as tmpdir:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.compile_targets",
                    str(FIXTURES / "strict-green-crt.toml"),
                    "--target",
                    "xresources",
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
            self.assertEqual(payload["stage"], "compile")
            self.assertEqual(payload["selected_targets"], ["xresources"])


if __name__ == "__main__":
    unittest.main()
