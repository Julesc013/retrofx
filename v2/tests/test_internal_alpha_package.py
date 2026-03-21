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
                allow_dirty=True,
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
            self.assertTrue((package_dir / "docs" / "ALPHA_CANDIDATE_SUMMARY.md").is_file())
            self.assertTrue((package_dir / "docs" / "ALPHA_RELEASE_CHECKLIST.md").is_file())
            self.assertTrue((package_dir / "docs" / "PRE_BETA_BLOCKERS.md").is_file())
            self.assertTrue((package_dir / "docs" / "PRE_BETA_CANDIDATE_NOTES.md").is_file())
            self.assertTrue((package_dir / "docs" / "PRE_BETA_CANDIDATE_SUMMARY.md").is_file())
            self.assertTrue((package_dir / "docs" / "PRE_BETA_READINESS.md").is_file())
            self.assertTrue((package_dir / "docs" / "PRE_BETA_RELEASE_CHECKLIST.md").is_file())
            self.assertTrue((package_dir / "docs" / "PUBLIC_BETA_RISK_SURFACE.md").is_file())
            self.assertTrue((package_dir / "docs" / "PUBLIC_BETA_GATES.md").is_file())
            self.assertTrue((package_dir / "docs" / "PUBLIC_BETA_BLOCKERS.md").is_file())
            self.assertTrue((package_dir / "docs" / "PUBLIC_BETA_READINESS.md").is_file())
            self.assertTrue((package_dir / "docs" / "TECHNICAL_BETA_NOTES.md").is_file())
            self.assertTrue((package_dir / "docs" / "TECHNICAL_BETA_CHECKLIST.md").is_file())

    def test_package_manifest_contains_required_internal_alpha_fields(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_internal_alpha_package(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                package_root=tmppackages,
                allow_dirty=True,
            )
            manifest = json.loads(Path(payload["package"]["manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "retrofx.internal-alpha-package/v2alpha1")
            self.assertEqual(manifest["release_status"]["version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(manifest["release_status"]["status_label"], CURRENT_STATUS_LABEL)
            self.assertIn("source_control", manifest["release_status"])
            self.assertIn("working_tree_clean", manifest["release_status"])
            self.assertIn("ready_for_internal_alpha_continuation", manifest["release_status"])
            self.assertIn("ready_for_local_alpha_tag_candidate", manifest["release_status"])
            self.assertIn("alpha_candidate_ready", manifest["release_status"])
            self.assertIn("ready_for_controlled_internal_alpha", manifest["release_status"])
            self.assertIn("ready_for_broader_alpha", manifest["release_status"])
            self.assertIn("ready_for_non_public_pre_beta", manifest["release_status"])
            self.assertIn("ready_for_local_pre_beta_tag_candidate", manifest["release_status"])
            self.assertIn("pre_beta_candidate_ready", manifest["release_status"])
            self.assertIn("ready_for_limited_public_technical_beta", manifest["release_status"])
            self.assertIn("ready_for_public_technical_beta_candidate", manifest["release_status"])
            self.assertIn("needs_public_surface_hardening", manifest["release_status"])
            self.assertIn("public_surface_position", manifest["release_status"])
            self.assertIn("public_beta_blockers", manifest["release_status"])
            self.assertIn("ready_for_pre_beta_stabilization", manifest["release_status"])
            self.assertIn("local_tag_exists", manifest["release_status"])
            self.assertIn("local_tag_name", manifest["release_status"])
            self.assertIn("local_tag_state", manifest["release_status"])
            self.assertIn("local_tag_points_at_head", manifest["release_status"])
            self.assertIn("latest_existing_local_alpha_tag", manifest["release_status"])
            self.assertIn("proposed_pre_beta_version", manifest["release_status"])
            self.assertIn("proposed_pre_beta_tag_name", manifest["release_status"])
            self.assertIn("latest_existing_local_pre_beta_tag", manifest["release_status"])
            self.assertIn("current_build_kind", manifest["release_status"])
            self.assertFalse(manifest["release_status"]["ready_for_controlled_alpha"])
            self.assertFalse(manifest["release_status"]["ready_for_local_alpha_tag_candidate"])
            self.assertFalse(manifest["release_status"]["alpha_candidate_ready"])
            self.assertFalse(manifest["release_status"]["ready_for_broader_alpha"])
            self.assertFalse(manifest["release_status"]["ready_for_non_public_pre_beta"])
            self.assertFalse(manifest["release_status"]["ready_for_local_pre_beta_tag_candidate"])
            self.assertFalse(manifest["release_status"]["pre_beta_candidate_ready"])
            self.assertFalse(manifest["release_status"]["ready_for_limited_public_technical_beta"])
            self.assertFalse(manifest["release_status"]["ready_for_public_technical_beta_candidate"])
            self.assertTrue(manifest["release_status"]["needs_public_surface_hardening"])
            self.assertEqual(manifest["release_status"]["public_surface_position"], "internal-only")
            self.assertFalse(manifest["release_status"]["ready_for_pre_beta_stabilization"])
            self.assertEqual(manifest["release_status"]["proposed_pre_beta_version"], "2.0.0-prebeta.internal.1")
            self.assertEqual(manifest["release_status"]["current_build_kind"], "untagged-post-alpha-hardening")
            self.assertEqual(manifest["release_status"]["latest_existing_local_alpha_tag"], "v2.0.0-alpha.internal.1")
            self.assertEqual(manifest["distribution"]["scope"], "internal-non-public")
            self.assertEqual(manifest["bundle"]["relative_dir"], "bundle")
            self.assertIn("terminal-tui", manifest["supported_target_families"])
            self.assertIn("scripts/dev/retrofx-v2 status", manifest["recommended_smoke_flow"])
            self.assertIn("docs/INTERNAL_ALPHA_RUNBOOK.md", manifest["included_docs"])
            self.assertIn("docs/ALPHA_CANDIDATE_NOTES.md", manifest["included_docs"])
            self.assertIn("docs/ALPHA_CANDIDATE_SUMMARY.md", manifest["included_docs"])
            self.assertIn("docs/BROADER_ALPHA_READINESS.md", manifest["included_docs"])
            self.assertIn("docs/PRE_BETA_BLOCKERS.md", manifest["included_docs"])
            self.assertIn("docs/PRE_BETA_CANDIDATE_NOTES.md", manifest["included_docs"])
            self.assertIn("docs/PRE_BETA_CANDIDATE_SUMMARY.md", manifest["included_docs"])
            self.assertIn("docs/PRE_BETA_READINESS.md", manifest["included_docs"])
            self.assertIn("docs/PRE_BETA_RELEASE_CHECKLIST.md", manifest["included_docs"])
            self.assertIn("docs/PUBLIC_BETA_RISK_SURFACE.md", manifest["included_docs"])
            self.assertIn("docs/PUBLIC_BETA_GATES.md", manifest["included_docs"])
            self.assertIn("docs/PUBLIC_BETA_BLOCKERS.md", manifest["included_docs"])
            self.assertIn("docs/PUBLIC_BETA_READINESS.md", manifest["included_docs"])
            self.assertIn("docs/TECHNICAL_BETA_NOTES.md", manifest["included_docs"])
            self.assertIn("docs/TECHNICAL_BETA_CHECKLIST.md", manifest["included_docs"])
            self.assertTrue(manifest["metadata_artifacts"])

    def test_publicish_status_label_override_is_blocked(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                allow_dirty=True,
                status_label="pre-beta",
            )
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["errors"][0]["code"], "blocked-package-status-label")

    def test_publicish_version_override_is_blocked(self) -> None:
        with TemporaryDirectory() as tmppackages:
            payload = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                allow_dirty=True,
                version="2.0.0-prebeta.internal.1",
            )
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["errors"][0]["code"], "blocked-package-version-override")

    def test_packaged_bundle_installs_into_temp_home(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                allow_dirty=True,
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
                allow_dirty=True,
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
                allow_dirty=True,
            )
            env = self._temp_home_env(tmphome)
            install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:00:00Z")
            status = describe_install_state(env=env, cwd=REPO_ROOT)
            self.assertTrue(status["ok"])
            self.assertEqual(status["installed_bundles"][0]["release_version"], CURRENT_EXPERIMENTAL_VERSION)
            self.assertEqual(status["installed_bundles"][0]["release_status"], CURRENT_STATUS_LABEL)

    def test_dirty_tree_package_generation_is_blocked_by_default(self) -> None:
        dirty_marker = REPO_ROOT / "v2" / ".two29-dirty-package-test"
        try:
            dirty_marker.write_text("dirty\n", encoding="utf-8")
            with TemporaryDirectory() as tmppackages:
                blocked = build_internal_alpha_package(
                    pack_id="modern-minimal",
                    pack_profile_id="warm-night",
                    package_root=tmppackages,
                )
                self.assertFalse(blocked["ok"])
                self.assertEqual(blocked["errors"][0]["code"], "dirty-working-tree")

                allowed = build_internal_alpha_package(
                    pack_id="modern-minimal",
                    pack_profile_id="warm-night",
                    package_root=tmppackages,
                    allow_dirty=True,
                )
                self.assertTrue(allowed["ok"])
        finally:
            dirty_marker.unlink(missing_ok=True)

    def test_runbook_relevant_package_commands_are_reachable(self) -> None:
        process = self._run([str(ENTRYPOINT), "package-alpha", "--pack", "modern-minimal", "--profile-id", "warm-night", "--help"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        self.assertIn("retrofx-v2 package-alpha", process.stdout)
        self.assertIn("--package-root", process.stdout)
        self.assertIn("--allow-dirty", process.stdout)
        self.assertIn("does not create a pre-beta", process.stdout)
        self.assertIn("public technical", process.stdout)

        wrapper_process = self._run([str(WRAPPER), "--help"])
        self.assertEqual(wrapper_process.returncode, 0, msg=wrapper_process.stderr)
        self.assertIn("retrofx-v2 package-alpha", wrapper_process.stdout)

    def test_packaged_install_does_not_collide_with_1x_paths(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmphome:
            package = build_internal_alpha_package(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                package_root=tmppackages,
                allow_dirty=True,
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
