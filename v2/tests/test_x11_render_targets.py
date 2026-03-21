"""Tests for the first real 2.x X11 render/compiler slice."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from v2.core.dev.compile_targets import compile_profile_to_output
from v2.core.dev.plan_session import plan_profile_session
from v2.session.dev.preview_x11_render import preview_x11_render_profile

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "v2" / "tests" / "fixtures"


def _simulated_path_lookup(name: str) -> str | None:
    available = {
        "picom": "/usr/bin/picom",
        "xrdb": "/usr/bin/xrdb",
        "i3-msg": "/usr/bin/i3-msg",
    }
    return available.get(name)


def _fake_probe_runner(*_args, **_kwargs):
    class Result:
        returncode = 0
        stderr = ""
        stdout = "picom probe ok"

    return Result()


class X11RenderTargetTests(unittest.TestCase):
    def test_shader_and_picom_are_emitted_for_valid_crt_profile(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "strict-green-crt.toml",
                out_root=tmpdir,
                target_names=["x11-shader", "x11-picom", "x11-render-runtime"],
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "XDG_CURRENT_DESKTOP": "i3",
                    "I3SOCK": "/tmp/i3.sock",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            self.assertTrue(payload["ok"])
            output_root = Path(payload["profile_output_root"])
            self.assertTrue((output_root / "x11-shader" / "shader.glsl").is_file())
            self.assertTrue((output_root / "x11-picom" / "picom.conf").is_file())
            self.assertTrue((output_root / "x11-render-runtime" / "runtime-metadata.json").is_file())

    def test_passthrough_profile_emits_expected_minimal_shader(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "passthrough-minimal.toml",
                out_root=tmpdir,
                target_names=["x11-shader", "x11-picom"],
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            self.assertTrue(payload["ok"])
            shader = (Path(payload["profile_output_root"]) / "x11-shader" / "shader.glsl").read_text(encoding="utf-8")
            picom = (Path(payload["profile_output_root"]) / "x11-picom" / "picom.conf").read_text(encoding="utf-8")
            self.assertIn("#define RX_MODE_PASSTHROUGH 1", shader)
            self.assertIn("window_shader()", shader)
            self.assertIn('window-shader-fg = "../x11-shader/shader.glsl";', picom)

    def test_monochrome_profile_emits_expected_shader_structure(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "strict-green-crt.toml",
                out_root=tmpdir,
                target_names=["x11-shader"],
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            self.assertTrue(payload["ok"])
            shader = (Path(payload["profile_output_root"]) / "x11-shader" / "shader.glsl").read_text(encoding="utf-8")
            self.assertIn("#define RX_MODE_MONOCHROME 1", shader)
            self.assertIn("const int RX_MONO_BANDS = 4;", shader)
            self.assertIn("#define RX_ENABLE_SCANLINES 1", shader)
            self.assertIn("#define RX_ENABLE_DITHER 1", shader)

    def test_palette_profile_emits_expected_shader_structure(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "vga-like-palette.toml",
                out_root=tmpdir,
                target_names=["x11-shader", "x11-picom"],
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            self.assertTrue(payload["ok"])
            shader = (Path(payload["profile_output_root"]) / "x11-shader" / "shader.glsl").read_text(encoding="utf-8")
            self.assertIn("#define RX_MODE_PALETTE 1", shader)
            self.assertIn("#define RX_PALETTE_KIND_VGA16 1", shader)
            self.assertIn("vec3 vga16_linear(int idx)", shader)

    def test_invalid_render_policy_fails_validation_earlier(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = compile_profile_to_output(
                FIXTURES / "invalid-render-policy.toml",
                out_root=tmpdir,
                target_names=["x11-shader"],
            )
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["stage"], "validation")

    def test_x11_render_artifacts_are_deterministic(self) -> None:
        env = {
            "DISPLAY": ":1",
            "XDG_SESSION_TYPE": "x11",
            "XDG_CURRENT_DESKTOP": "i3",
            "I3SOCK": "/tmp/i3.sock",
            "TERM": "xterm-256color",
        }
        with TemporaryDirectory() as tmpdir_a, TemporaryDirectory() as tmpdir_b:
            payload_a = compile_profile_to_output(
                FIXTURES / "vga-like-palette.toml",
                out_root=tmpdir_a,
                target_names=["x11-shader", "x11-picom", "x11-render-runtime"],
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            payload_b = compile_profile_to_output(
                FIXTURES / "vga-like-palette.toml",
                out_root=tmpdir_b,
                target_names=["x11-shader", "x11-picom", "x11-render-runtime"],
                env=env,
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
            )
            self.assertEqual(
                [
                    [artifact["content_sha256"] for artifact in target["artifacts"]]
                    for target in payload_a["compiled_targets"]
                ],
                [
                    [artifact["content_sha256"] for artifact in target["artifacts"]]
                    for target in payload_b["compiled_targets"]
                ],
            )

    def test_plan_differs_between_x11_and_wayland_for_x11_render(self) -> None:
        x11_payload = plan_profile_session(
            FIXTURES / "strict-green-crt.toml",
            env={
                "DISPLAY": ":1",
                "XDG_SESSION_TYPE": "x11",
                "XDG_CURRENT_DESKTOP": "i3",
                "I3SOCK": "/tmp/i3.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
            path_lookup=_simulated_path_lookup,
        )
        wayland_payload = plan_profile_session(
            FIXTURES / "strict-green-crt.toml",
            env={
                "WAYLAND_DISPLAY": "wayland-0",
                "XDG_SESSION_TYPE": "wayland",
                "XDG_CURRENT_DESKTOP": "sway",
                "SWAYSOCK": "/tmp/sway.sock",
                "TERM": "xterm-256color",
            },
            cwd=REPO_ROOT,
            stdin_isatty=False,
            path_lookup=_simulated_path_lookup,
        )
        self.assertEqual(x11_payload["plan"]["x11_render"]["overall_status"], "x11-live-preview-available")
        self.assertEqual(wayland_payload["plan"]["x11_render"]["overall_status"], "export-only-non-x11")
        self.assertIn("x11-picom", x11_payload["plan"]["apply_preview_targets"])
        self.assertIn("x11-shader", wayland_payload["plan"]["degraded_targets"])

    def test_preview_command_writes_preview_state(self) -> None:
        with TemporaryDirectory() as tmpdir:
            payload = preview_x11_render_profile(
                FIXTURES / "strict-green-crt.toml",
                out_root=tmpdir,
                env={
                    "DISPLAY": ":1",
                    "XDG_SESSION_TYPE": "x11",
                    "XDG_CURRENT_DESKTOP": "i3",
                    "I3SOCK": "/tmp/i3.sock",
                    "TERM": "xterm-256color",
                },
                cwd=REPO_ROOT,
                stdin_isatty=False,
                path_lookup=_simulated_path_lookup,
                probe_picom=True,
                command_runner=_fake_probe_runner,
            )
            self.assertTrue(payload["ok"])
            preview_state = Path(payload["preview"]["preview_state_path"])
            self.assertTrue(preview_state.is_file())
            state_payload = json.loads(preview_state.read_text(encoding="utf-8"))
            self.assertEqual(state_payload["render"]["overall_status"], "x11-live-preview-available")
            self.assertEqual(state_payload["probe"]["status"], "ok")

    def test_dev_preview_entrypoint_emits_json(self) -> None:
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
                    "v2.session.dev.preview_x11_render",
                    str(FIXTURES / "strict-green-crt.toml"),
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
            self.assertEqual(payload["stage"], "x11-render-preview")


if __name__ == "__main__":
    unittest.main()
