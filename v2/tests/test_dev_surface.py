"""Tests for the unified TWO-20 dev surface."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class UnifiedDevSurfaceTests(unittest.TestCase):
    def test_unified_entrypoint_help_works(self) -> None:
        process = self._run([str(ENTRYPOINT), "--help"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        self.assertIn("status", process.stdout)
        self.assertIn("resolve", process.stdout)
        self.assertIn("smoke", process.stdout)

    def test_status_report_runs(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_env(tmphome)
            process = self._run([str(ENTRYPOINT), "status"], env=env)
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "platform-status")
            self.assertIn("implemented_status_matrix", payload)
            self.assertIn("current_activation", payload["implemented_surface"])

    def test_resolve_plan_compile_apply_off_are_reachable(self) -> None:
        with TemporaryDirectory() as tmphome, TemporaryDirectory() as tmpout:
            env = self._temp_env(tmphome)
            plan_env = {
                **env,
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "sway",
                "SWAYSOCK": "/tmp/sway.sock",
                "TERM": "xterm-256color",
            }

            resolve = self._run([str(ENTRYPOINT), "resolve", str(FIXTURES / "warm-night-theme-only.toml")], env=plan_env)
            self.assertEqual(resolve.returncode, 0, msg=resolve.stderr)

            plan = self._run(
                [str(ENTRYPOINT), "plan", str(FIXTURES / "warm-night-theme-only.toml"), "--out-root", tmpout, "--write-preview"],
                env=plan_env,
            )
            self.assertEqual(plan.returncode, 0, msg=plan.stderr)

            compile_result = self._run(
                [
                    str(ENTRYPOINT),
                    "compile",
                    str(FIXTURES / "warm-night-theme-only.toml"),
                    "--out-root",
                    tmpout,
                    "--target",
                    "gtk-export",
                ],
                env=plan_env,
            )
            self.assertEqual(compile_result.returncode, 0, msg=compile_result.stderr)

            apply_result = self._run([str(ENTRYPOINT), "apply", str(FIXTURES / "warm-night-theme-only.toml")], env=plan_env)
            self.assertEqual(apply_result.returncode, 0, msg=apply_result.stderr)
            apply_payload = json.loads(apply_result.stdout)
            self.assertTrue(apply_payload["ok"])

            off_result = self._run([str(ENTRYPOINT), "off"], env=env)
            self.assertEqual(off_result.returncode, 0, msg=off_result.stderr)
            off_payload = json.loads(off_result.stdout)
            self.assertTrue(off_payload["ok"])

    def test_machine_readable_summary_mentions_expected_commands(self) -> None:
        process = self._run([str(ENTRYPOINT), "capabilities"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        payload = json.loads(process.stdout)
        command_names = [item["command"] for item in payload["dev_surface"]["commands"]]
        self.assertIn("status", command_names)
        self.assertIn("apply", command_names)
        self.assertIn("migrate inspect-1x", command_names)
        areas = [item["area"] for item in payload["implemented_status_matrix"]]
        self.assertIn("X11 render or compiler", areas)
        self.assertIn("live Wayland render", areas)

    def test_smoke_workflow_runs_non_destructively(self) -> None:
        with TemporaryDirectory() as tmphome, TemporaryDirectory() as tmpout:
            env = self._temp_env(tmphome)
            env.update(
                {
                    "WAYLAND_DISPLAY": "wayland-0",
                    "XDG_SESSION_TYPE": "wayland",
                    "XDG_CURRENT_DESKTOP": "sway",
                    "SWAYSOCK": "/tmp/sway.sock",
                    "TERM": "xterm-256color",
                }
            )
            process = self._run(
                [
                    str(ENTRYPOINT),
                    "smoke",
                    "--pack",
                    "modern-minimal",
                    "--profile-id",
                    "warm-night",
                    "--out-root",
                    tmpout,
                ],
                env=env,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertIsNone(payload["steps"]["apply"])
            compile_root = Path(payload["steps"]["compile"]["profile_output_root"])
            self.assertTrue(compile_root.is_dir())

    def test_status_doc_mentions_current_platform_truth(self) -> None:
        content = (REPO_ROOT / "docs" / "v2" / "IMPLEMENTED_STATUS.md").read_text(encoding="utf-8")
        self.assertIn("schema validation", content)
        self.assertIn("bounded apply or off", content)
        self.assertIn("live Wayland render", content)

    def _temp_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
            "PATH": "/usr/bin:/bin",
        }

    def _run(self, args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        run_env = dict(env or {})
        run_env.setdefault("PYTHONPATH", str(REPO_ROOT))
        return subprocess.run(
            args,
            cwd=REPO_ROOT,
            env=run_env,
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
