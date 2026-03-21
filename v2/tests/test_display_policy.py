"""Tests for the first real 2.x display-policy slice."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.compile_targets import compile_profile_to_output
from v2.core.dev.plan_session import plan_profile_session
from v2.core.pipeline import run_profile_pipeline

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


class DisplayPolicyTests(unittest.TestCase):
    def test_explicit_display_policy_resolves_correctly(self) -> None:
        result = run_profile_pipeline(FIXTURES / "strict-green-display-policy.toml")
        self.assertTrue(result.ok)
        resolved = result.resolved_profile
        assert resolved is not None
        display = resolved["semantics"]["render"]["display"]
        self.assertEqual(display["gamma"], 1.08)
        self.assertEqual(display["contrast"], 1.14)
        self.assertEqual(display["temperature"], 5900)
        self.assertEqual(display["black_lift"], 0.03)
        self.assertEqual(display["blue_light_reduction"], 0.18)
        self.assertEqual(display["tint_bias"], "#7dff70")

    def test_display_defaults_are_filled_when_omitted(self) -> None:
        result = run_profile_pipeline(FIXTURES / "vga-like-palette.toml")
        self.assertTrue(result.ok)
        normalized = result.normalized_profile
        assert normalized is not None
        display = normalized["render"]["display"]
        self.assertEqual(display["gamma"], 1.0)
        self.assertEqual(display["contrast"], 1.0)
        self.assertEqual(display["temperature"], 6500)
        self.assertEqual(display["black_lift"], 0.0)
        self.assertEqual(display["blue_light_reduction"], 0.0)
        self.assertIsNone(display["tint_bias"])

    def test_invalid_display_policy_fails_validation(self) -> None:
        result = run_profile_pipeline(FIXTURES / "invalid-display-policy.toml")
        self.assertFalse(result.ok)
        self.assertEqual(result.stage, "validation")
        codes = {error.code for error in result.errors}
        self.assertIn("invalid-number-range", codes)
        self.assertIn("invalid-tint-bias", codes)

    def test_display_policy_compiler_emits_artifacts(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "strict-green-display-policy.toml",
                out_root=tmpdir,
                target_names=["x11-display-policy"],
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "XDG_CURRENT_DESKTOP": "i3",
                    "I3SOCK": "/tmp/i3.sock",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
            )
            self.assertTrue(payload["ok"])
            output_dir = Path(payload["profile_output_root"]) / "x11-display-policy"
            self.assertTrue((output_dir / "display-policy.json").is_file())
            self.assertTrue((output_dir / "x11-render-policy.env").is_file())

    def test_display_policy_artifacts_are_deterministic(self) -> None:
        env = {
            "DISPLAY": ":1",
            "XDG_SESSION_TYPE": "x11",
            "XDG_CURRENT_DESKTOP": "i3",
            "I3SOCK": "/tmp/i3.sock",
            "TERM": "xterm-256color",
        }
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "strict-green-display-policy.toml",
                out_root=tmpdir_a,
                target_names=["x11-display-policy"],
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "strict-green-display-policy.toml",
                out_root=tmpdir_b,
                target_names=["x11-display-policy"],
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
            )
            self.assertTrue(payload_a["ok"])
            self.assertTrue(payload_b["ok"])
            self.assertEqual(
                [artifact["content_sha256"] for artifact in payload_a["compiled_targets"][0]["artifacts"]],
                [artifact["content_sha256"] for artifact in payload_b["compiled_targets"][0]["artifacts"]],
            )

    def test_plan_output_includes_display_policy(self) -> None:
        payload = plan_profile_session(
            FIXTURES / "strict-green-display-policy.toml",
            env={
                "DISPLAY": ":1",
                "XDG_SESSION_TYPE": "x11",
                "XDG_CURRENT_DESKTOP": "i3",
                "I3SOCK": "/tmp/i3.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        self.assertTrue(payload["ok"])
        self.assertIn("display_policy", payload["profile"])
        self.assertEqual(payload["plan"]["display_policy"]["overall_status"], "future-render-consumer")

    def test_x11_and_wayland_display_policy_interpretations_differ(self) -> None:
        x11_payload = plan_profile_session(
            FIXTURES / "strict-green-display-policy.toml",
            env={
                "DISPLAY": ":1",
                "XDG_SESSION_TYPE": "x11",
                "XDG_CURRENT_DESKTOP": "i3",
                "I3SOCK": "/tmp/i3.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
        )
        wayland_payload = plan_profile_session(
            FIXTURES / "warm-night-display-policy.toml",
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
        self.assertEqual(x11_payload["plan"]["display_policy"]["overall_status"], "future-render-consumer")
        self.assertEqual(wayland_payload["plan"]["display_policy"]["overall_status"], "advisory-export-only")

    def test_dev_compile_entrypoint_emits_display_policy_json(self) -> None:
        with TemporaryDirectory() as tmpdir:
            env = dict(
                DISPLAY=":1",
                XDG_SESSION_TYPE="x11",
                XDG_CURRENT_DESKTOP="i3",
                I3SOCK="/tmp/i3.sock",
                TERM="xterm-256color",
                PYTHONPATH=str(REPO_ROOT),
                PATH=str(Path("/usr/bin")) + ":" + str(Path("/bin")),
            )
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "v2.core.dev.compile_targets",
                    str(FIXTURES / "strict-green-display-policy.toml"),
                    "--target",
                    "x11-display-policy",
                    "--out-root",
                    tmpdir,
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["display_policy"]["overall_status"], "future-render-consumer")


if __name__ == "__main__":
    unittest.main()
