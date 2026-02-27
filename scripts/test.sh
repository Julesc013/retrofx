#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
RETROFX="$ROOT_DIR/scripts/retrofx"
ACTIVE_DIR="$ROOT_DIR/active"
STATE_DIR="$ROOT_DIR/state"
PROFILES_DIR="$ROOT_DIR/profiles"
TEST_TMP_DIR="$STATE_DIR/tests"
BASE16_FIXTURE="$ROOT_DIR/tests/fixtures/base16.json"

log() {
  printf '[test] %s\n' "$*"
}

warn() {
  printf '[test][warn] %s\n' "$*" >&2
}

die() {
  printf '[test][error] %s\n' "$*" >&2
  exit 1
}

run_retrofx_x11() {
  DISPLAY=':99' WAYLAND_DISPLAY='' XDG_SESSION_TYPE='x11' "$RETROFX" "$@"
}

run_retrofx_wayland() {
  DISPLAY='' WAYLAND_DISPLAY='wayland-0' XDG_SESSION_TYPE='wayland' "$RETROFX" "$@"
}

run_retrofx_x11_home() {
  local test_home="$1"
  shift
  HOME="$test_home" DISPLAY=':99' WAYLAND_DISPLAY='' XDG_SESSION_TYPE='x11' "$RETROFX" "$@"
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  if ! printf '%s\n' "$haystack" | grep -Fq "$needle"; then
    die "expected output to contain: $needle"
  fi
}

assert_not_contains() {
  local haystack="$1"
  local needle="$2"
  if printf '%s\n' "$haystack" | grep -Fq "$needle"; then
    die "expected output to not contain: $needle"
  fi
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || die "missing expected file: $path"
}

hash_file() {
  local path="$1"
  sha256sum "$path" | awk '{print $1}'
}

line_of() {
  local pattern="$1"
  local path="$2"
  grep -n "$pattern" "$path" | head -n1 | cut -d: -f1
}

hex_brightness() {
  local hex="${1#\#}"
  local r g b
  r=$((16#${hex:0:2}))
  g=$((16#${hex:2:2}))
  b=$((16#${hex:4:2}))
  printf '%d' $(((299 * r + 587 * g + 114 * b) / 1000))
}

validate_active_files() {
  local mode="${1:-x11}"

  require_file "$ACTIVE_DIR/profile.toml"
  require_file "$ACTIVE_DIR/profile.env"
  require_file "$ACTIVE_DIR/xresources"
  require_file "$ACTIVE_DIR/Xresources"
  require_file "$ACTIVE_DIR/alacritty.toml"
  require_file "$ACTIVE_DIR/meta"
  require_file "$ACTIVE_DIR/semantic.env"
  require_file "$ACTIVE_DIR/tty-palette.env"
  require_file "$ACTIVE_DIR/tty-palette.txt"

  if [[ "$mode" == "wayland" ]]; then
    [[ ! -f "$ACTIVE_DIR/picom.conf" ]] || die "wayland active should not contain picom.conf"
    [[ ! -f "$ACTIVE_DIR/shader.glsl" ]] || die "wayland active should not contain shader.glsl"
  else
    require_file "$ACTIVE_DIR/picom.conf"
    require_file "$ACTIVE_DIR/shader.glsl"
  fi
}

validate_ansi_palette_env() {
  local palette_env="$1"
  local i key

  require_file "$palette_env"
  # shellcheck source=/dev/null
  source "$palette_env"

  for ((i = 0; i < 16; i++)); do
    key="ANSI_$i"
    [[ -n "${!key:-}" ]] || die "missing $key in $palette_env"
    [[ "${!key}" =~ ^#[0-9a-fA-F]{6}$ ]] || die "invalid $key format in $palette_env"
  done

  [[ -n "${SEM_BACKGROUND:-}" ]] || die "missing SEM_BACKGROUND"
  [[ -n "${SEM_NORMAL:-}" ]] || die "missing SEM_NORMAL"
  [[ -n "${SEM_DIM:-}" ]] || die "missing SEM_DIM"
  [[ -n "${SEM_BRIGHT:-}" ]] || die "missing SEM_BRIGHT"
  [[ -n "${SEM_INFO:-}" ]] || die "missing SEM_INFO"
  [[ -n "${SEM_SUCCESS:-}" ]] || die "missing SEM_SUCCESS"
  [[ -n "${SEM_WARNING:-}" ]] || die "missing SEM_WARNING"
  [[ -n "${SEM_ERROR:-}" ]] || die "missing SEM_ERROR"
}

validate_monochrome_semantics() {
  local palette_env="$1"
  local b_error b_warning b_success b_info

  # shellcheck source=/dev/null
  source "$palette_env"

  b_error="$(hex_brightness "$SEM_ERROR")"
  b_warning="$(hex_brightness "$SEM_WARNING")"
  b_success="$(hex_brightness "$SEM_SUCCESS")"
  b_info="$(hex_brightness "$SEM_INFO")"

  ((b_error >= b_warning)) || die "monochrome semantic mapping: error should be >= warning"
  ((b_warning >= b_success)) || die "monochrome semantic mapping: warning should be >= success"
  ((b_success >= b_info)) || die "monochrome semantic mapping: success should be >= info"
}

validate_shader_static() {
  local shader_file="$1"
  local expected_mode="$2"
  local expected_bands="$3"
  local expected_palette_kind="$4"
  local expected_palette_size="$5"
  local step
  local prev=0
  local line
  local -a steps=(
    'PIPELINE_STEP_1_LINEARIZE'
    'PIPELINE_STEP_2_TRANSFORM'
    'PIPELINE_STEP_3_QUANTIZE'
    'PIPELINE_STEP_4_DITHER'
    'PIPELINE_STEP_5_SCANLINES'
    'PIPELINE_STEP_6_FLICKER'
    'PIPELINE_STEP_7_VIGNETTE'
    'PIPELINE_STEP_8_ENCODE'
  )

  require_file "$shader_file"

  if grep -Eq '@[A-Z0-9_]+@' "$shader_file"; then
    die "shader contains unsubstituted placeholders"
  fi

  grep -q 'void main()' "$shader_file" || die "shader missing main()"
  grep -q 'gl_FragColor' "$shader_file" || die "shader missing gl_FragColor"

  grep -q 'for (i = 0; i < 16; i++)' "$shader_file" || die "vga16 loop bound is missing"
  if grep -Fq 'for (i = 0; i < 256' "$shader_file"; then
    die "forbidden 256-iteration loop found in shader"
  fi

  grep -q '#if ENABLE_DITHER == 1' "$shader_file" || die "missing dither guard"
  grep -q '#if MODE_MONO == 1 || MODE_PALETTE == 1' "$shader_file" || die "dither is not quantization-gated"

  for step in "${steps[@]}"; do
    line="$(line_of "$step" "$shader_file")"
    [[ -n "$line" ]] || die "shader missing marker $step"
    if ((line <= prev)); then
      die "shader marker order invalid at $step"
    fi
    prev="$line"
  done

  grep -q "^#define MONO_BANDS $expected_bands$" "$shader_file" || die "MONO_BANDS constant mismatch"
  grep -q "^#define PALETTE_SIZE $expected_palette_size$" "$shader_file" || die "PALETTE_SIZE constant mismatch"

  case "$expected_mode" in
    passthrough)
      grep -q '^#define MODE_PASSTHROUGH 1$' "$shader_file" || die "MODE_PASSTHROUGH mismatch"
      ;;
    mono)
      grep -q '^#define MODE_MONO 1$' "$shader_file" || die "MODE_MONO mismatch"
      ;;
    palette)
      grep -q '^#define MODE_PALETTE 1$' "$shader_file" || die "MODE_PALETTE mismatch"
      ;;
    *)
      die "unknown expected mode: $expected_mode"
      ;;
  esac

  case "$expected_palette_kind" in
    vga16)
      grep -q '^#define PALETTE_KIND_VGA16 1$' "$shader_file" || die "PALETTE_KIND_VGA16 mismatch"
      ;;
    mono2)
      grep -q '^#define PALETTE_KIND_MONO2 1$' "$shader_file" || die "PALETTE_KIND_MONO2 mismatch"
      ;;
    mono4)
      grep -q '^#define PALETTE_KIND_MONO4 1$' "$shader_file" || die "PALETTE_KIND_MONO4 mismatch"
      ;;
    mono8)
      grep -q '^#define PALETTE_KIND_MONO8 1$' "$shader_file" || die "PALETTE_KIND_MONO8 mismatch"
      ;;
    mono16)
      grep -q '^#define PALETTE_KIND_MONO16 1$' "$shader_file" || die "PALETTE_KIND_MONO16 mismatch"
      ;;
    cube32)
      grep -q '^#define PALETTE_KIND_CUBE32 1$' "$shader_file" || die "PALETTE_KIND_CUBE32 mismatch"
      ;;
    cube64)
      grep -q '^#define PALETTE_KIND_CUBE64 1$' "$shader_file" || die "PALETTE_KIND_CUBE64 mismatch"
      ;;
    cube128)
      grep -q '^#define PALETTE_KIND_CUBE128 1$' "$shader_file" || die "PALETTE_KIND_CUBE128 mismatch"
      ;;
    cube256)
      grep -q '^#define PALETTE_KIND_CUBE256 1$' "$shader_file" || die "PALETTE_KIND_CUBE256 mismatch"
      ;;
    custom)
      grep -q '^#define PALETTE_KIND_CUSTOM 1$' "$shader_file" || die "PALETTE_KIND_CUSTOM mismatch"
      ;;
    passthrough)
      :
      ;;
    *)
      die "unknown expected palette kind: $expected_palette_kind"
      ;;
  esac
}

count_custom_palette_entries() {
  local shader_file="$1"
  awk '
    /const vec3 CUSTOM_PALETTE\[CUSTOM_PALETTE_SIZE\] = vec3\[\]\(/ {in_block=1; next}
    in_block && /^\);$/ {in_block=0; print count + 0; exit}
    in_block && /vec3\(/ {count++}
  ' "$shader_file"
}

cleanup() {
  rm -rf "$TEST_TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TEST_TMP_DIR"

log "running shellcheck when available"
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck \
    "$RETROFX" \
    "$ROOT_DIR/scripts/test.sh" \
    "$ROOT_DIR/backends/tty/apply.sh" \
    "$ROOT_DIR/scripts/integrate/retrofx-env.sh" \
    "$ROOT_DIR/scripts/integrate/install-xsession.sh" \
    "$ROOT_DIR/scripts/integrate/remove-xsession.sh" \
    "$ROOT_DIR/scripts/ci.sh"
else
  warn "shellcheck not installed; skipping"
fi

log "checking version command"
version_output="$("$RETROFX" --version)"
assert_contains "$version_output" "retrofx "
assert_contains "$version_output" "x11=full"
assert_contains "$version_output" "wayland=degraded"

log "checking list command"
list_output="$(run_retrofx_x11 list)"
assert_contains "$list_output" "Core Pack:"
assert_contains "$list_output" "crt-green-p1-4band"
assert_contains "$list_output" "palette-128"

log "checking gallery command"
gallery_output="$(run_retrofx_x11 gallery)"
assert_contains "$gallery_output" "RetroFX offline gallery"
assert_contains "$gallery_output" "core"
assert_contains "$gallery_output" "community"

log "checking search command"
search_output="$(run_retrofx_x11 search crt)"
assert_contains "$search_output" "crt-green-p1-4band"

log "checking info command"
info_output="$(run_retrofx_x11 info crt-green-p1-4band)"
assert_contains "$info_output" "Profile: crt-green-p1-4band"
assert_contains "$info_output" "Mode"
info_font_output="$(run_retrofx_x11 info crt-green-fonts-aa)"
assert_contains "$info_font_output" "Profile: crt-green-fonts-aa"
assert_contains "$info_font_output" "Fonts"
assert_contains "$info_font_output" "Font AA"
info_c64_output="$(run_retrofx_x11 info c64)"
assert_contains "$info_c64_output" "Profile: c64"
assert_contains "$info_c64_output" "kind = custom"

log "checking export commands"
export_xr_path="$TEST_TMP_DIR/exported.Xresources"
run_retrofx_x11 export xresources crt-green-p1-4band "$export_xr_path"
require_file "$export_xr_path"
export_alacritty_path="$TEST_TMP_DIR/exported.alacritty.toml"
run_retrofx_x11 export alacritty crt-green-p1-4band "$export_alacritty_path"
require_file "$export_alacritty_path"
grep -q '^\[colors.primary\]$' "$export_alacritty_path" || die "exported alacritty file missing colors.primary block"
grep -q '^\[font.normal\]$' "$export_alacritty_path" || die "exported alacritty file missing font.normal block"

log "checking base16 import/export commands"
interop_profile_name="base16-test-profile"
interop_profile_file="$PROFILES_DIR/user/$interop_profile_name.toml"
interop_palette_file="$ROOT_DIR/palettes/imported/$interop_profile_name.txt"
rm -f "$interop_profile_file" "$interop_palette_file"
run_retrofx_x11 import base16 "$BASE16_FIXTURE" --name "$interop_profile_name"
require_file "$interop_profile_file"
require_file "$interop_palette_file"
base16_export_path="$TEST_TMP_DIR/exported.base16.json"
run_retrofx_x11 export base16 "$interop_profile_name" "$base16_export_path"
require_file "$base16_export_path"
grep -q '"system": "base16"' "$base16_export_path" || die "base16 export missing system key"
grep -q '"base00":' "$base16_export_path" || die "base16 export missing base00 key"
grep -q '"base0f":' "$base16_export_path" || die "base16 export missing base0f key"
rm -f "$interop_profile_file" "$interop_palette_file"

log "checking base16 sanitation rejects invalid colors"
invalid_base16="$TEST_TMP_DIR/base16-invalid.json"
cat >"$invalid_base16" <<'JSON'
{
  "base00": "#000000",
  "base01": "#111111",
  "base02": "#222222",
  "base03": "#333333",
  "base04": "#444444",
  "base05": "#555555",
  "base06": "#666666",
  "base07": "#777777",
  "base08": "#888888",
  "base09": "#999999",
  "base0a": "#zzzzzz",
  "base0b": "#bbbbbb",
  "base0c": "#cccccc",
  "base0d": "#dddddd",
  "base0e": "#eeeeee",
  "base0f": "#ffffff"
}
JSON
if run_retrofx_x11 import base16 "$invalid_base16" --name base16-invalid >/dev/null 2>&1; then
  die "base16 import accepted invalid color data"
fi

log "checking install-pack command (community placeholder)"
install_pack_output="$(run_retrofx_x11 install-pack community 2>&1)"
assert_contains "$install_pack_output" "has no profiles"

profiles=("$PROFILES_DIR"/*.toml)
if [[ ! -e "${profiles[0]}" ]]; then
  die "no profiles found in $PROFILES_DIR"
fi

if [[ -z "${DISPLAY:-}" ]] || ! command -v picom >/dev/null 2>&1; then
  warn "X11 or picom unavailable; runtime shader validation is expected to be skipped"
fi

log "applying each repository profile and validating generated active files"
for profile_path in "${profiles[@]}"; do
  [[ -e "$profile_path" ]] || continue
  profile_name="$(basename "$profile_path" .toml)"
  log "apply $profile_name"
  run_retrofx_x11 apply "$profile_name"
  validate_active_files
  validate_ansi_palette_env "$ACTIVE_DIR/tty-palette.env"
done

log "applying pack profile by id resolution"
run_retrofx_x11 apply crt-green-p1-4band
validate_active_files
assert_contains "$(cat "$ACTIVE_DIR/profile.env")" "PROFILE_ID=crt-green-p1-4band"

log "fonts + aa generation checks"
run_retrofx_x11 apply crt-green-fonts-aa
validate_active_files
require_file "$ACTIVE_DIR/fontconfig.conf"
grep -q '<bool>false</bool>' "$ACTIVE_DIR/fontconfig.conf" || die "fontconfig antialias mapping mismatch"
grep -q '<const>none</const>' "$ACTIVE_DIR/fontconfig.conf" || die "fontconfig subpixel mapping mismatch"
grep -q 'Terminus Nerd Font' "$ACTIVE_DIR/fontconfig.conf" || die "fontconfig missing terminal family override"
grep -q 'family = "Terminus Nerd Font"' "$ACTIVE_DIR/alacritty.toml" || die "alacritty missing terminal font family"
grep -q 'terminal_fallback: DejaVu Sans Mono, Noto Color Emoji' "$ACTIVE_DIR/alacritty.toml" || die "alacritty missing fallback comment"

log "static shader checks: monochrome profile"
mono_profile="$TEST_TMP_DIR/mono-check.toml"
cat >"$mono_profile" <<'PROFILE'
name = "Mono Check"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 13
phosphor = "green"
hotcore = true

[effects]
blur_strength = 1
scanlines = true
flicker = true
dither = "ordered"
vignette = true

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
run_retrofx_x11 apply "$mono_profile"
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" mono 13 vga16 16

log "static shader checks: cube256 palette profile"
palette_profile="$TEST_TMP_DIR/cube256-check.toml"
cat >"$palette_profile" <<'PROFILE'
name = "Cube256 Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "cube256"
size = 256

[effects]
blur_strength = 1
scanlines = true
flicker = false
dither = "ordered"
vignette = false

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
run_retrofx_x11 apply "$palette_profile"
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube256 256

log "static shader checks: structured palette family"
run_retrofx_x11 apply palette-2
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 mono2 2
run_retrofx_x11 apply palette-4
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 mono4 4
run_retrofx_x11 apply palette-8
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 mono8 8
run_retrofx_x11 apply palette-16
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 vga16 16
run_retrofx_x11 apply palette-32
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube32 32
run_retrofx_x11 apply palette-64
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube64 64
run_retrofx_x11 apply palette-128
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube128 128
run_retrofx_x11 apply palette-256
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube256 256

log "custom palette parsing + bounded constants"
custom_palette_file="$TEST_TMP_DIR/custom-pal.txt"
cat >"$custom_palette_file" <<'PAL'
# custom test palette
#000000
#  comment line with hash-space
#ff0000
#00ff00
#0000ff
PAL
custom_profile="$TEST_TMP_DIR/custom-palette.toml"
cat >"$custom_profile" <<PROFILE
name = "Custom Palette Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "custom"
size = 4
custom_file = "$custom_palette_file"

[effects]
blur_strength = 1
scanlines = false
flicker = false
dither = "ordered"
vignette = false

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
run_retrofx_x11 apply "$custom_profile"
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 custom 4
grep -q '^#define CUSTOM_PALETTE_SIZE 4$' "$ACTIVE_DIR/shader.glsl" || die "CUSTOM_PALETTE_SIZE define mismatch for custom palette"
[[ "$(count_custom_palette_entries "$ACTIVE_DIR/shader.glsl")" == "4" ]] || die "custom palette constant entry count mismatch"

log "picom selective rules + consistency knobs"
rules_profile="$TEST_TMP_DIR/rules-check.toml"
cat >"$rules_profile" <<'PROFILE'
name = "Rules Check"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 8
phosphor = "green"
hotcore = false

[effects]
blur_strength = 2
scanlines = true
scanline_preset = "blur_on"
flicker = false
dither = "ordered"
vignette = false
transparency = "rules"

[colors]
background = "#0b120b"
foreground = "#99ffaa"

[rules]
exclude_wm_class = ["firefox", "mpv"]
exclude_wm_name = ["Picture-in-Picture"]
exclude_opacity_below = 0.95

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
run_retrofx_x11 apply "$rules_profile"
validate_active_files
rules_cfg="$(cat "$ACTIVE_DIR/picom.conf")"
assert_contains "$rules_cfg" "blur-background-exclude = ["
assert_contains "$rules_cfg" "class_g = 'firefox'"
assert_contains "$rules_cfg" "class_g = 'mpv'"
assert_contains "$rules_cfg" "name = 'Picture-in-Picture'"
assert_contains "$rules_cfg" "opacity < 0.950000"
assert_contains "$rules_cfg" "detect-client-opacity = true;"
assert_contains "$rules_cfg" "unredir-if-possible = false;"

log "wayland degraded apply path"
wayland_apply_output="$(run_retrofx_wayland apply "$mono_profile" 2>&1)"
assert_contains "$wayland_apply_output" "Wayland session detected: shader pipeline disabled; applied degraded outputs only."
validate_active_files wayland

log "tty backend mock test: monochrome semantic mapping"
tty_mono_profile="$TEST_TMP_DIR/tty-mono.toml"
cat >"$tty_mono_profile" <<'PROFILE'
name = "TTY Mono Check"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 8
phosphor = "green"
hotcore = false

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "ordered"
vignette = false

[scope]
x11 = false
tty = true
tuigreet = false
PROFILE
RETROFX_TTY_MODE=mock run_retrofx_x11 apply "$tty_mono_profile"
validate_active_files
validate_ansi_palette_env "$ACTIVE_DIR/tty-palette.env"
validate_monochrome_semantics "$ACTIVE_DIR/tty-palette.env"
require_file "$STATE_DIR/tty-current.env"

log "tty backend mock test: vga16 semantic mapping"
tty_vga_profile="$TEST_TMP_DIR/tty-vga16.toml"
cat >"$tty_vga_profile" <<'PROFILE'
name = "TTY VGA16 Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "vga16"
size = 16

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = false
tty = true
tuigreet = false
PROFILE
RETROFX_TTY_MODE=mock run_retrofx_x11 apply "$tty_vga_profile"
# shellcheck source=/dev/null
source "$ACTIVE_DIR/tty-palette.env"
[[ "$ANSI_1" == '#aa0000' ]] || die "vga16 semantic mapping mismatch for ANSI_1"
[[ "$ANSI_2" == '#00aa00' ]] || die "vga16 semantic mapping mismatch for ANSI_2"
[[ "$ANSI_4" == '#0000aa' ]] || die "vga16 semantic mapping mismatch for ANSI_4"

log "tty backend mock test: cube256 summary palette"
tty_cube_profile="$TEST_TMP_DIR/tty-cube256.toml"
cat >"$tty_cube_profile" <<'PROFILE'
name = "TTY Cube256 Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "cube256"
size = 256

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = false
tty = true
tuigreet = false
PROFILE
RETROFX_TTY_MODE=mock run_retrofx_x11 apply "$tty_cube_profile"
validate_ansi_palette_env "$ACTIVE_DIR/tty-palette.env"
# shellcheck source=/dev/null
source "$ACTIVE_DIR/tty-palette.env"
(( $(hex_brightness "$ANSI_0") < 24 )) || die "cube256 summary palette ANSI_0 should remain dark"
(( $(hex_brightness "$ANSI_8") > $(hex_brightness "$ANSI_0") )) || die "cube256 summary palette should keep dim/bright separation"
[[ "$ANSI_1" != "$ANSI_0" ]] || die "cube256 summary palette missing accent contrast"

log "tuigreet backend generation test"
tuigreet_profile="$TEST_TMP_DIR/tuigreet-check.toml"
cat >"$tuigreet_profile" <<'PROFILE'
name = "Tuigreet Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "vga16"
size = 16

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = false
tty = false
tuigreet = true
PROFILE
run_retrofx_x11 apply "$tuigreet_profile"
require_file "$ACTIVE_DIR/tuigreet.conf"
grep -q '^background = "#' "$ACTIVE_DIR/tuigreet.conf" || die "tuigreet config missing background color"

log "verifying off --tty restores previous tty palette state in mock mode"
RETROFX_TTY_MODE=mock run_retrofx_x11 off --tty
require_file "$STATE_DIR/tty-current.env"

log "wizard non-interactive generation"
mkdir -p "$PROFILES_DIR/user"
before_user_list="$(find "$PROFILES_DIR/user" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort || true)"
before_user_count="$(find "$PROFILES_DIR/user" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | wc -l | awk '{print $1}')"
RETROFX_WIZARD_NONINTERACTIVE=1 run_retrofx_x11 new
after_user_count="$(find "$PROFILES_DIR/user" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | wc -l | awk '{print $1}')"
((after_user_count > before_user_count)) || die "non-interactive wizard did not create a user profile"
after_user_list="$(find "$PROFILES_DIR/user" -mindepth 1 -maxdepth 1 -type f -name '*.toml' | sort || true)"
wizard_profile_created="$(comm -13 <(printf '%s\n' "$before_user_list") <(printf '%s\n' "$after_user_list") | head -n1)"
[[ -n "$wizard_profile_created" ]] || die "unable to identify created wizard profile"
require_file "$wizard_profile_created"
grep -q '^name = "Wizard Default Profile"' "$wizard_profile_created" || die "wizard default profile content mismatch"
rm -f "$wizard_profile_created"

log "doctor capability output (simulated X11)"
doctor_x11_output="$(run_retrofx_x11 doctor 2>&1)"
assert_contains "$doctor_x11_output" "Session type: x11"
assert_contains "$doctor_x11_output" "WM/DE:"
assert_contains "$doctor_x11_output" "Capabilities:"
assert_contains "$doctor_x11_output" "X11 backend: full shader pipeline"

log "doctor capability output (simulated Wayland)"
doctor_wayland_output="$(run_retrofx_wayland doctor 2>&1)"
assert_contains "$doctor_wayland_output" "Session type: wayland"
assert_contains "$doctor_wayland_output" "Global post-process shaders are not supported in this backend."
assert_contains "$doctor_wayland_output" "Wayland backend: degraded outputs only"

log "doctor JSON output"
doctor_json_output="$(run_retrofx_x11 doctor --json)"
assert_contains "$doctor_json_output" "\"mode\":"
assert_contains "$doctor_json_output" "\"session\":"
assert_contains "$doctor_json_output" "\"picom_present\":"
assert_contains "$doctor_json_output" "\"warnings\":"
assert_contains "$doctor_json_output" "\"errors\":"
DOCTOR_JSON="$doctor_json_output" python3 - <<'PY'
import json
import os
import sys

data = json.loads(os.environ["DOCTOR_JSON"])
required = [
    "mode",
    "session",
    "picom_present",
    "glx_backend_possible",
    "available_profiles_count",
    "last_good_present",
    "tty_backend_available",
    "tuigreet_backend_available",
    "warnings",
    "errors",
]
missing = [k for k in required if k not in data]
if missing:
    raise SystemExit(f"doctor json missing keys: {missing}")
if not isinstance(data["warnings"], list) or not isinstance(data["errors"], list):
    raise SystemExit("doctor json warnings/errors must be arrays")
PY

log "self-check catches missing files in isolated RETROFX_HOME"
selfcheck_home="$TEST_TMP_DIR/selfcheck-home"
mkdir -p "$selfcheck_home"
for item in backends templates scripts profiles palettes docs README.md VERSION CHANGELOG.md; do
  if [[ -e "$ROOT_DIR/$item" ]]; then
    cp -a "$ROOT_DIR/$item" "$selfcheck_home/$item"
  fi
done
mkdir -p "$selfcheck_home/active" "$selfcheck_home/state"
RETROFX_HOME="$selfcheck_home" run_retrofx_x11 apply passthrough
RETROFX_HOME="$selfcheck_home" run_retrofx_x11 self-check
rm -f "$selfcheck_home/templates/shader.glsl.in"
if RETROFX_HOME="$selfcheck_home" run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail when template files are missing"
fi

log "install/uninstall cycle in isolated HOME"
install_home="$TEST_TMP_DIR/home-install"
mkdir -p "$install_home"
HOME="$install_home" run_retrofx_x11 install --yes
[[ -d "$install_home/.config/retrofx" ]] || die "install did not create ~/.config/retrofx"
[[ -x "$install_home/.local/bin/retrofx" ]] || die "install did not create launcher ~/.local/bin/retrofx"
install_status_output="$(HOME="$install_home" "$install_home/.local/bin/retrofx" status 2>&1)"
assert_contains "$install_status_output" "Execution mode: installed"
install_list_output="$(HOME="$install_home" "$install_home/.local/bin/retrofx" list 2>&1)"
assert_contains "$install_list_output" "Core Pack:"
HOME="$install_home" run_retrofx_x11 uninstall --yes
[[ ! -d "$install_home/.config/retrofx" ]] || die "uninstall did not remove ~/.config/retrofx"
[[ ! -e "$install_home/.local/bin/retrofx" ]] || die "uninstall did not remove launcher"

log "repair restores active from last_good"
run_retrofx_x11 apply crt-green-p1-4band
require_file "$STATE_DIR/last_good/profile.toml"
expected_repair_hash="$(hash_file "$STATE_DIR/last_good/profile.toml")"
printf 'corrupted=true\n' >"$ACTIVE_DIR/profile.toml"
if run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail for corrupted active/profile.toml"
fi
run_retrofx_x11 repair
repaired_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ "$repaired_hash" == "$expected_repair_hash" ]] || die "repair did not restore last_good profile state"
run_retrofx_x11 self-check

log "verifying apply -> off returns to passthrough baseline"
run_retrofx_x11 apply passthrough
baseline_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ ! -f "$ACTIVE_DIR/fontconfig.conf" ]] || die "passthrough should not generate fontconfig.conf by default"
run_retrofx_x11 apply "$mono_profile"
run_retrofx_x11 off
post_off_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ "$baseline_hash" == "$post_off_hash" ]] || die "off did not restore passthrough profile state"

log "verifying wayland off keeps degraded outputs and succeeds"
RETROFX_TTY_MODE=mock run_retrofx_wayland apply "$tty_mono_profile"
RETROFX_TTY_MODE=mock run_retrofx_wayland off
validate_active_files wayland

log "checking audit log exists"
require_file "$STATE_DIR/logs/retrofx.log"

log "all tests passed"
