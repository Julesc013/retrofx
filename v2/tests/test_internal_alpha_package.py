"""Tests for the TWO-24 internal-alpha packaging flow."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from v2.dev.package_alpha import build_internal_alpha_package
from v2.dev.release import CURRENT_EXPERIMENTAL_VERSION, CURRENT_STATUS_LABEL
from v2.session.install import describe_install_state, install_dev_bundle, uninstall_dev_bundle

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"
WRAPPER = REPO_ROOT / "scripts" / "dev" / "retrofx-v2-package-alpha"


class InternalAlphaPackageTests(unittest.TestCase):
    def test_internal_alpha_package_generation(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
            )
            self.assertTrue(payload["ok"])
            package_dir = Path(payload["package"]["output_dir"])
            self.assertTrue((package_dir / "package-manifest.json").is_file())
            self.assertTrue((package_dir / "bundle" / "manifest.json").is_file())
            self.assertTrue((package_dir / "docs" / "INTERNAL_ALPHA_RUNBOOK.md").is_file())
            self.assertTrue((package_dir / "docs" / "INTERNAL_ALPHA_NOTES.md").is_file())
            self.assertTrue((package_dir / "docs" / "CONTROLLED_ALPHA_PLAN.md").is_file())
            self.assertTrue((package_dir / "docs" / "ALPHA_TRIAGE.md").is_file())
            self.assertTrue((package_dir / "docs" / "ALPHA_REMEDIATION_BACKLOG.md").is_file())
            self.assertTrue((package_dir / "docs" / "ALPHA_CANDIDATE_NOTES.md").is_file())
            self.assertTrue((package_dir / "docs" / "ALPHA_RELEASE_CHECKLIST.md").is_file())

    def test_package_manifest_contains_required_internal_alpha_fields(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_internal_alpha_package(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                package_root=tmppackages,
            )
            manifest = json.loads(Path(payload["package"]["manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "retrofx.internal-alpha-package/v2alpha1")
            self.assertEqual(manifest["release_status"]["version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(manifest["release_status"]["status_label"], CURRENT_STATUS_LABEL)
            self.assertIn("source_control", manifest["release_status"])
            self.assertIn("working_tree_clean", manifest["release_status"])
            self.assertIn("ready_for_internal_alpha_continuation", manifest["release_status"])
            self.assertIn("ready_for_local_alpha_tag_candidate", manifest["release_status"])
            self.assertEqual(manifest["distribution"]["scope"], "internal-non-public")
            self.assertEqual(manifest["bundle"]["relative_dir"], "bundle")
            self.assertIn("terminal-tui", manifest["supported_target_families"])
            self.assertIn("scripts/dev/retrofx-v2 status", manifest["recommended_smoke_flow"])
            self.assertIn("docs/INTERNAL_ALPHA_RUNBOOK.md", manifest["included_docs"])
            self.assertIn("docs/ALPHA_CANDIDATE_NOTES.md", manifest["included_docs"])
            self.assertTrue(manifest["metadata_artifacts"])

    def test_packaged_bundle_installs_into_temp_home(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
            )
            env = self._temp_home_env(tmphome)
            payload = install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:00:00Z")
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["release_status"]["version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(payload["release_status"]["status_label"], CURRENT_STATUS_LABEL)
            self.assertEqual(payload["record"]["experimental_release"]["version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(payload["record"]["experimental_release"]["status_label"], CURRENT_STATUS_LABEL)

    def test_packaged_bundle_uninstalls_cleanly(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
            )
            env = self._temp_home_env(tmphome)
            install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:00:00Z")
            uninstall_payload = uninstall_dev_bundle("modern-minimal--warm-night", env=env)
            self.assertTrue(uninstall_payload["ok"])
            self.assertFalse((Path(tmphome) / ".local" / "share" / "retrofx-v2-dev" / "bundles" / "modern-minimal--warm-night").exists())

    def test_install_state_exposes_release_version_and_status(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                package_root=tmppackages,
            )
            env = self._temp_home_env(tmphome)
            install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:00:00Z")
            status = describe_install_state(env=env, cwd=REPO_ROOT)
            self.assertTrue(status["ok"])
            self.assertEqual(status["installed_bundles"][0]["release_version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(status["installed_bundles"][0]["release_status"], CURRENT_STATUS_LABEL)

    def test_runbook_relevant_package_commands_are_reachable(self) -> None:
        process = self._run([str(ENTRYPOINT), "package-alpha", "--pack", "modern-minimal", "--profile-id", "warm-night", "--help"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        self.assertIn("retrofx-v2 package-alpha", process.stdout)
        self.assertIn("--package-root", process.stdout)

        wrapper_process = self._run([str(WRAPPER), "--help"])
        self.assertEqual(wrapper_process.returncode, 0, msg=wrapper_process.stderr)
        self.assertIn("retrofx-v2 package-alpha", wrapper_process.stdout)

    def test_packaged_install_does_not_collide_with_1x_paths(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                package_root=tmppackages,
            )
            env = self._temp_home_env(tmphome)
            install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:00:00Z")
            layout = describe_install_state(env=env, cwd=REPO_ROOT)["install_layout"]
            self.assertTrue(layout["config_root"].endswith("retrofx-v2-dev"))
            self.assertNotEqual(layout["config_root"], str(Path(tmphome) / ".config" / "retrofx"))
            self.assertNotEqual(layout["launcher_path"], str(Path(tmphome) / ".local" / "bin" / "retrofx"))

    def _temp_home_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
            "PYTHONPATH": str(REPO_ROOT),
            "PATH": "/usr/bin:/bin",
        }

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            env={"PYTHONPATH": str(REPO_ROOT), "PATH": "/usr/bin:/bin"},
        )


if __name__ == "__main__":
    unittest.main()
