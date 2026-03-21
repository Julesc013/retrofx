"""Tests for the first real 2.x WM target compilers."""

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


class WmTargetCompilerTests(unittest.TestCase):
    def test_i3_fragment_is_emitted_for_valid_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "wm-chrome-overrides.toml", out_root=tmpdir, target_names=["i3"])
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "i3" / "retrofx-theme.conf"
            self.assertTrue(output_file.is_file())

    def test_sway_fragment_is_emitted_for_valid_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "modern-minimal-wm.toml", out_root=tmpdir, target_names=["sway"])
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "sway" / "retrofx-theme.conf"
            self.assertTrue(output_file.is_file())

    def test_waybar_stylesheet_is_emitted_for_valid_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "modern-minimal-wm.toml", out_root=tmpdir, target_names=["waybar"])
            self.assertTrue(payload["ok"])
            output_file = Path(payload["profile_output_root"]) / "waybar" / "style.css"
            self.assertTrue(output_file.is_file())

    def test_emitted_files_contain_expected_sections(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "wm-chrome-overrides.toml",
                out_root=tmpdir,
                target_names=["i3", "sway", "waybar"],
            )
            self.assertTrue(payload["ok"])
            i3_fragment = (Path(payload["profile_output_root"]) / "i3" / "retrofx-theme.conf").read_text(encoding="utf-8")
            sway_fragment = (Path(payload["profile_output_root"]) / "sway" / "retrofx-theme.conf").read_text(encoding="utf-8")
            waybar_css = (Path(payload["profile_output_root"]) / "waybar" / "style.css").read_text(encoding="utf-8")
            self.assertIn("client.focused", i3_fragment)
            self.assertIn("bar {", i3_fragment)
            self.assertIn("client.focused", sway_fragment)
            self.assertIn("window#waybar", waybar_css)
            self.assertIn("@define-color retrofx-status-bg", waybar_css)

    def test_deterministic_regeneration_produces_same_content(self) -> None:
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "wm-chrome-overrides.toml",
                out_root=tmpdir_a,
                target_names=["i3", "sway", "waybar"],
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "wm-chrome-overrides.toml",
                out_root=tmpdir_b,
                target_names=["i3", "sway", "waybar"],
            )
            self.assertTrue(payload_a["ok"])
            self.assertTrue(payload_b["ok"])
            self.assertEqual(
                [target["artifacts"][0]["content_sha256"] for target in payload_a["compiled_targets"]],
                [target["artifacts"][0]["content_sha256"] for target in payload_b["compiled_targets"]],
            )

    def test_malformed_profile_fails_before_target_emission(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(FIXTURES / "malformed-profile.toml", out_root=tmpdir, target_names=["i3"])
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["stage"], "validation")
            self.assertEqual(payload["compiled_targets"], [])
            self.assertIsNone(payload["profile_output_root"])

    def test_chrome_overrides_are_emitted(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "wm-chrome-overrides.toml",
                out_root=tmpdir,
                target_names=["i3", "sway", "waybar"],
            )
            self.assertTrue(payload["ok"])
            i3_fragment = (Path(payload["profile_output_root"]) / "i3" / "retrofx-theme.conf").read_text(encoding="utf-8")
            sway_fragment = (Path(payload["profile_output_root"]) / "sway" / "retrofx-theme.conf").read_text(encoding="utf-8")
            waybar_css = (Path(payload["profile_output_root"]) / "waybar" / "style.css").read_text(encoding="utf-8")
            self.assertIn("gaps inner 12", i3_fragment)
            self.assertIn("set $retrofx_border_active #cf8a4a", i3_fragment)
            self.assertIn("gaps inner 12", sway_fragment)
            self.assertIn("margin: 6px 12px 0 12px;", waybar_css)
            self.assertIn("border-radius: 8px;", waybar_css)

    def test_default_heavy_profile_compiles_from_derived_tokens(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "modern-minimal-wm.toml",
                out_root=tmpdir,
                target_names=["i3", "waybar"],
            )
            self.assertTrue(payload["ok"])
            i3_fragment = (Path(payload["profile_output_root"]) / "i3" / "retrofx-theme.conf").read_text(encoding="utf-8")
            waybar_css = (Path(payload["profile_output_root"]) / "waybar" / "style.css").read_text(encoding="utf-8")
            self.assertIn("set $retrofx_status_bg", i3_fragment)
            self.assertIn("client.urgent", i3_fragment)
            self.assertIn("@define-color retrofx-border-active", waybar_css)
            self.assertIn("window#waybar", waybar_css)

    def test_dev_compile_entrypoint_can_emit_wm_target(self) -> None:
        with TemporaryDirectory() as tmpdir:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.compile_targets",
                    str(FIXTURES / "wm-chrome-overrides.toml"),
                    "--target",
                    "sway",
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
            self.assertEqual(payload["selected_targets"], ["sway"])


if __name__ == "__main__":
    unittest.main()
