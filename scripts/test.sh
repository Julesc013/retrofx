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

validate_active_files() {
  require_file "$ACTIVE_DIR/profile.toml"
  require_file "$ACTIVE_DIR/profile.env"
  require_file "$ACTIVE_DIR/picom.conf"
  require_file "$ACTIVE_DIR/shader.glsl"
  require_file "$ACTIVE_DIR/xresources"
  require_file "$ACTIVE_DIR/meta"
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

log "applying each profile and validating generated active files"
for profile_path in "${profiles[@]}"; do
  [[ -e "$profile_path" ]] || continue
  profile_name="$(basename "$profile_path" .toml)"
  log "apply $profile_name"
  "$RETROFX" apply "$profile_name"
  validate_active_files
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
