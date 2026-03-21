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
        self.assertIn("package-alpha", process.stdout)
        self.assertIn("diagnostics", process.stdout)
        self.assertIn("smoke", process.stdout)
        self.assertIn("not yet", process.stdout)
        self.assertIn("limited public technical beta", process.stdout)

    def test_delegated_help_uses_unified_prog_names(self) -> None:
        for command, expected_usage in (
            ("resolve", "usage: retrofx-v2 resolve"),
            ("bundle", "usage: retrofx-v2 bundle"),
            ("apply", "usage: retrofx-v2 apply"),
        ):
            process = self._run([str(ENTRYPOINT), command, "--help"])
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            self.assertIn(expected_usage, process.stdout)
            self.assertNotIn("usage: cli.py", process.stdout)

    def test_status_report_runs(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_env(tmphome)
            process = self._run([str(ENTRYPOINT), "status"], env=env)
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "platform-status")
            self.assertIn("release_status", payload)
            self.assertIn("source_control", payload)
            self.assertIn("ready_for_internal_alpha_continuation", payload["release_status"])
            self.assertIn("ready_for_local_alpha_tag_candidate", payload["release_status"])
            self.assertIn("alpha_candidate_ready", payload["release_status"])
            self.assertIn("ready_for_controlled_internal_alpha", payload["release_status"])
            self.assertIn("ready_for_broader_alpha", payload["release_status"])
            self.assertIn("ready_for_non_public_pre_beta", payload["release_status"])
            self.assertIn("ready_for_local_pre_beta_tag_candidate", payload["release_status"])
            self.assertIn("pre_beta_candidate_ready", payload["release_status"])
            self.assertIn("ready_for_limited_public_technical_beta", payload["release_status"])
            self.assertIn("ready_for_public_technical_beta_candidate", payload["release_status"])
            self.assertIn("needs_public_surface_hardening", payload["release_status"])
            self.assertIn("public_surface_position", payload["release_status"])
            self.assertIn("public_beta_blockers", payload["release_status"])
            self.assertIn("ready_for_pre_beta_stabilization", payload["release_status"])
            self.assertIn("local_tag_exists", payload["release_status"])
            self.assertIn("local_tag_name", payload["release_status"])
            self.assertIn("local_tag_state", payload["release_status"])
            self.assertIn("local_tag_points_at_head", payload["release_status"])
            self.assertIn("latest_existing_local_alpha_tag", payload["release_status"])
            self.assertIn("proposed_pre_beta_version", payload["release_status"])
            self.assertIn("proposed_pre_beta_tag_name", payload["release_status"])
            self.assertIn("latest_existing_local_pre_beta_tag", payload["release_status"])
            self.assertIn("current_build_kind", payload["release_status"])
            self.assertFalse(payload["release_status"]["ready_for_controlled_alpha"])
            self.assertFalse(payload["release_status"]["ready_for_local_alpha_tag_candidate"])
            self.assertFalse(payload["release_status"]["alpha_candidate_ready"])
            self.assertFalse(payload["release_status"]["ready_for_broader_alpha"])
            self.assertFalse(payload["release_status"]["ready_for_non_public_pre_beta"])
            self.assertFalse(payload["release_status"]["ready_for_local_pre_beta_tag_candidate"])
            self.assertFalse(payload["release_status"]["pre_beta_candidate_ready"])
            self.assertFalse(payload["release_status"]["ready_for_limited_public_technical_beta"])
            self.assertFalse(payload["release_status"]["ready_for_public_technical_beta_candidate"])
            self.assertTrue(payload["release_status"]["needs_public_surface_hardening"])
            self.assertEqual(payload["release_status"]["public_surface_position"], "internal-only")
            self.assertFalse(payload["release_status"]["ready_for_pre_beta_stabilization"])
            self.assertEqual(payload["release_status"]["proposed_pre_beta_version"], "2.0.0-prebeta.internal.1")
            self.assertEqual(payload["release_status"]["current_build_kind"], "untagged-post-alpha-hardening")
            self.assertIn("implemented_status_matrix", payload)
            self.assertIn("implemented_interfaces", payload)
            self.assertIn("install_state", payload["implemented_surface"])
            self.assertIn("current_activation", payload["implemented_surface"])
            self.assertGreaterEqual(payload["implemented_interfaces"]["count"], 6)

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
        self.assertIn("package-alpha", command_names)
        self.assertIn("diagnostics", command_names)
        self.assertIn("migrate inspect-1x", command_names)
        areas = [item["area"] for item in payload["implemented_status_matrix"]]
        self.assertIn("X11 render or compiler", areas)
        self.assertIn("live Wayland render", areas)
        interface_names = [item["name"] for item in payload["implemented_interfaces"]["interfaces"]]
        self.assertIn("resolved-profile", interface_names)
        self.assertIn("session-plan", interface_names)
        self.assertFalse(payload["release_status"]["ready_for_limited_public_technical_beta"])
        self.assertIn("package, install, and diagnostics surfaces remain repo-checkout dependent", payload["release_status"]["public_beta_blockers"][1])

    def test_option_only_pack_selector_reaches_bundle_subcommand(self) -> None:
        with TemporaryDirectory() as tmpbundle:
            process = self._run(
                [
                    str(ENTRYPOINT),
                    "bundle",
                    "--pack",
                    "modern-minimal",
                    "--profile-id",
                    "warm-night",
                    "--bundle-root",
                    tmpbundle,
                ]
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "bundle")
            self.assertEqual(payload["profile"]["id"], "warm-night")

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

    def test_implemented_interfaces_doc_mentions_current_contracts(self) -> None:
        content = (REPO_ROOT / "docs" / "v2" / "IMPLEMENTED_INTERFACES.md").read_text(encoding="utf-8")
        self.assertIn("resolved profile", content)
        self.assertIn("target compile result", content)
        self.assertIn("migration report", content)

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
