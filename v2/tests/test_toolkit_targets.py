"""Tests for the bounded TWO-18 toolkit and desktop export targets."""

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


class ToolkitTargetTests(unittest.TestCase):
    def test_explicit_icon_cursor_settings_resolve(self) -> None:
        result = run_profile_pipeline(FIXTURES / "retro-desktop-explicit.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        chrome = resolved["semantics"]["chrome"]
        self.assertEqual(chrome["icon_theme"], "Papirus-Dark")
        self.assertEqual(chrome["icon_variant"], "retro-green")
        self.assertEqual(chrome["cursor_theme"], "Bibata-Modern-Ice")
        self.assertEqual(chrome["cursor_size"], 26)
        self.assertEqual(chrome["cursor_variant"], "ice")

    def test_gtk_facing_output_is_emitted_deterministically(self) -> None:
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "retro-desktop-explicit.toml",
                out_root=tmpdir_a,
                target_names=["gtk-export"],
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "retro-desktop-explicit.toml",
                out_root=tmpdir_b,
                target_names=["gtk-export"],
            )
            self.assertTrue(payload_a["ok"])
            self.assertTrue(payload_b["ok"])
            gtk_file = Path(payload_a["profile_output_root"]) / "gtk-export" / "gtk-export.ini"
            contents = gtk_file.read_text(encoding="utf-8")
            self.assertIn("[Settings]", contents)
            self.assertIn("gtk-icon-theme-name=Papirus-Dark", contents)
            self.assertIn("gtk-cursor-theme-size=26", contents)
            self.assertEqual(
                payload_a["compiled_targets"][0]["artifacts"][0]["content_sha256"],
                payload_b["compiled_targets"][0]["artifacts"][0]["content_sha256"],
            )

    def test_qt_facing_output_emits_palette_and_cursor_hints(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "retro-desktop-explicit.toml",
                out_root=tmpdir,
                target_names=["qt-export"],
            )
            self.assertTrue(payload["ok"])
            qt_file = Path(payload["profile_output_root"]) / "qt-export" / "qt-export.json"
            qt_payload = json.loads(qt_file.read_text(encoding="utf-8"))
            self.assertEqual(qt_payload["icons"]["theme"], "Papirus-Dark")
            self.assertEqual(qt_payload["cursor"]["size"], 26)
            self.assertIn("Window", qt_payload["palette"])
            self.assertEqual(qt_payload["style_hints"]["qt_style_hint_name"], "Fusion")

    def test_icon_cursor_output_emits_expected_values(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "retro-desktop-explicit.toml",
                out_root=tmpdir,
                target_names=["icon-cursor", "desktop-style"],
            )
            self.assertTrue(payload["ok"])
            icon_cursor_file = Path(payload["profile_output_root"]) / "icon-cursor" / "policy.json"
            icon_cursor = json.loads(icon_cursor_file.read_text(encoding="utf-8"))
            self.assertEqual(icon_cursor["icon_policy"]["variant"], "retro-green")
            self.assertEqual(icon_cursor["cursor_policy"]["theme"], "Bibata-Modern-Ice")
            desktop_style = json.loads(
                (Path(payload["profile_output_root"]) / "desktop-style" / "desktop-style.json").read_text(encoding="utf-8")
            )
            self.assertEqual(desktop_style["cursor"]["size"], 26)
            self.assertTrue(desktop_style["surface_preferences"]["prefer_dark_theme"])

    def test_defaults_still_emit_coherent_toolkit_artifacts(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpdir,
                target_names=["gtk-export", "qt-export", "desktop-style"],
            )
            self.assertTrue(payload["ok"])
            gtk_file = Path(payload["profile_output_root"]) / "gtk-export" / "gtk-export.ini"
            self.assertIn("gtk-cursor-theme-size=24", gtk_file.read_text(encoding="utf-8"))
            qt_payload = json.loads((Path(payload["profile_output_root"]) / "qt-export" / "qt-export.json").read_text(encoding="utf-8"))
            self.assertEqual(qt_payload["icons"]["theme"], "")
            self.assertEqual(qt_payload["cursor"]["size"], 24)

    def test_invalid_toolkit_values_fail_validation(self) -> None:
        result = run_profile_pipeline(FIXTURES / "invalid-toolkit-profile.toml")
        self.assertFalse(result.ok)
        self.assertEqual(result.stage, "validation")
        codes = {error.code for error in result.errors}
        self.assertIn("invalid-chrome-string", codes)
        self.assertIn("invalid-int-range", codes)

    def test_plan_output_includes_toolkit_information(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "retro-desktop-explicit.toml",
            env={
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "gnome",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertIn("toolkit_style", payload["plan"])
        self.assertEqual(payload["plan"]["toolkit_style"]["resolved_values"]["icon_theme"], "Papirus-Dark")
        self.assertIn("gtk-export", payload["plan"]["compile_targets"])
        self.assertIn("qt-export", payload["plan"]["compile_targets"])

    def test_dev_compile_entrypoint_includes_resolved_chrome_and_toolkit_summary(self) -> None:
        with TemporaryDirectory() as tmpdir:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.compile_targets",
                    str(FIXTURES / "retro-desktop-explicit.toml"),
                    "--target",
                    "gtk-export",
                    "--target",
                    "qt-export",
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
            self.assertEqual(payload["resolved_chrome"]["cursor_size"], 26)
            self.assertEqual(payload["toolkit_style"]["resolved_values"]["cursor_theme"], "Bibata-Modern-Ice")


if __name__ == "__main__":
    unittest.main()
