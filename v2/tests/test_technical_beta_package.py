"""Tests for the TWO-32 limited technical-beta candidate surface."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from v2.dev.package_technical_beta import build_technical_beta_package

REPO_ROOT = Path(__file__).resolve().parents[2]
TECHBETA_ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2-techbeta"
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class TechnicalBetaPackageTests(unittest.TestCase):
    def test_technical_beta_wrapper_help_limits_surface(self) -> None:
        process = self._run([str(TECHBETA_ENTRYPOINT), "--help"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        self.assertIn("status", process.stdout)
        self.assertIn("diagnostics", process.stdout)
        self.assertIn("apply", process.stdout)
        self.assertIn("technical-beta", process.stdout)
        self.assertNotIn("preview-x11", process.stdout)
        self.assertNotIn("migrate", process.stdout)
        self.assertNotIn("package-alpha", process.stdout)

    def test_technical_beta_status_reports_candidate_ready(self) -> None:
        with TemporaryDirectory() as tmphome:
            process = self._run([str(TECHBETA_ENTRYPOINT), "status"], env=self._temp_env(tmphome))
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertEqual(payload["stage"], "technical-beta-status")
            self.assertEqual(payload["release_status"]["version"], "2.0.0-techbeta.1")
            self.assertEqual(payload["release_status"]["status_label"], "technical-beta")
            self.assertTrue(payload["release_status"]["ready_for_limited_public_technical_beta"])
            self.assertTrue(payload["release_status"]["ready_for_public_technical_beta_candidate"])
            self.assertEqual(payload["release_status"]["public_surface_position"], "limited-public-technical-beta-candidate")
            commands = [item["command"] for item in payload["dev_surface"]["commands"]]
            self.assertIn("diagnostics", commands)
            self.assertNotIn("preview-x11", commands)
            self.assertNotIn("migrate inspect-1x", commands)

    def test_technical_beta_apply_rejects_wayland(self) -> None:
        with TemporaryDirectory() as tmphome:
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
            process = self._run([str(TECHBETA_ENTRYPOINT), "apply", str(FIXTURES / "warm-night-theme-only.toml")], env=env)
            self.assertEqual(process.returncode, 1, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertEqual(payload["errors"][0]["code"], "technical-beta-unsupported-apply-environment")

    def test_technical_beta_package_generation(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_technical_beta_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                allow_dirty=True,
            )
            self.assertTrue(payload["ok"])
            package_dir = Path(payload["package"]["output_dir"])
            self.assertTrue((package_dir / "package-manifest.json").is_file())
            self.assertTrue((package_dir / "bin" / "retrofx-v2-techbeta").is_file())
            self.assertTrue((package_dir / "toolchain" / "v2").is_dir())
            self.assertTrue((package_dir / "toolchain" / "scripts" / "dev" / "retrofx-v2-techbeta").is_file())
            self.assertTrue((package_dir / "docs" / "TECHNICAL_BETA_CANDIDATE_NOTES.md").is_file())
            manifest = json.loads((package_dir / "package-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "retrofx.technical-beta-package/v2alpha1")
            self.assertEqual(manifest["release_status"]["version"], "2.0.0-techbeta.1")
            self.assertEqual(manifest["release_status"]["status_label"], "technical-beta")
            self.assertEqual(manifest["distribution"]["scope"], "limited-public-technical-beta")
            self.assertEqual(manifest["distribution"]["toolchain_mode"], "copied-toolchain")
            self.assertEqual(manifest["toolchain"]["entrypoint_relative_path"], "bin/retrofx-v2-techbeta")
            self.assertTrue(manifest["release_status"]["ready_for_limited_public_technical_beta"])

    def test_packaged_wrapper_help_and_temp_home_install_flow(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome, TemporaryDirectory() as tmpdiag:
            payload = build_technical_beta_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                allow_dirty=True,
            )
            package_dir = Path(payload["package"]["output_dir"])
            env = self._temp_env(tmphome)

            help_process = self._run([str(package_dir / "bin" / "retrofx-v2-techbeta"), "--help"], env=env, cwd=package_dir)
            self.assertEqual(help_process.returncode, 0, msg=help_process.stderr)
            self.assertIn("limited technical-beta", help_process.stdout)

            install_process = self._run(
                [str(package_dir / "bin" / "retrofx-v2-techbeta"), "install", str(package_dir / "bundle")],
                env=env,
                cwd=package_dir,
            )
            self.assertEqual(install_process.returncode, 0, msg=install_process.stderr)
            install_payload = json.loads(install_process.stdout)
            self.assertEqual(install_payload["release_status"]["status_label"], "technical-beta")

            diagnostics_process = self._run(
                [
                    str(package_dir / "bin" / "retrofx-v2-techbeta"),
                    "diagnostics",
                    "--pack",
                    "modern-minimal",
                    "--profile-id",
                    "warm-night",
                    "--output-root",
                    tmpdiag,
                    "--label",
                    "techbeta",
                ],
                env=env,
                cwd=package_dir,
            )
            self.assertEqual(diagnostics_process.returncode, 0, msg=diagnostics_process.stderr)
            diagnostics_payload = json.loads(diagnostics_process.stdout)
            self.assertTrue((Path(diagnostics_payload["capture"]["output_dir"]) / "capture-manifest.json").is_file())

            uninstall_process = self._run(
                [str(package_dir / "bin" / "retrofx-v2-techbeta"), "uninstall", "modern-minimal--warm-night"],
                env=env,
                cwd=package_dir,
            )
            self.assertEqual(uninstall_process.returncode, 0, msg=uninstall_process.stderr)
            uninstall_payload = json.loads(uninstall_process.stdout)
            self.assertTrue(uninstall_payload["ok"])

    def _temp_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
            "PATH": "/usr/bin:/bin",
        }

    def _run(
        self,
        args: list[str],
        *,
        env: dict[str, str] | None = None,
        cwd: str | Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=cwd or REPO_ROOT,
            env=dict(env or {}),
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
