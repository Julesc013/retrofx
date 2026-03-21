"""Structural contract tests for the hardened TWO-21 interface layer."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from v2.compat import inspect_legacy_profile
from v2.core.interfaces import (
    ACTIVATION_MANIFEST_KEYS,
    CURRENT_STATE_KEYS,
    IMPLEMENTED_INTERFACES,
    INSTALL_RECORD_KEYS,
    MIGRATION_REPORT_KEYS,
    MIGRATION_SUMMARY_KEYS,
    PACK_MANIFEST_KEYS,
    PACK_PROFILE_ENTRY_KEYS,
    RESOLVED_PROFILE_DECISIONS_KEYS,
    RESOLVED_PROFILE_SEMANTICS_KEYS,
    RESOLVED_PROFILE_TOP_LEVEL_KEYS,
    SESSION_PLAN_ENTRY_KEYS,
    SESSION_PLAN_KEYS,
    TARGET_ARTIFACT_KEYS,
    TARGET_COMPILE_RESULT_KEYS,
)
from v2.core.dev.compile_targets import compile_profile_to_output
from v2.core.pipeline import run_profile_pipeline
from v2.packs import load_pack_manifest
from v2.session.apply import apply_dev_profile, off_dev_profile
from v2.session.environment import detect_environment
from v2.session.install import build_dev_bundle, install_dev_bundle
from v2.session.planning import build_session_plan
from v2.targets import compile_resolved_profile_targets

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"
LEGACY_PROFILES = REPO_ROOT / "profiles" / "packs" / "core"


class InterfaceContractTests(unittest.TestCase):
    def test_contract_registry_lists_expected_surfaces(self) -> None:
        names = [entry["name"] for entry in IMPLEMENTED_INTERFACES]
        self.assertIn("resolved-profile", names)
        self.assertIn("target-compile-result", names)
        self.assertIn("session-plan", names)
        self.assertIn("activation-state", names)
        self.assertIn("migration-report", names)

    def test_resolved_profile_shape_contract(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-crt.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        self._assert_required_keys(resolved, RESOLVED_PROFILE_TOP_LEVEL_KEYS)
        self._assert_required_keys(resolved["semantics"], RESOLVED_PROFILE_SEMANTICS_KEYS)
        self._assert_required_keys(resolved["decisions"], RESOLVED_PROFILE_DECISIONS_KEYS)
        self.assertIn("requested_targets", resolved["semantics"]["session"])
        self.assertIn("display", resolved["semantics"]["render"])

    def test_target_compiler_contract_uses_resolved_input_and_deterministic_paths(self) -> None:
        resolved = run_profile_pipeline(FIXTURES / "strict-green-crt.toml").resolved_profile
        assert resolved is not None

        with TemporaryDirectory() as tmpout:
            compiled = compile_resolved_profile_targets(resolved, tmpout, ["xresources"])
            self.assertEqual(compiled["selected_targets"], ["xresources"])
            self.assertTrue(compiled["profile_output_root"].endswith("/strict-green-crt"))
            result = compiled["compiled_targets"][0]
            self._assert_required_keys(result, TARGET_COMPILE_RESULT_KEYS)
            artifact = result["artifacts"][0]
            self._assert_required_keys(artifact, TARGET_ARTIFACT_KEYS)
            self.assertEqual(artifact["relative_path"], "xresources/Xresources")
            self.assertTrue(Path(artifact["output_path"]).is_file())

        with self.assertRaises(KeyError):
            compile_resolved_profile_targets({"schema": "retrofx.profile/v2alpha1"}, REPO_ROOT / "v2" / "out", ["xresources"])

    def test_compile_surface_preserves_target_warning_and_note_shapes(self) -> None:
        with TemporaryDirectory() as tmpout:
            payload = compile_profile_to_output(
                FIXTURES / "warm-night-theme-only.toml",
                out_root=tmpout,
                target_names=["gtk-export", "qt-export"],
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
            for result in payload["compiled_targets"]:
                self._assert_required_keys(result, TARGET_COMPILE_RESULT_KEYS)
                self.assertIsInstance(result["warnings"], list)
                self.assertIsInstance(result["notes"], list)

    def test_session_plan_shape_contract(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-crt.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None

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
            path_lookup=lambda name: "/tmp/fake-picom" if name == "picom" else None,
        )
        plan = build_session_plan(resolved, environment)
        self._assert_required_keys(plan, SESSION_PLAN_KEYS)
        self.assertTrue(plan["target_entries"])
        for entry in plan["target_entries"]:
            self._assert_required_keys(entry, SESSION_PLAN_ENTRY_KEYS)
        self.assertIn("compile_targets", plan)
        self.assertIn("skipped_targets", plan)
        self.assertIsInstance(plan["warnings"], list)

    def test_apply_state_and_manifest_contracts(self) -> None:
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
                now="2026-03-21T11:00:00Z",
            )
            self.assertTrue(payload["ok"])
            current_state = json.loads(Path(payload["activation"]["current_state_path"]).read_text(encoding="utf-8"))
            manifest = json.loads(Path(payload["activation"]["manifest_path"]).read_text(encoding="utf-8"))
            self._assert_required_keys(current_state, CURRENT_STATE_KEYS)
            self._assert_required_keys(manifest, ACTIVATION_MANIFEST_KEYS)
            self.assertEqual(current_state["activation"]["activation_id"], manifest["activation_id"])

            off_payload = off_dev_profile(env=env, now="2026-03-21T11:01:00Z")
            self.assertTrue(off_payload["ok"])
            self.assertFalse(Path(payload["activation"]["current_state_path"]).exists())

    def test_pack_manifest_and_profile_entry_contracts(self) -> None:
        manifest = load_pack_manifest("crt-core")
        self._assert_required_keys(manifest, PACK_MANIFEST_KEYS)
        self.assertTrue(manifest["profiles"])
        for entry in manifest["profiles"]:
            self._assert_required_keys(entry, PACK_PROFILE_ENTRY_KEYS)

    def test_migration_report_contract(self) -> None:
        payload = inspect_legacy_profile(LEGACY_PROFILES / "crt-green-p1-4band.toml")
        self.assertTrue(payload["ok"])
        report = payload["migration_report"]
        self._assert_required_keys(report, MIGRATION_REPORT_KEYS)
        self._assert_required_keys(report["mapping_summary"], MIGRATION_SUMMARY_KEYS)
        self.assertIsInstance(report["mapped_cleanly"], list)
        self.assertIsInstance(report["mapped_with_degradation"], list)
        self.assertIsInstance(report["requires_manual_follow_up"], list)
        self.assertIsInstance(report["unsupported_or_ignored"], list)

    def test_install_record_contract(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                bundle_root=tmpbundle,
                target_names=["xresources"],
            )
            self.assertTrue(bundle["ok"])
            env = self._temp_home_env(tmphome)
            install_payload = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T11:10:00Z")
            self.assertTrue(install_payload["ok"])
            record = install_payload["record"]
            self._assert_required_keys(record, INSTALL_RECORD_KEYS)
            self.assertEqual(record["bundle_id"], "crt-core--green-crt")

    def _assert_required_keys(self, payload: dict[str, object], required_keys: tuple[str, ...]) -> None:
        missing = [key for key in required_keys if key not in payload]
        self.assertEqual(missing, [], msg=f"Missing required keys: {missing}")

    def _temp_home_env(self, home: str) -> dict[str, str]:
        home_path = Path(home)
        return {
            "HOME": str(home_path),
            "XDG_CONFIG_HOME": str(home_path / ".config"),
            "XDG_DATA_HOME": str(home_path / ".local" / "share"),
            "XDG_STATE_HOME": str(home_path / ".local" / "state"),
        }


if __name__ == "__main__":
    unittest.main()
