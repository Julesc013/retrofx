"""Tests for the TWO-25 controlled internal alpha support layer."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from v2.dev.capture_diagnostics import capture_diagnostics
from v2.dev.package_alpha import build_internal_alpha_package
from v2.session.install import install_dev_bundle

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"


class AlphaSupportTests(unittest.TestCase):
    def test_diagnostics_capture_helper_emits_expected_artifacts(self) -> None:
        with TemporaryDirectory() as tmpout, TemporaryDirectory() as tmphome:
            payload = capture_diagnostics(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                output_root=tmpout,
                label="smoke",
                env=self._temp_env(tmphome),
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T12:30:00Z",
            )
            self.assertTrue(payload["ok"])
            capture_dir = Path(payload["capture"]["output_dir"])
            self.assertTrue((capture_dir / "capture-manifest.json").is_file())
            self.assertTrue((capture_dir / "source-control.json").is_file())
            self.assertTrue((capture_dir / "platform-status.json").is_file())
            self.assertTrue((capture_dir / "environment.json").is_file())
            self.assertTrue((capture_dir / "install-state.json").is_file())
            self.assertTrue((capture_dir / "current-activation.json").is_file())
            self.assertTrue((capture_dir / "profile" / "resolved-profile.json").is_file())
            self.assertTrue((capture_dir / "profile" / "session-plan.json").is_file())
            self.assertTrue((capture_dir / "profile" / "output-inventory.json").is_file())
            self.assertTrue((capture_dir / "profile" / "install-bundle-inventory.json").is_file())
            manifest = json.loads((capture_dir / "capture-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("capture-manifest.json", manifest["artifacts"])
            self.assertIn("source-control.json", manifest["artifacts"])
            self.assertTrue(manifest["included_sections"]["source_control"])
            source_control = json.loads((capture_dir / "source-control.json").read_text(encoding="utf-8"))
            self.assertIn("working_tree_clean", source_control)
            install_bundle_inventory = json.loads(
                (capture_dir / "profile" / "install-bundle-inventory.json").read_text(encoding="utf-8")
            )
            self.assertFalse(install_bundle_inventory["present"])

    def test_diagnostics_capture_observes_packaged_install_state(self) -> None:
        with TemporaryDirectory() as tmppackages, TemporaryDirectory() as tmpdiag, TemporaryDirectory() as tmphome:
            env = self._temp_env(tmphome)
            package = build_internal_alpha_package(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                package_root=tmppackages,
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
            )
            install_dev_bundle(Path(package["package"]["output_dir"]) / "bundle", env=env, now="2026-03-21T12:31:00Z")

            payload = capture_diagnostics(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                output_root=tmpdiag,
                label="installed",
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T12:32:00Z",
            )
            install_state = json.loads((Path(payload["capture"]["output_dir"]) / "install-state.json").read_text(encoding="utf-8"))
            installed = install_state["installed_bundles"]
            self.assertEqual(len(installed), 1)
            self.assertEqual(installed[0]["bundle_id"], "modern-minimal--warm-night")
            self.assertEqual(installed[0]["release_status"], "internal-alpha")
            capture_dir = Path(payload["capture"]["output_dir"])
            install_bundle_inventory = json.loads(
                (capture_dir / "profile" / "install-bundle-inventory.json").read_text(encoding="utf-8")
            )
            self.assertTrue(install_bundle_inventory["present"])
            self.assertEqual(install_bundle_inventory["bundle_id"], "modern-minimal--warm-night")
            self.assertTrue((capture_dir / "profile" / "install-bundle-manifest.json").is_file())
            self.assertTrue((capture_dir / "profile" / "source-package-manifest.json").is_file())

    def test_diagnostics_capture_does_not_create_1x_paths(self) -> None:
        with TemporaryDirectory() as tmpout, TemporaryDirectory() as tmphome:
            env = self._temp_env(tmphome)
            payload = capture_diagnostics(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                output_root=tmpout,
                label="safe",
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
                now="2026-03-21T12:33:00Z",
            )
            self.assertTrue(payload["ok"])
            self.assertFalse((Path(tmphome) / ".config" / "retrofx").exists())
            self.assertFalse((Path(tmphome) / ".local" / "bin" / "retrofx").exists())

    def test_alpha_docs_exist_and_reference_real_flows(self) -> None:
        doc_expectations = {
            "docs/v2/CONTROLLED_ALPHA_PLAN.md": ["scripts/dev/retrofx-v2", "apply", "migration"],
            "docs/v2/ALPHA_TRIAGE.md": ["alpha-blocker", "install-bundle", "x11-experimental-render"],
            "docs/v2/ALPHA_EXECUTION_CHECKLIST.md": ["diagnostics", "package-alpha", "migrate inspect-1x"],
            "docs/v2/ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md": ["branch", "session type", "diagnostics directory"],
            "docs/v2/ALPHA_FEEDBACK_TEMPLATE.md": ["degraded-pass", "severity", "category"],
            "docs/v2/ALPHA_ISSUE_TEMPLATE.md": ["alpha-blocker", "Commands:", "diagnostics directory"],
            "docs/v2/POST_ALPHA_DECISION_RULES.md": ["Continue Alpha As-Is", "Enter Alpha Remediation", "Expand The Tester Set"],
            "docs/v2/ALPHA_CANDIDATE_SUMMARY.md": ["ALPHA_CANDIDATE_READY=yes", "v2.0.0-alpha.internal.1", "package-alpha"],
            "docs/v2/BROADER_ALPHA_READINESS.md": ["READY_FOR_BROADER_ALPHA=no", "READY_FOR_PRE_BETA_STABILIZATION=no", "internal alpha only"],
            "docs/v2/PRE_BETA_GATES.md": ["broader alpha", "pre-beta", "deterministic"],
            "docs/v2/NEXT_STAGE_VERDICT.md": ["READY_FOR_INTERNAL_ALPHA_CONTINUATION", "READY_FOR_BROADER_ALPHA", "READY_FOR_PRE_BETA_STABILIZATION"],
        }
        for relative_path, expected_strings in doc_expectations.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for expected in expected_strings:
                self.assertIn(expected, content, msg=f"{relative_path} missing `{expected}`")

    def test_unified_dev_surface_exposes_diagnostics(self) -> None:
        process = self._run([str(ENTRYPOINT), "--help"])
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        self.assertIn("diagnostics", process.stdout)

        help_process = self._run([str(ENTRYPOINT), "diagnostics", "--help"])
        self.assertEqual(help_process.returncode, 0, msg=help_process.stderr)
        self.assertIn("retrofx-v2 diagnostics", help_process.stdout)
        self.assertIn("--output-root", help_process.stdout)

    def _temp_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
            "PATH": "/usr/bin:/bin",
            "PYTHONPATH": str(REPO_ROOT),
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
