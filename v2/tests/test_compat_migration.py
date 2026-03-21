"""Tests for the first real 2.x 1.x-compatibility inspection slice."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.compat import inspect_legacy_profile
from v2.core.pipeline import run_profile_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"
LEGACY_PROFILES = REPO_ROOT / "profiles" / "packs" / "core"


class CompatibilityMigrationTests(unittest.TestCase):
    def test_monochrome_profile_inspection_maps_core_fields(self) -> None:
        payload = inspect_legacy_profile(LEGACY_PROFILES / "crt-green-p1-4band.toml")
        self.assertTrue(payload["ok"])
        report = payload["migration_report"]
        self.assertEqual(report["legacy_profile"]["mode"], "monochrome")
        self.assertEqual(report["proposed_identity"]["id"], "crt-green-p1-4band")
        self.assertEqual(report["draft_profile"]["render"]["mode"], "monochrome")
        self.assertEqual(report["draft_profile"]["render"]["quantization"]["bands"], 4)

    def test_palette_profile_inspection_maps_palette_fields(self) -> None:
        payload = inspect_legacy_profile(LEGACY_PROFILES / "ibm-vga16.toml")
        self.assertTrue(payload["ok"])
        draft = payload["migration_report"]["draft_profile"]
        self.assertEqual(draft["render"]["mode"], "palette")
        self.assertEqual(draft["render"]["palette"]["kind"], "vga16")
        self.assertEqual(draft["render"]["palette"]["size"], 16)
        self.assertEqual(payload["migration_report"]["proposed_identity"]["family"], "dos")

    def test_fonts_and_aa_profile_maps_typography(self) -> None:
        payload = inspect_legacy_profile(LEGACY_PROFILES / "crt-green-fonts-aa.toml")
        self.assertTrue(payload["ok"])
        typography = payload["migration_report"]["draft_profile"]["typography"]
        self.assertEqual(typography["console_font"], "ter-v16n")
        self.assertEqual(typography["terminal_primary"], "Terminus Nerd Font")
        self.assertEqual(typography["terminal_fallbacks"], ["DejaVu Sans Mono", "Noto Color Emoji"])
        self.assertEqual(typography["aa"]["antialias"], "off")
        self.assertEqual(typography["aa"]["subpixel"], "none")

    def test_unsupported_and_lossy_fields_are_reported(self) -> None:
        payload = inspect_legacy_profile(FIXTURES / "legacy-1x-colors-rules.toml")
        self.assertTrue(payload["ok"])
        report = payload["migration_report"]
        self.assertIn("rules.window_opacity", [entry["legacy_field"] for entry in report["unsupported_or_ignored"]])
        self.assertIn("effects.transparency", [entry["legacy_field"] for entry in report["requires_manual_follow_up"]])
        self.assertGreaterEqual(report["mapping_summary"]["mapped_with_degradation"], 1)
        self.assertEqual(report["draft_profile"]["color"]["semantic"]["bg0"], "#081018")
        self.assertEqual(report["draft_profile"]["color"]["semantic"]["fg0"], "#dff3ff")

    def test_migration_output_is_deterministic(self) -> None:
        payload_a = inspect_legacy_profile(LEGACY_PROFILES / "vfd-505-8band.toml")
        payload_b = inspect_legacy_profile(LEGACY_PROFILES / "vfd-505-8band.toml")
        self.assertEqual(
            json.dumps(payload_a["migration_report"], sort_keys=True),
            json.dumps(payload_b["migration_report"], sort_keys=True),
        )

    def test_malformed_legacy_profile_fails_cleanly(self) -> None:
        payload = inspect_legacy_profile(FIXTURES / "invalid-legacy-1x-profile.toml")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["stage"], "legacy-load")
        self.assertEqual(payload["errors"][0]["code"], "missing-legacy-table")

    def test_draft_profile_is_emitted_and_validates(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = inspect_legacy_profile(
                LEGACY_PROFILES / "c64.toml",
                out_root=tmpdir,
                write_draft=True,
            )
            self.assertTrue(payload["ok"])
            emitted = payload["emitted_bundle"]
            assert emitted is not None
            draft_path = Path(emitted["output_dir"]) / "draft-profile.toml"
            self.assertTrue(draft_path.is_file())
            self.assertTrue((Path(emitted["output_dir"]) / "migration-report.json").is_file())
            draft_pipeline = run_profile_pipeline(draft_path)
            self.assertTrue(draft_pipeline.ok)
            draft_content = draft_path.read_text(encoding="utf-8")
            self.assertIn('schema = "retrofx.profile/v2alpha1"', draft_content)
            self.assertIn("[render.palette]", draft_content)
            self.assertIn("[session]", draft_content)

    def test_dev_entrypoint_emits_json(self) -> None:
        with TemporaryDirectory() as tmpdir:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.compat.dev.inspect_1x_profile",
                    str(LEGACY_PROFILES / "crt-green-p1-4band.toml"),
                    "--out-root",
                    tmpdir,
                    "--write-draft",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stage"], "migration-inspection")
            self.assertIsNotNone(payload["emitted_bundle"])


if __name__ == "__main__":
    unittest.main()
