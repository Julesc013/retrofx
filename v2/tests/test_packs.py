"""Tests for the first real 2.x local pack system."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.compile_targets import compile_profile_to_output
from v2.core.dev.plan_session import plan_profile_session
from v2.core.pipeline import run_pack_profile_pipeline
from v2.packs import PackLoadError, discover_packs, load_pack_manifest, load_pack_profile_document

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class PackSystemTests(unittest.TestCase):
    def test_pack_manifest_parses_successfully(self) -> None:
        manifest = load_pack_manifest("crt-core")
        self.assertEqual(manifest["id"], "crt-core")
        self.assertEqual(manifest["family"], "crt")
        self.assertIn("preview", manifest["assets"])
        self.assertIn("green-crt", [profile["id"] for profile in manifest["profiles"]])

    def test_curated_builtin_packs_are_discoverable(self) -> None:
        packs = discover_packs()
        pack_ids = [pack["id"] for pack in packs]
        self.assertIn("crt-core", pack_ids)
        self.assertIn("terminal-classic", pack_ids)
        self.assertIn("modern-minimal", pack_ids)

    def test_pack_profile_discovery_and_resolution_work(self) -> None:
        raw_profile = load_pack_profile_document("modern-minimal", "warm-night")
        self.assertEqual(raw_profile.origin["type"], "pack")
        self.assertEqual(raw_profile.origin["pack"]["id"], "modern-minimal")

        result = run_pack_profile_pipeline("modern-minimal", "warm-night")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        self.assertEqual(resolved["identity"]["id"], "warm-night")
        self.assertEqual(resolved["pack"]["id"], "modern-minimal")

    def test_malformed_pack_manifest_fails_cleanly(self) -> None:
        with TemporaryDirectory() as tmpdir:
            packs_root = Path(tmpdir)
            broken_pack = packs_root / "broken-pack"
            broken_pack.mkdir()
            (broken_pack / "pack.toml").write_text(
                (FIXTURES / "invalid-pack-manifest.toml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            with self.assertRaises(PackLoadError) as context:
                load_pack_manifest("broken-pack", packs_root=packs_root)

            self.assertEqual(context.exception.issue.code, "missing-pack-profiles")

    def test_pack_aware_compile_output_includes_pack_metadata(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                pack_id="crt-core",
                pack_profile_id="green-crt",
                out_root=tmpdir,
                target_names=["xresources"],
            )
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["pack"]["id"], "crt-core")
            self.assertEqual(payload["profile_origin"]["type"], "pack")
            output_file = Path(payload["profile_output_root"]) / "xresources" / "Xresources"
            self.assertTrue(output_file.is_file())

    def test_pack_aware_plan_output_includes_expected_metadata(self) -> None:
        payload = plan_profile_session(
            pack_id="modern-minimal",
            pack_profile_id="warm-night",
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
        self.assertEqual(payload["profile"]["origin"]["type"], "pack")
        self.assertEqual(payload["profile"]["pack"]["id"], "modern-minimal")
        self.assertIn("wm", payload["plan"]["requested_targets"])

    def test_pack_resolution_is_deterministic(self) -> None:
        payload_a = run_pack_profile_pipeline("crt-core", "amber-crt")
        payload_b = run_pack_profile_pipeline("crt-core", "amber-crt")
        self.assertTrue(payload_a.ok)
        self.assertTrue(payload_b.ok)
        self.assertEqual(
            json.dumps(payload_a.resolved_profile, sort_keys=True),
            json.dumps(payload_b.resolved_profile, sort_keys=True),
        )

    def test_dev_pack_entrypoints_emit_json(self) -> None:
        process = subprocess.run(
            [sys.executable, "-m", "v2.core.dev.list_packs"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        payload = json.loads(process.stdout)
        self.assertTrue(payload["ok"])
        self.assertIn("crt-core", [pack["id"] for pack in payload["packs"]])

        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "v2.core.dev.resolve_profile",
                "--pack",
                "crt-core",
                "--profile-id",
                "green-crt",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        resolved_payload = json.loads(process.stdout)
        self.assertTrue(resolved_payload["ok"])
        self.assertEqual(resolved_payload["source"]["origin"]["type"], "pack")


if __name__ == "__main__":
    unittest.main()
