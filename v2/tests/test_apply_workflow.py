"""Tests for the bounded TWO-19 apply/off workflow."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.session.apply import apply_dev_profile, describe_current_activation, off_dev_profile

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class ApplyWorkflowTests(unittest.TestCase):
    def test_apply_export_heavy_profile_creates_current_state_manifest(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            payload = apply_dev_profile(
                FIXTURES / "warm-night-theme-only.toml",
                env={
                    **env,
                    "WAYLAND_DISPLAY": "wayland-0",
                    "XDG_SESSION_TYPE": "wayland",
                    "XDG_CURRENT_DESKTOP": "sway",
                    "SWAYSOCK": "/tmp/sway.sock",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:00:00Z",
            )
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "apply")
            self.assertEqual(payload["activation"]["live_applied_targets"], [])
            current_state_path = Path(payload["activation"]["current_state_path"])
            manifest_path = Path(payload["activation"]["manifest_path"])
            self.assertTrue(current_state_path.is_file())
            self.assertTrue(manifest_path.is_file())
            current_state = json.loads(current_state_path.read_text(encoding="utf-8"))
            self.assertEqual(current_state["profile"]["id"], "warm-night-theme-only")
            self.assertIn("gtk-export", current_state["activation"]["activated_targets"])

    def test_apply_with_live_eligible_x11_probe_records_live_targets(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            payload = apply_dev_profile(
                FIXTURES / "strict-green-crt.toml",
                env={
                    **env,
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "XDG_CURRENT_DESKTOP": "i3",
                    "I3SOCK": "/tmp/i3.sock",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=lambda name: "/tmp/fake-picom" if name == "picom" else None,
                probe_x11=True,
                probe_seconds=0.1,
                command_runner=self._successful_runner,
                now="2026-03-21T10:05:00Z",
            )
            self.assertTrue(payload["ok"])
            self.assertIn("x11-picom", payload["activation"]["live_applied_targets"])
            self.assertIn("x11-shader", payload["activation"]["live_applied_targets"])
            manifest = json.loads(Path(payload["activation"]["manifest_path"]).read_text(encoding="utf-8"))
            self.assertTrue(manifest["activation"]["used_x11_live_probe"])

    def test_status_reporting_after_apply(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            apply_dev_profile(
                FIXTURES / "warm-night-theme-only.toml",
                env={**env, "WAYLAND_DISPLAY": "wayland-0", "XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "sway", "SWAYSOCK": "/tmp/sway.sock", "TERM": "xterm-256color"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:10:00Z",
            )
            status = describe_current_activation(env=env, cwd=REPO_ROOT)
            self.assertTrue(status["ok"])
            self.assertTrue(status["active"])
            self.assertEqual(status["activation"]["profile"]["id"], "warm-night-theme-only")
            self.assertIn("active_current_root", status["state_layout"])

    def test_off_clears_current_activation(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            apply_payload = apply_dev_profile(
                FIXTURES / "warm-night-theme-only.toml",
                env={**env, "WAYLAND_DISPLAY": "wayland-0", "XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "sway", "SWAYSOCK": "/tmp/sway.sock", "TERM": "xterm-256color"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:15:00Z",
            )
            current_root = Path(apply_payload["activation"]["current_root"])
            self.assertTrue(current_root.exists())
            off_payload = off_dev_profile(env=env, now="2026-03-21T10:16:00Z")
            self.assertTrue(off_payload["ok"])
            self.assertFalse(current_root.exists())
            status = describe_current_activation(env=env, cwd=REPO_ROOT)
            self.assertFalse(status["active"])

    def test_repeated_apply_updates_current_and_last_good(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            first = apply_dev_profile(
                FIXTURES / "warm-night-theme-only.toml",
                env={**env, "WAYLAND_DISPLAY": "wayland-0", "XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "sway", "SWAYSOCK": "/tmp/sway.sock", "TERM": "xterm-256color"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:20:00Z",
            )
            second = apply_dev_profile(
                FIXTURES / "retro-desktop-explicit.toml",
                env={**env, "DISPLAY": ":1", "XDG_SESSION_TYPE": "x11", "XDG_CURRENT_DESKTOP": "GNOME", "TERM": "xterm-256color"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:21:00Z",
            )
            self.assertTrue(first["ok"])
            self.assertTrue(second["ok"])
            status = describe_current_activation(env=env, cwd=REPO_ROOT)
            self.assertEqual(status["activation"]["profile"]["id"], "retro-desktop-explicit")
            last_good = json.loads((Path(env["XDG_STATE_HOME"]) / "retrofx-v2-dev" / "last-good" / "last-good.json").read_text(encoding="utf-8"))
            self.assertEqual(last_good["profile"]["id"], "warm-night-theme-only")

    def test_apply_in_unsupported_environment_degrades_without_live_side_effects(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            payload = apply_dev_profile(
                FIXTURES / "strict-green-crt.toml",
                env={**env, "RETROFX_V2_FORCE_SESSION_TYPE": "tty", "TERM": "linux"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:25:00Z",
            )
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["activation"]["live_applied_targets"], [])
            manifest = json.loads(Path(payload["activation"]["manifest_path"]).read_text(encoding="utf-8"))
            self.assertIn("x11-shader", manifest["activation"]["degraded_targets"])

    def test_off_when_nothing_is_active_is_clean(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            payload = off_dev_profile(env=env, now="2026-03-21T10:30:00Z")
            self.assertTrue(payload["ok"])
            self.assertFalse(payload["active"])
            self.assertEqual(payload["removed_paths"], [])

    def test_1x_paths_are_untouched_by_apply_and_off(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            apply_dev_profile(
                FIXTURES / "warm-night-theme-only.toml",
                env={**env, "WAYLAND_DISPLAY": "wayland-0", "XDG_SESSION_TYPE": "wayland", "XDG_CURRENT_DESKTOP": "sway", "SWAYSOCK": "/tmp/sway.sock", "TERM": "xterm-256color"},
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T10:35:00Z",
            )
            off_dev_profile(env=env, now="2026-03-21T10:36:00Z")
            self.assertFalse((Path(tmphome) / ".config" / "retrofx").exists())
            self.assertFalse((Path(tmphome) / ".local" / "bin" / "retrofx").exists())

    def test_dev_status_cli_emits_json(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            env.update({"PYTHONPATH": str(REPO_ROOT), "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin"))})
            process = subprocess.run(
                [sys.executable, "-m", "v2.session.apply.cli", "status"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "status")

    def _temp_home_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
        }

    def _successful_runner(self, command, **_kwargs):
        class Result:
            returncode = 0
            stderr = ""
            stdout = ""

        return Result()


if __name__ == "__main__":
    unittest.main()
