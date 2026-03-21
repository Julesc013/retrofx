"""Experimental GLSL shader compiler for the first 2.x X11 render slice."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.common import write_target_artifact
from v2.targets.interfaces import TargetCompileResult
from v2.targets.x11.common import build_x11_render_context, build_x11_warnings, display_tint_triplet, glsl_vec3


class X11ShaderCompiler:
    target_name = "x11-shader"
    family_name = "x11"
    output_file_name = "shader.glsl"
    supported_target_classes = ("x11", "wm")

    def compile(
        self,
        resolved_profile: Mapping[str, Any],
        profile_output_root: Path,
        compile_context: Mapping[str, Any] | None = None,
    ) -> TargetCompileResult:
        context_map = dict(compile_context or {})
        environment = dict(context_map.get("environment", {}))
        display_policy = context_map.get("display_policy")
        x11_render = context_map.get("x11_render")
        context = build_x11_render_context(
            resolved_profile,
            environment=environment,
            display_policy=display_policy,
            x11_render=x11_render,
        )
        output_dir = profile_output_root / self.target_name
        artifact = write_target_artifact(
            target_name=self.target_name,
            output_dir=output_dir,
            file_name=self.output_file_name,
            content=self._render(context),
        )
        warnings = build_x11_warnings(context, self.supported_target_classes)
        if context.implemented_mode == "passthrough" and context.render_mode == "palette":
            warnings.append("Palette render intent degraded to passthrough for this first 2.x X11 shader slice.")

        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=[artifact],
            consumed_sections=[
                "identity",
                "semantics.color.semantic",
                "semantics.color.terminal_ansi",
                "semantics.render.mode",
                "semantics.render.quantization",
                "semantics.render.palette",
                "semantics.render.effects",
                "semantics.render.display",
                "semantics.session",
            ],
            ignored_sections=[
                "semantics.typography",
                "semantics.chrome",
            ],
            warnings=warnings,
            notes=[
                "Deterministic GLSL 1.10-compatible shader body for the bounded TWO-17 X11 render subset.",
                "Implemented now: passthrough, monochrome bands, vga16 palette, plus bounded dither/scanlines/flicker/vignette/hotcore handling.",
            ],
        )

    def _render(self, context) -> str:
        display = context.display
        tint_triplet, tint_strength = display_tint_triplet(display)
        color_lines = [f"    if (idx <= 0) return {glsl_vec3(context.terminal_ansi['0'])};"]
        for slot in range(1, 15):
            color_lines.append(f"    if (idx == {slot}) return {glsl_vec3(context.terminal_ansi[str(slot)])};")
        color_lines.append(f"    return {glsl_vec3(context.terminal_ansi['15'])};")
        palette_body = "\n".join(color_lines)

        monochrome = 1 if context.implemented_mode == "monochrome" else 0
        passthrough = 1 if context.implemented_mode == "passthrough" else 0
        palette = 1 if context.implemented_mode == "palette" else 0
        dither = 1 if context.effects.get("dither") == "ordered" and context.implemented_mode in {"monochrome", "palette"} else 0
        scanlines = 1 if context.effects.get("scanlines") else 0
        flicker = 1 if context.effects.get("flicker") else 0
        vignette = 1 if context.effects.get("vignette") else 0
        hotcore = 1 if context.effects.get("hotcore") and context.implemented_mode == "monochrome" else 0
        palette_vga16 = 1 if context.implemented_mode == "palette" and context.palette_kind == "vga16" else 0

        shader = f"""/*
 * RetroFX 2.x experimental X11 render shader
 * profile.id: {context.profile_id}
 * profile.name: {context.profile_name}
 *
 * Supported in TWO-17:
 *   - passthrough
 *   - monochrome with quantization bands
 *   - palette/vga16
 *   - blur (via picom config), ordered dither, scanlines, flicker, vignette, hotcore
 */

#define RX_MODE_PASSTHROUGH {passthrough}
#define RX_MODE_MONOCHROME {monochrome}
#define RX_MODE_PALETTE {palette}
#define RX_PALETTE_KIND_VGA16 {palette_vga16}
#define RX_ENABLE_DITHER {dither}
#define RX_ENABLE_SCANLINES {scanlines}
#define RX_ENABLE_FLICKER {flicker}
#define RX_ENABLE_VIGNETTE {vignette}
#define RX_ENABLE_HOTCORE {hotcore}

const int RX_MONO_BANDS = {context.monochrome_bands};
const float RX_DISPLAY_GAMMA = {float(display.get("gamma", 1.0)):.6f};
const float RX_DISPLAY_CONTRAST = {float(display.get("contrast", 1.0)):.6f};
const float RX_BLACK_LIFT = {float(display.get("black_lift", 0.0)):.6f};
const float RX_BLUE_LIGHT_REDUCTION = {float(display.get("blue_light_reduction", 0.0)):.6f};
const float RX_TINT_STRENGTH = {tint_strength:.6f};
const vec3 RX_BACKGROUND_LINEAR = {glsl_vec3(context.background)};
const vec3 RX_FOREGROUND_LINEAR = {glsl_vec3(context.foreground)};
const vec3 RX_GLOW_LINEAR = {glsl_vec3(context.glow_tint)};
const vec3 RX_TINT_RGB = vec3({tint_triplet[0]:.6f}, {tint_triplet[1]:.6f}, {tint_triplet[2]:.6f});

#if __VERSION__ >= 130
#define RX_IN in
#else
#define RX_IN varying
#endif

RX_IN vec2 texcoord;
uniform sampler2D tex;
uniform vec2 effective_size;
uniform float time;
vec4 default_post_processing(vec4 c);

float rx_clamp01(float value) {{
    return clamp(value, 0.0, 1.0);
}}

vec3 srgb_to_linear(vec3 color) {{
    return pow(max(color, vec3(0.0)), vec3(2.2));
}}

vec3 linear_to_srgb(vec3 color) {{
    return pow(max(color, vec3(0.0)), vec3(1.0 / 2.2));
}}

float luminance(vec3 color) {{
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}}

float bayer4(vec2 p) {{
    int x = int(mod(p.x, 4.0));
    int y = int(mod(p.y, 4.0));
    if (y == 0) {{
        if (x == 0) return 0.0;
        if (x == 1) return 8.0;
        if (x == 2) return 2.0;
        return 10.0;
    }}
    if (y == 1) {{
        if (x == 0) return 12.0;
        if (x == 1) return 4.0;
        if (x == 2) return 14.0;
        return 6.0;
    }}
    if (y == 2) {{
        if (x == 0) return 3.0;
        if (x == 1) return 11.0;
        if (x == 2) return 1.0;
        return 9.0;
    }}
    if (x == 0) return 15.0;
    if (x == 1) return 7.0;
    if (x == 2) return 13.0;
    return 5.0;
}}

vec3 apply_display_policy(vec3 color) {{
    color = pow(clamp(color, 0.0, 1.0), vec3(1.0 / max(RX_DISPLAY_GAMMA, 0.001)));
    color = ((color - 0.5) * RX_DISPLAY_CONTRAST) + 0.5;
    color = color + vec3(RX_BLACK_LIFT);
    color = mix(color, color * RX_TINT_RGB, RX_TINT_STRENGTH);
    return clamp(color, 0.0, 1.0);
}}

vec3 vga16_linear(int idx) {{
{palette_body}
}}

vec3 quantize_vga16(vec3 color) {{
    vec3 best = vga16_linear(0);
    float best_distance = 1e9;
    int i;
    for (i = 0; i < 16; i++) {{
        vec3 candidate = vga16_linear(i);
        float distance_sq = dot(color - candidate, color - candidate);
        if (distance_sq < best_distance) {{
            best_distance = distance_sq;
            best = candidate;
        }}
    }}
    return best;
}}

vec3 render_monochrome(vec3 color) {{
    float bands = float(max(RX_MONO_BANDS - 1, 1));
    float lum = floor(rx_clamp01(luminance(color)) * bands + 0.5) / bands;
    vec3 mono = mix(RX_BACKGROUND_LINEAR, RX_FOREGROUND_LINEAR, lum);
#if RX_ENABLE_HOTCORE == 1
    mono = mix(mono, RX_GLOW_LINEAR, lum * lum * 0.28);
#endif
    return mono;
}}

vec3 render_palette(vec3 color) {{
#if RX_PALETTE_KIND_VGA16 == 1
    return quantize_vga16(color);
#else
    return color;
#endif
}}

vec3 apply_ordered_dither(vec3 color, vec2 position) {{
    float offset = (bayer4(position) / 15.0) - 0.5;
    return clamp(color + vec3(offset * 0.025), 0.0, 1.0);
}}

vec3 apply_scanlines(vec3 color, vec2 position) {{
    float row = mod(position.y, 2.0);
    float strength = mix(0.84, 1.0, row);
    return color * strength;
}}

vec3 apply_flicker(vec3 color, float clock_time) {{
    float flicker = 0.985 + (sin(clock_time * 80.0) * 0.015);
    return clamp(color * flicker, 0.0, 1.0);
}}

vec3 apply_vignette(vec3 color, vec2 uv) {{
    float distance_from_center = distance(uv, vec2(0.5, 0.5));
    float vignette = smoothstep(0.78, 0.18, distance_from_center);
    return color * vignette;
}}

vec4 window_shader() {{
    vec4 sampled = texture2D(tex, texcoord);

    /* PIPELINE_STEP_1_LINEARIZE */
    vec3 color = srgb_to_linear(sampled.rgb);

    /* PIPELINE_STEP_2_DISPLAY_POLICY */
    color = apply_display_policy(color);

    /* PIPELINE_STEP_3_RENDER_MODE */
#if RX_MODE_MONOCHROME == 1
    color = render_monochrome(color);
#elif RX_MODE_PALETTE == 1
    color = render_palette(color);
#endif

    /* PIPELINE_STEP_4_DITHER */
#if RX_ENABLE_DITHER == 1
    color = apply_ordered_dither(color, gl_FragCoord.xy);
#endif

    /* PIPELINE_STEP_5_SCANLINES */
#if RX_ENABLE_SCANLINES == 1
    color = apply_scanlines(color, gl_FragCoord.xy);
#endif

    /* PIPELINE_STEP_6_FLICKER */
#if RX_ENABLE_FLICKER == 1
    color = apply_flicker(color, time);
#endif

    /* PIPELINE_STEP_7_VIGNETTE */
#if RX_ENABLE_VIGNETTE == 1
    color = apply_vignette(color, texcoord);
#endif

    /* PIPELINE_STEP_8_ENCODE */
    return default_post_processing(vec4(linear_to_srgb(clamp(color, 0.0, 1.0)), sampled.a));
        }}
"""
        return shader
