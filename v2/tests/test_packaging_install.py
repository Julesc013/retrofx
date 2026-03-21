"""Tests for the experimental RetroFX 2.x bundle and user-local install flow."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.session.install import build_dev_bundle, describe_install_state, install_dev_bundle, load_bundle_manifest, uninstall_dev_bundle

REPO_ROOT = Path(__file__).resolve().parents[2]


class PackagingInstallTests(unittest.TestCase):
    def test_repo_local_bundle_generation(self) -> None:
        with TemporaryDirectory() as tmpbundle:
            payload = build_dev_bundle(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                bundle_root=tmpbundle,
                target_names=["xresources", "alacritty"],
            )
            self.assertTrue(payload["ok"])
            bundle_dir = Path(payload["bundle"]["output_dir"])
            self.assertTrue((bundle_dir / "targets" / "xresources" / "Xresources").is_file())
            self.assertTrue((bundle_dir / "targets" / "alacritty" / "alacritty.toml").is_file())

    def test_bundle_manifest_generation(self) -> None:
        with TemporaryDirectory() as tmpbundle:
            payload = build_dev_bundle(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                bundle_root=tmpbundle,
                target_names=["alacritty", "fontconfig"],
            )
            self.assertTrue(payload["ok"])
            manifest = load_bundle_manifest(payload["bundle"]["output_dir"])
            self.assertEqual(manifest["schema"], "retrofx.bundle/v2alpha1")
            self.assertEqual(manifest["bundle_id"], "modern-minimal--warm-night")
            self.assertEqual(manifest["install_name"], "retrofx-v2-dev")
            self.assertEqual(manifest["experimental_release"]["status_label"], "internal-alpha")
            self.assertEqual([target["target_name"] for target in manifest["compiled_targets"]], ["alacritty", "fontconfig"])

    def test_experimental_install_into_temp_home(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                bundle_root=tmpbundle,
                target_names=["xresources"],
            )
            self.assertTrue(bundle["ok"])
            env = self._temp_home_env(tmphome)
            payload = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            self.assertTrue(payload["ok"])
            installed_bundle_dir = Path(payload["install"]["bundle_dir"])
            self.assertTrue((installed_bundle_dir / "manifest.json").is_file())
            self.assertTrue((installed_bundle_dir / "targets" / "xresources" / "Xresources").is_file())

    def test_status_reporting_for_installed_dev_mode(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                bundle_root=tmpbundle,
                target_names=["xresources"],
            )
            env = self._temp_home_env(tmphome)
            install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            status = describe_install_state(env=env, cwd=REPO_ROOT)
            self.assertTrue(status["ok"])
            self.assertEqual(status["toolchain_mode"], "repo-local-dev")
            self.assertEqual(len(status["installed_bundles"]), 1)
            self.assertEqual(status["installed_bundles"][0]["bundle_id"], "crt-core--green-crt")
            self.assertEqual(status["installed_bundles"][0]["release_status"], "internal-alpha")

    def test_uninstall_cleanup_in_temp_home(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                bundle_root=tmpbundle,
                target_names=["alacritty"],
            )
            env = self._temp_home_env(tmphome)
            install_payload = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            installed_bundle_dir = Path(install_payload["install"]["bundle_dir"])
            uninstall_payload = uninstall_dev_bundle("modern-minimal--warm-night", env=env)
            self.assertTrue(uninstall_payload["ok"])
            self.assertFalse(installed_bundle_dir.exists())
            status = describe_install_state(env=env, cwd=REPO_ROOT)
            self.assertEqual(status["installed_bundles"], [])

    def test_uninstall_refuses_bundle_dir_outside_managed_root(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="modern-minimal",
                pack_profile_id="warm-night",
                bundle_root=tmpbundle,
                target_names=["alacritty"],
            )
            env = self._temp_home_env(tmphome)
            install_payload = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            foreign_dir = Path(tmphome) / "foreign-bundle-dir"
            foreign_dir.mkdir(parents=True, exist_ok=True)
            foreign_marker = foreign_dir / "keep.txt"
            foreign_marker.write_text("keep me", encoding="utf-8")
            record_path = Path(install_payload["install"]["record_path"])
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["install_targets"]["bundle_dir"] = str(foreign_dir)
            record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

            uninstall_payload = uninstall_dev_bundle("modern-minimal--warm-night", env=env)
            self.assertFalse(uninstall_payload["ok"])
            self.assertTrue(foreign_marker.exists())
            self.assertEqual(uninstall_payload["errors"][0]["code"], "unowned-install-target")

    def test_install_paths_do_not_collide_with_1x(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            status = describe_install_state(env=env, cwd=REPO_ROOT)
            layout = status["install_layout"]
            self.assertTrue(layout["config_root"].endswith("retrofx-v2-dev"))
            self.assertTrue(layout["data_root"].endswith("retrofx-v2-dev"))
            self.assertTrue(layout["state_root"].endswith("retrofx-v2-dev"))
            self.assertNotEqual(layout["config_root"], str(Path(tmphome) / ".config" / "retrofx"))
            self.assertNotEqual(layout["launcher_path"], str(Path(tmphome) / ".local" / "bin" / "retrofx"))

    def test_install_state_metadata_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmpbundle, TemporaryDirectory() as tmphome:
            bundle = build_dev_bundle(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                bundle_root=tmpbundle,
                target_names=["xresources"],
            )
            env = self._temp_home_env(tmphome)
            install_payload_a = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            record_path = Path(install_payload_a["install"]["record_path"])
            record_a = record_path.read_text(encoding="utf-8")
            uninstall_dev_bundle("crt-core--green-crt", env=env)
            install_payload_b = install_dev_bundle(bundle["bundle"]["output_dir"], env=env, now="2026-03-21T00:00:00Z")
            record_b = Path(install_payload_b["install"]["record_path"]).read_text(encoding="utf-8")
            self.assertEqual(record_a, record_b)

    def test_dev_cli_status_emits_json(self) -> None:
        with TemporaryDirectory() as tmphome:
            env = self._temp_home_env(tmphome)
            env.update(
                {
                    "PYTHONPATH": str(REPO_ROOT),
                    "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                }
            )
            process = subprocess.run(
                [sys.executable, "-m", "v2.session.install.cli", "status"],
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


if __name__ == "__main__":
    unittest.main()
