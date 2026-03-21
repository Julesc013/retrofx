"""Tests for the early 2.x environment detection and session planner."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.plan_session import plan_profile_session
from v2.session.environment import detect_environment

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class SessionPlanningTests(unittest.TestCase):
    def test_detect_environment_x11_simulated(self) -> None:
        environment = detect_environment(
            env={
                "DISPLAY": ":1",
                "XDG_SESSION_TYPE": "x11",
                "XDG_CURRENT_DESKTOP": "i3",
                "I3SOCK": "/tmp/i3.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
            path_lookup=lambda _name: None,
        )
        self.assertEqual(environment["session_type"], "x11")
        self.assertEqual(environment["wm_or_de"], "i3")
        self.assertEqual(environment["context_class"], "repo-local-dev")

    def test_detect_environment_wayland_simulated(self) -> None:
        environment = detect_environment(
            env={
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "sway",
                "SWAYSOCK": "/tmp/sway.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
            path_lookup=lambda _name: None,
        )
        self.assertEqual(environment["session_type"], "wayland")
        self.assertEqual(environment["wm_or_de"], "sway")

    def test_detect_environment_tty_simulated(self) -> None:
        environment = detect_environment(
            env={
                "RETROFX_V2_FORCE_SESSION_TYPE": "tty",
                "TERM": "linux",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
            path_lookup=lambda _name: None,
        )
        self.assertEqual(environment["session_type"], "tty")
        self.assertEqual(environment["wm_or_de"], "unknown")

    def test_plan_generation_for_crt_profile_x11(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "strict-green-crt.toml",
            env={
                "DISPLAY": ":1",
                "XDG_SESSION_TYPE": "x11",
                "XDG_CURRENT_DESKTOP": "i3",
                "I3SOCK": "/tmp/i3.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stage"], "session-plan")
        self.assertIn("i3", payload["plan"]["apply_preview_targets"])
        self.assertIn("xresources", payload["plan"]["apply_preview_targets"])
        self.assertIn("sway", payload["plan"]["degraded_targets"])

    def test_plan_generation_for_theme_only_profile_wayland(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "warm-night-theme-only.toml",
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
        self.assertIn("sway", payload["plan"]["apply_preview_targets"])
        self.assertIn("gtk-export", payload["plan"]["compile_targets"])
        self.assertIn("qt-export", payload["plan"]["compile_targets"])
        self.assertEqual(payload["plan"]["toolkit_style"]["overall_status"], "export-only-advisory")

    def test_deterministic_plan_output_for_same_input(self) -> None:
        env = {
            "WAYLAND_DISPLAY": "wayland-0",
            "XDG_SESSION_TYPE": "wayland",
            "XDG_CURRENT_DESKTOP": "sway",
            "SWAYSOCK": "/tmp/sway.sock",
            "TERM": "xterm-256color",
        }
        payload_a = plan_profile_session(
            FIXTURES / "modern-minimal-wm.toml",
            env=env,
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        payload_b = plan_profile_session(
            FIXTURES / "modern-minimal-wm.toml",
            env=env,
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertEqual(
            json.dumps(payload_a["plan"], sort_keys=True),
            json.dumps(payload_b["plan"], sort_keys=True),
        )

    def test_unsupported_and_degraded_paths_are_reported(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "warm-night-theme-only.toml",
            env={
                "RETROFX_V2_FORCE_SESSION_TYPE": "tty",
                "TERM": "linux",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertIn("i3", payload["plan"]["degraded_targets"])
        self.assertIn("gtk-export", payload["plan"]["degraded_targets"])
        self.assertIn("qt-export", payload["plan"]["degraded_targets"])

    def test_plan_preview_bundle_is_written(self) -> None:
        with TemporaryDirectory() as tmpdir:
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
                out_root=tmpdir,
                write_preview=True,
            )
            self.assertTrue(payload["ok"])
            preview_dir = Path(payload["preview_bundle"]["output_dir"])
            self.assertTrue((preview_dir / "session-plan.json").is_file())
            self.assertTrue((preview_dir / "summary.txt").is_file())

    def test_dev_plan_entrypoint_emits_json(self) -> None:
        with TemporaryDirectory() as tmpdir:
            env = dict(
                DISPLAY=":1",
                XDG_SESSION_TYPE="x11",
                XDG_CURRENT_DESKTOP="i3",
                I3SOCK="/tmp/i3.sock",
                TERM="xterm-256color",
                PYTHONPATH=str(REPO_ROOT),
                PATH=str(Path("/usr/bin")) + ":" + str(Path("/bin")),
            )
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.plan_session",
                    str(FIXTURES / "strict-green-crt.toml"),
                    "--out-root",
                    tmpdir,
                    "--write-preview",
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "session-plan")
            self.assertIsNotNone(payload["preview_bundle"])

    def test_wayland_gnome_like_plan_is_explicitly_export_only(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "warm-night-theme-only.toml",
            env={
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "GNOME",
                "GNOME_DESKTOP_SESSION_ID": "this",
                "RETROFX_V2_FORCE_WM_OR_DE": "gnome",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["environment"]["wm_or_de"], "gnome")
        self.assertFalse(payload["environment"]["capability_hints"]["wm_outputs_meaningful"])
        self.assertTrue(payload["environment"]["capability_hints"]["wayland_export_only_desktop"])
        self.assertEqual(payload["plan"]["apply_preview_targets"], [])
        self.assertIn("Wayland `gnome` sessions are not part of the currently validated broader-alpha set; treat GUI-facing outputs here as export-oriented validation only.", payload["plan"]["warnings"])


if __name__ == "__main__":
    unittest.main()
