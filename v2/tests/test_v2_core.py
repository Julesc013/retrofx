"""Tests for the initial 2.x core scaffold."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from v2.core.pipeline import run_profile_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class V2CorePipelineTests(unittest.TestCase):
    def test_crt_profile_resolves_successfully(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-crt.toml")
        self.assertTrue(result.ok)
        self.assertEqual(result.stage, "resolution")
        resolved = result.resolved_profile
        assert resolved is not None
        self.assertEqual(resolved["identity"]["id"], "strict-green-crt")
        self.assertEqual(resolved["semantics"]["render"]["mode"], "monochrome")

    def test_palette_profile_resolves_successfully(self) -> None:
        result = run_profile_pipeline(FIXTURES / "vga-like-palette.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        self.assertEqual(resolved["semantics"]["render"]["mode"], "palette")
        self.assertEqual(resolved["semantics"]["render"]["palette"]["kind"], "vga16")
        self.assertEqual(resolved["semantics"]["render"]["palette"]["size"], 16)

    def test_theme_only_profile_resolves_successfully(self) -> None:
        result = run_profile_pipeline(FIXTURES / "warm-night-theme-only.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        self.assertEqual(resolved["semantics"]["render"]["mode"], "passthrough")
        self.assertEqual(resolved["semantics"]["session"]["apply_mode"], "current-session")

    def test_malformed_profile_fails_validation(self) -> None:
        result = run_profile_pipeline(FIXTURES / "malformed-profile.toml")
        self.assertFalse(result.ok)
        self.assertEqual(result.stage, "validation")
        codes = {error.code for error in result.errors}
        self.assertIn("missing-custom-palette-source", codes)
        self.assertIn("missing-session-targets", codes)

    def test_invalid_color_profile_fails_validation(self) -> None:
        result = run_profile_pipeline(FIXTURES / "invalid-color-profile.toml")
        self.assertFalse(result.ok)
        self.assertEqual(result.stage, "validation")
        codes = {error.code for error in result.errors}
        self.assertIn("invalid-color", codes)

    def test_normalization_fills_expected_defaults(self) -> None:
        result = run_profile_pipeline(FIXTURES / "warm-night-theme-only.toml")
        self.assertTrue(result.ok)
        normalized = result.normalized_profile
        assert normalized is not None
        self.assertEqual(normalized["render"]["mode"], "passthrough")
        self.assertEqual(normalized["session"]["persistence"], "ephemeral")
        self.assertIn("bg1", normalized["color"]["semantic"])
        self.assertEqual(len(normalized["color"]["terminal"]["ansi"]), 16)
        self.assertEqual(len(normalized["color"]["tty"]["ansi"]), 16)

    def test_resolved_profile_contains_expected_sections(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-crt.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        for key in (
            "identity",
            "semantics",
            "target_requests",
            "capability_context",
            "target_plan",
            "artifact_plan",
            "decisions",
        ):
            self.assertIn(key, resolved)

    def test_dev_entrypoint_emits_json(self) -> None:
        process = subprocess.run(
            [sys.executable, "-m", "v2.core.dev.resolve_profile", str(FIXTURES / "strict-green-crt.toml")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(process.returncode, 0, msg=process.stderr)
        payload = json.loads(process.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["stage"], "resolution")


if __name__ == "__main__":
    unittest.main()
