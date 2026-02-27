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
  require_file "$ACTIVE_DIR/profile.toml"
  require_file "$ACTIVE_DIR/profile.env"
  require_file "$ACTIVE_DIR/picom.conf"
  require_file "$ACTIVE_DIR/shader.glsl"
  require_file "$ACTIVE_DIR/xresources"
  require_file "$ACTIVE_DIR/meta"
  require_file "$ACTIVE_DIR/semantic.env"
  require_file "$ACTIVE_DIR/tty-palette.env"
  require_file "$ACTIVE_DIR/tty-palette.txt"
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
"$RETROFX" list >/dev/null

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
  "$RETROFX" apply "$profile_name"
  validate_active_files
  validate_ansi_palette_env "$ACTIVE_DIR/tty-palette.env"
done

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
"$RETROFX" apply "$mono_profile"
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
"$RETROFX" apply "$palette_profile"
validate_active_files
validate_shader_static "$ACTIVE_DIR/shader.glsl" palette 4 cube256 256

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
RETROFX_TTY_MODE=mock "$RETROFX" apply "$tty_mono_profile"
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
RETROFX_TTY_MODE=mock "$RETROFX" apply "$tty_vga_profile"
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
RETROFX_TTY_MODE=mock "$RETROFX" apply "$tty_cube_profile"
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
"$RETROFX" apply "$tuigreet_profile"
require_file "$ACTIVE_DIR/tuigreet.conf"
grep -q '^background = "#' "$ACTIVE_DIR/tuigreet.conf" || die "tuigreet config missing background color"

log "verifying off --tty restores previous tty palette state in mock mode"
RETROFX_TTY_MODE=mock "$RETROFX" off --tty
require_file "$STATE_DIR/tty-current.env"

log "verifying apply -> off returns to passthrough baseline"
"$RETROFX" apply passthrough
baseline_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
"$RETROFX" apply "$mono_profile"
"$RETROFX" off
post_off_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ "$baseline_hash" == "$post_off_hash" ]] || die "off did not restore passthrough profile state"

log "checking audit log exists"
require_file "$STATE_DIR/logs/retrofx.log"

log "all tests passed"
