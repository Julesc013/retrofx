#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
RETROFX="$ROOT_DIR/scripts/retrofx"
ACTIVE_DIR="$ROOT_DIR/active"
STATE_DIR="$ROOT_DIR/state"
PROFILES_DIR="$ROOT_DIR/profiles"
TEST_TMP_DIR="$STATE_DIR/tests"

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

assert_contains() {
  local haystack="$1"
  local needle="$2"
  if ! printf '%s\n' "$haystack" | grep -Fq "$needle"; then
    die "expected output to contain: $needle"
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

cleanup() {
  rm -rf "$TEST_TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TEST_TMP_DIR"

log "running shellcheck when available"
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$RETROFX" "$ROOT_DIR/scripts/test.sh"
else
  warn "shellcheck not installed; skipping"
fi

log "checking list command"
list_output="$(run_retrofx_x11 list)"
assert_contains "$list_output" "Core Pack:"
assert_contains "$list_output" "crt-green-p1-4band"

log "checking search command"
search_output="$(run_retrofx_x11 search crt)"
assert_contains "$search_output" "crt-green-p1-4band"

log "checking info command"
info_output="$(run_retrofx_x11 info crt-green-p1-4band)"
assert_contains "$info_output" "Profile: crt-green-p1-4band"
assert_contains "$info_output" "Mode"

log "checking export commands"
export_xr_path="$TEST_TMP_DIR/exported.Xresources"
run_retrofx_x11 export xresources crt-green-p1-4band "$export_xr_path"
require_file "$export_xr_path"
export_alacritty_output="$(run_retrofx_x11 export alacritty crt-green-p1-4band "$TEST_TMP_DIR/alacritty.yml" 2>&1)"
assert_contains "$export_alacritty_output" "Export not yet supported in this build."

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
[[ "$ANSI_0" == '#000000' ]] || die "cube256 summary palette should keep black at ANSI_0"
[[ "$ANSI_8" == '#555555' ]] || die "cube256 summary palette should keep dim gray at ANSI_8"
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

log "verifying apply -> off returns to passthrough baseline"
run_retrofx_x11 apply passthrough
baseline_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
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
