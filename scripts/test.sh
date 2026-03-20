#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
RETROFX="$ROOT_DIR/scripts/retrofx"
ACTIVE_DIR="$ROOT_DIR/active"
STATE_DIR="$ROOT_DIR/state"
MANIFESTS_DIR="$STATE_DIR/manifests"
PROFILES_DIR="$ROOT_DIR/profiles"
TEST_TMP_DIR="$STATE_DIR/tests"
BASE16_FIXTURE="$ROOT_DIR/tests/fixtures/base16.json"
RUNTIME_STATE_HELPER="$ROOT_DIR/scripts/integrate/retrofx-runtime-state.sh"

# shellcheck source=/dev/null
source "$RUNTIME_STATE_HELPER"

log() {
  printf '[test] %s\n' "$*"
}

section() {
  printf '\n[test][section] %s\n' "$*"
}

note() {
  printf '[test][note] %s\n' "$*"
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

assert_regex() {
  local haystack="$1"
  local regex="$2"
  if ! printf '%s\n' "$haystack" | grep -Eq "$regex"; then
    die "expected output to match regex: $regex"
  fi
}

assert_manifest_has_entry() {
  local manifest="$1"
  local class="$2"
  local rel="$3"

  if ! grep -Fqx "artifact=$class|$rel" "$manifest"; then
    die "expected manifest $manifest to contain artifact=$class|$rel"
  fi
}

assert_manifest_lacks_entry() {
  local manifest="$1"
  local class="$2"
  local rel="$3"

  if grep -Fqx "artifact=$class|$rel" "$manifest"; then
    die "expected manifest $manifest to omit artifact=$class|$rel"
  fi
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || die "missing expected file: $path"
}

assert_file_missing() {
  local path="$1"
  [[ ! -e "$path" ]] || die "unexpected file present: $path"
}

manifest_value() {
  local manifest="$1"
  local key="$2"

  awk -F= -v key="$key" '
    $1 == key {
      print substr($0, index($0, "=") + 1)
      exit
    }
  ' "$manifest"
}

assert_manifest_value() {
  local manifest="$1"
  local key="$2"
  local expected="$3"
  local actual

  actual="$(manifest_value "$manifest" "$key")"
  [[ -n "$actual" ]] || die "expected manifest $manifest to contain key '$key'"
  [[ "$actual" == "$expected" ]] || die "expected manifest $manifest $key=$expected, got ${actual:-<empty>}"
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
  require_file "$MANIFESTS_DIR/current.manifest"
  require_file "$MANIFESTS_DIR/last_good.manifest"

  if [[ "$mode" == "wayland" || "$mode" == "no-x11-runtime" ]]; then
    [[ ! -f "$ACTIVE_DIR/picom.conf" ]] || die "$mode active should not contain picom.conf"
    [[ ! -f "$ACTIVE_DIR/shader.glsl" ]] || die "$mode active should not contain shader.glsl"
  else
    require_file "$ACTIVE_DIR/picom.conf"
    require_file "$ACTIVE_DIR/shader.glsl"
  fi
}

assert_active_runtime_metadata_valid() {
  if ! retrofx_runtime_load_active_metadata "$ROOT_DIR"; then
    die "active runtime metadata is invalid: $RETROFX_RUNTIME_METADATA_ERROR"
  fi
}

assert_active_x11_runtime_enabled() {
  local expected="$1"

  assert_active_runtime_metadata_valid
  [[ "${RETROFX_RUNTIME_X11_RUNTIME_ENABLED:-false}" == "$expected" ]] ||
    die "expected x11_runtime_enabled=$expected, got ${RETROFX_RUNTIME_X11_RUNTIME_ENABLED:-unset}"
}

assert_active_compositor_required() {
  local expected="$1"

  assert_active_runtime_metadata_valid
  [[ "$RETROFX_RUNTIME_COMPOSITOR_REQUIRED" == "$expected" ]] ||
    die "expected compositor_required=$expected, got ${RETROFX_RUNTIME_COMPOSITOR_REQUIRED:-unset}"
}

assert_active_runtime_degraded() {
  local expected="$1"

  assert_active_runtime_metadata_valid
  [[ "$RETROFX_RUNTIME_DEGRADED" == "$expected" ]] ||
    die "expected degraded=$expected, got ${RETROFX_RUNTIME_DEGRADED:-unset}"
}

make_session_wrapper_stubs() {
  local stub_dir="$1"

  mkdir -p "$stub_dir"

  cat >"$stub_dir/picom" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
for arg in "$@"; do
  if [[ "$arg" == "--log-file" ]]; then
    exit 0
  fi
done
printf '%s\n' "$*" >>"${RETROFX_TEST_PICOM_LOG:?}"
exit 0
EOF

  cat >"$stub_dir/i3" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >>"${RETROFX_TEST_I3_LOG:?}"
exit 0
EOF

  cat >"$stub_dir/pgrep" <<'EOF'
#!/usr/bin/env bash
exit 1
EOF

  chmod +x "$stub_dir/picom" "$stub_dir/i3" "$stub_dir/pgrep"
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
  local expected_levels expected_inv
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

  grep -q 'vec4 window_shader()' "$shader_file" || die "shader missing window_shader()"
  grep -q 'default_post_processing' "$shader_file" || die "shader missing default_post_processing output"

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
  expected_levels=$((expected_bands - 1))
  grep -q "^#define MONO_LEVELS $expected_levels$" "$shader_file" || die "MONO_LEVELS constant mismatch"
  expected_inv="$(awk -v l="$expected_levels" 'BEGIN { printf "%.9f", 1.0 / l }')"
  grep -q "^#define MONO_INV_LEVELS $expected_inv$" "$shader_file" || die "MONO_INV_LEVELS constant mismatch"
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
    /vec3 custom_linear\(int idx\)/ {in_block=1; next}
    in_block && /^\}/ {in_block=0; print count + 0; exit}
    in_block && /return vec3\(/ {count++}
  ' "$shader_file"
}

cleanup() {
  rm -rf "$TEST_TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TEST_TMP_DIR"

section "Preflight / Execution Model"
note "repo-local regression suite with simulated X11/Wayland session env vars"
note "wrapper tests stub picom/i3 binaries; TTY tests use RETROFX_TTY_MODE=mock"
note "live X11/picom shader validation remains host-dependent and may be skipped"

log "running shellcheck when available"
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck \
    "$RETROFX" \
    "$ROOT_DIR/scripts/test.sh" \
    "$ROOT_DIR/backends/tty/apply.sh" \
    "$ROOT_DIR/scripts/integrate/retrofx-runtime-state.sh" \
    "$ROOT_DIR/scripts/integrate/i3-retro-session.sh" \
    "$ROOT_DIR/scripts/integrate/retrofx-env.sh" \
    "$ROOT_DIR/scripts/integrate/install-xsession.sh" \
    "$ROOT_DIR/scripts/integrate/remove-xsession.sh" \
    "$ROOT_DIR/scripts/ci.sh"
else
  warn "shellcheck not installed; skipping"
fi

section "CLI Surface / Basic Commands"

log "checking version command"
version_output="$("$RETROFX" --version)"
assert_contains "$version_output" "retrofx "
assert_contains "$version_output" "x11=full"
assert_contains "$version_output" "wayland=degraded"

log "checking help output"
help_output="$("$RETROFX" --help)"
assert_contains "$help_output" "retrofx explain <profile>"
assert_contains "$help_output" "retrofx apply <profile> [--safe] [--dry-run]"

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

log "checking explain command"
explain_passthrough_output="$(run_retrofx_x11 explain passthrough)"
assert_contains "$explain_passthrough_output" "RetroFX explain"
assert_contains "$explain_passthrough_output" "Profile: passthrough"
assert_contains "$explain_passthrough_output" "Compositor required: no"
assert_contains "$explain_passthrough_output" "Scoped backend hooks: (none)"
assert_contains "$explain_passthrough_output" "Optional runtime artifacts: picom.conf, shader.glsl"
explain_wayland_output="$(run_retrofx_wayland explain crt-green-p1-4band)"
assert_contains "$explain_wayland_output" "Resolved apply session: wayland"
assert_contains "$explain_wayland_output" "Runtime degraded: yes"
assert_contains "$explain_wayland_output" "wayland session detected; applying degraded outputs for x11 scope."

section "Interop / Export / Pack / Path"

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
run_retrofx_x11 apply "$interop_profile_name"
validate_active_files
base16_export_path="$TEST_TMP_DIR/exported.base16.json"
base16_export_path_again="$TEST_TMP_DIR/exported-again.base16.json"
run_retrofx_x11 export base16 "$interop_profile_name" "$base16_export_path"
run_retrofx_x11 export base16 "$interop_profile_name" "$base16_export_path_again"
require_file "$base16_export_path"
require_file "$base16_export_path_again"
grep -q '"system": "base16"' "$base16_export_path" || die "base16 export missing system key"
grep -q '"base00":' "$base16_export_path" || die "base16 export missing base00 key"
grep -q '"base0f":' "$base16_export_path" || die "base16 export missing base0f key"
cmp -s "$base16_export_path" "$base16_export_path_again" || die "base16 export should be deterministic for the same profile"
BASE16_FIXTURE_PATH="$BASE16_FIXTURE" BASE16_EXPORT_PATH="$base16_export_path" python3 - <<'PY'
import json
import os
import sys

with open(os.environ["BASE16_FIXTURE_PATH"], "r", encoding="utf-8") as fh:
    src = json.load(fh)
with open(os.environ["BASE16_EXPORT_PATH"], "r", encoding="utf-8") as fh:
    out = json.load(fh)

for key in [f"base{i:02x}" for i in range(16)]:
    if key not in out:
        raise SystemExit(f"missing exported key: {key}")

if out.get("system") != "base16":
    raise SystemExit("base16 export system key mismatch")
if out.get("generated_by") != "retrofx":
    raise SystemExit("base16 export generated_by mismatch")
if out.get("mapping") != "resolved-retrofx-ansi16":
    raise SystemExit("base16 export mapping metadata mismatch")
if out.get("round_trip") != "lossy-best-effort":
    raise SystemExit("base16 export round_trip metadata mismatch")
if "generated_at" in out:
    raise SystemExit("base16 export should not contain generated_at")

# Import keeps all 16 source slots in the custom palette file, but export
# serializes the resolved RetroFX ANSI16 palette after semantic anchors.
if out["base00"] != src["base00"].lower():
    raise SystemExit("base00 should preserve the imported background anchor")
if out["base05"] != src["base05"].lower():
    raise SystemExit("base05 should preserve the imported semantic foreground")
if out["base07"] != src["base05"].lower():
    raise SystemExit("base07 should reflect the resolved RetroFX ANSI7 foreground")
if out["base07"] == src["base07"].lower():
    raise SystemExit("base07 unexpectedly round-tripped losslessly")
PY
rm -f "$interop_profile_file" "$interop_palette_file" "$base16_export_path" "$base16_export_path_again"

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
invalid_base16_output="$(run_retrofx_x11 import base16 "$invalid_base16" --name base16-invalid 2>&1 || true)"
assert_contains "$invalid_base16_output" "base16 parse error"
if run_retrofx_x11 import base16 "$invalid_base16" --name base16-invalid >/dev/null 2>&1; then
  die "base16 import accepted invalid color data"
fi

log "checking install-pack command (community placeholder)"
install_pack_output="$(run_retrofx_x11 install-pack community 2>&1)"
assert_contains "$install_pack_output" "has no profiles"

log "install-pack core relocates pack-local assets into user-owned storage"
pack_home="$TEST_TMP_DIR/pack-install-home"
mkdir -p "$pack_home"
for item in backends templates scripts profiles palettes docs README.md VERSION CHANGELOG.md; do
  if [[ -e "$ROOT_DIR/$item" ]]; then
    cp -a "$ROOT_DIR/$item" "$pack_home/$item"
  fi
done
mkdir -p "$pack_home/active" "$pack_home/state"
pack_install_core_output="$(RETROFX_HOME="$pack_home" run_retrofx_x11 install-pack core 2>&1)"
assert_contains "$pack_install_core_output" "install-pack 'core':"
pack_c64_profile="$pack_home/profiles/user/c64.toml"
require_file "$pack_c64_profile"
pack_c64_asset_dir="$pack_home/profiles/user_assets/c64"
[[ -d "$pack_c64_asset_dir" ]] || die "install-pack core did not create user asset directory for c64"
pack_c64_asset="$(find "$pack_c64_asset_dir" -mindepth 1 -maxdepth 1 -type f | sort | head -n1 || true)"
[[ -n "$pack_c64_asset" && -f "$pack_c64_asset" ]] || die "install-pack core did not copy c64 palette asset"
grep -Fq 'custom_file = "../user_assets/c64/' "$pack_c64_profile" || die "installed c64 profile did not rewrite custom_file into user_assets"
pack_c64_rel="$(grep '^custom_file = ' "$pack_c64_profile" | head -n1 | sed -E 's/^[^"]*"([^"]+)".*$/\1/' || true)"
[[ -n "$pack_c64_rel" ]] || die "unable to read rewritten custom_file path from installed c64 profile"
[[ -f "$(dirname "$pack_c64_profile")/$pack_c64_rel" ]] || die "rewritten custom_file path does not resolve from installed c64 profile"
pack_apply_c64_output="$(RETROFX_HOME="$pack_home" run_retrofx_x11 apply c64 2>&1)"
assert_not_contains "$pack_apply_c64_output" "custom palette file not found"
require_file "$pack_home/active/profile.toml"
pack_reinstall_core_output="$(RETROFX_HOME="$pack_home" run_retrofx_x11 install-pack core 2>&1)"
assert_contains "$pack_reinstall_core_output" "copied=0"
rm -f "$pack_c64_asset"
missing_pack_asset_selfcheck_output="$(RETROFX_HOME="$pack_home" run_retrofx_x11 self-check 2>&1 || true)"
assert_contains "$missing_pack_asset_selfcheck_output" "active source profile missing source asset for palette.custom_file"
if RETROFX_HOME="$pack_home" run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail when relocated c64 asset is missing"
fi
missing_pack_asset_apply_output="$(RETROFX_HOME="$pack_home" run_retrofx_x11 apply c64 2>&1 || true)"
assert_contains "$missing_pack_asset_apply_output" "custom palette file not found"

section "Wrapper / Runtime Intent"
note "session wrapper checks validate launch policy with stubbed picom/i3 commands, not a live desktop session"

log "session wrapper skips picom for no-compositor runtime intent"
wrapper_stub_dir="$TEST_TMP_DIR/wrapper-stubs"
make_session_wrapper_stubs "$wrapper_stub_dir"
wrapper_picom_log="$TEST_TMP_DIR/wrapper-picom.log"
wrapper_i3_log="$TEST_TMP_DIR/wrapper-i3.log"
rm -f "$wrapper_picom_log" "$wrapper_i3_log"
wrapper_passthrough_output="$(
  RETROFX_TEST_PICOM_LOG="$wrapper_picom_log" \
    RETROFX_TEST_I3_LOG="$wrapper_i3_log" \
    PATH="$wrapper_stub_dir:$PATH" \
    DISPLAY=':99' WAYLAND_DISPLAY='' XDG_SESSION_TYPE='x11' \
    "$ROOT_DIR/scripts/integrate/i3-retro-session.sh" passthrough 2>&1
)"
sleep 0.2
assert_active_compositor_required "false"
assert_contains "$wrapper_passthrough_output" "active runtime metadata says compositor is not required; skipping compositor launch"
[[ ! -f "$wrapper_picom_log" ]] || die "wrapper should not launch picom for passthrough runtime intent"
require_file "$wrapper_i3_log"

log "session wrapper starts picom for compositor-required runtime intent"
rm -f "$wrapper_picom_log" "$wrapper_i3_log"
wrapper_crt_output="$(
  RETROFX_TEST_PICOM_LOG="$wrapper_picom_log" \
    RETROFX_TEST_I3_LOG="$wrapper_i3_log" \
    PATH="$wrapper_stub_dir:$PATH" \
    DISPLAY=':99' WAYLAND_DISPLAY='' XDG_SESSION_TYPE='x11' \
    "$ROOT_DIR/scripts/integrate/i3-retro-session.sh" crt-green-p1-4band 2>&1
)"
sleep 0.2
assert_active_compositor_required "true"
[[ -f "$wrapper_picom_log" ]] || die "wrapper should launch picom for compositor-required runtime intent"
require_file "$wrapper_i3_log"
assert_contains "$wrapper_crt_output" "applied profile 'crt-green-p1-4band'"

scope_x11_false_profile="$TEST_TMP_DIR/scope-x11-false.toml"
cat >"$scope_x11_false_profile" <<'PROFILE'
name = "Scope X11 False Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "vga16"
size = 16

[effects]
blur_strength = 3
scanlines = true
flicker = true
dither = "ordered"
vignette = true

[scope]
x11 = false
tty = false
tuigreet = false
PROFILE

log "scope.x11=false apply suppresses X11 runtime artifacts"
run_retrofx_x11 apply "$scope_x11_false_profile"
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "picom.conf"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "shader.glsl"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "picom.conf"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "shader.glsl"
scope_x11_false_status_output="$(run_retrofx_x11 status 2>&1)"
assert_contains "$scope_x11_false_status_output" "X11 runtime active: no"
assert_contains "$scope_x11_false_status_output" "Compositor required: no"
run_retrofx_x11 self-check
printf 'stale-picom\n' >"$ACTIVE_DIR/picom.conf"
printf 'stale-shader\n' >"$ACTIVE_DIR/shader.glsl"
scope_x11_false_selfcheck_output="$(run_retrofx_x11 self-check 2>&1 || true)"
assert_contains "$scope_x11_false_selfcheck_output" "should not exist when scope.x11=false"
run_retrofx_x11 repair
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"

log "transition from X11-active profile to scope.x11=false cleans stale X11 artifacts"
run_retrofx_x11 apply crt-green-p1-4band
require_file "$ACTIVE_DIR/picom.conf"
require_file "$ACTIVE_DIR/shader.glsl"
run_retrofx_x11 apply "$scope_x11_false_profile"
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
if [[ -f "$ACTIVE_DIR/picom.conf" || -f "$ACTIVE_DIR/shader.glsl" ]]; then
  die "scope.x11=false apply left stale X11 runtime artifacts in active/"
fi
run_retrofx_x11 self-check

log "session wrapper skips picom when scope.x11=false disables X11 runtime"
rm -f "$wrapper_picom_log" "$wrapper_i3_log"
wrapper_scope_x11_false_output="$(
  RETROFX_TEST_PICOM_LOG="$wrapper_picom_log" \
    RETROFX_TEST_I3_LOG="$wrapper_i3_log" \
    PATH="$wrapper_stub_dir:$PATH" \
    DISPLAY=':99' WAYLAND_DISPLAY='' XDG_SESSION_TYPE='x11' \
    "$ROOT_DIR/scripts/integrate/i3-retro-session.sh" "$scope_x11_false_profile" 2>&1
)"
sleep 0.2
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
assert_contains "$wrapper_scope_x11_false_output" "active runtime metadata says X11 runtime is disabled; skipping compositor launch"
assert_file_missing "$wrapper_picom_log"
require_file "$wrapper_i3_log"

log "explicit export stays separate from scope.x11=false active runtime"
before_scope_export_meta_hash="$(hash_file "$ACTIVE_DIR/meta")"
scope_x11_export_output="$TEST_TMP_DIR/scope-x11-false.Xresources"
run_retrofx_x11 export xresources "$scope_x11_false_profile" "$scope_x11_export_output"
require_file "$scope_x11_export_output"
after_scope_export_meta_hash="$(hash_file "$ACTIVE_DIR/meta")"
[[ "$before_scope_export_meta_hash" == "$after_scope_export_meta_hash" ]] || die "export xresources should not mutate active runtime metadata"
assert_active_x11_runtime_enabled "false"

log "runtime metadata missing or corrupt disables compositor intent safely"
run_retrofx_x11 apply crt-green-p1-4band
assert_active_compositor_required "true"
mv "$ACTIVE_DIR/meta" "$TEST_TMP_DIR/active.meta.backup"
if retrofx_runtime_current_requires_compositor "$ROOT_DIR"; then
  die "runtime metadata reader should fail closed when active/meta is missing"
fi
assert_contains "$RETROFX_RUNTIME_METADATA_ERROR" "missing runtime metadata"
cat >"$ACTIVE_DIR/meta" <<'META'
profile=crt-green-p1-4band.toml
session_type=x11
compositor_required=maybe
META
if retrofx_runtime_current_requires_compositor "$ROOT_DIR"; then
  die "runtime metadata reader should fail closed for invalid active/meta"
fi
assert_contains "$RETROFX_RUNTIME_METADATA_ERROR" "compositor_required"
run_retrofx_x11 repair
assert_active_compositor_required "true"

log "off resets compositor runtime intent"
run_retrofx_x11 apply crt-green-p1-4band
assert_active_compositor_required "true"
run_retrofx_x11 off
assert_active_compositor_required "false"
if retrofx_runtime_current_requires_compositor "$ROOT_DIR"; then
  die "off should leave a no-compositor active runtime intent"
fi

log "wayland degraded runtime intent never requires a compositor"
run_retrofx_wayland apply crt-green-p1-4band
assert_active_runtime_metadata_valid
[[ "$RETROFX_RUNTIME_SESSION_TYPE" == "wayland" ]] || die "expected active runtime session_type=wayland"
assert_active_compositor_required "false"
assert_active_runtime_degraded "true"
if retrofx_runtime_current_requires_compositor "$ROOT_DIR"; then
  die "wayland degraded runtime intent should not require a compositor"
fi
wayland_status_output="$(run_retrofx_wayland status 2>&1)"
assert_contains "$wayland_status_output" "Active session: wayland"
assert_contains "$wayland_status_output" "X11 runtime active: no"
assert_contains "$wayland_status_output" "Compositor required: no"

log "manifest contract follows apply/off transitions"
run_retrofx_x11 apply crt-green-p1-4band
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "profile_id" "crt-green-p1-4band"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "session_type" "x11"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "scope_x11" "true"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "compositor_required" "true"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "picom.conf"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "shader.glsl"
run_retrofx_x11 off
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "profile_id" "passthrough"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "session_type" "x11"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "scope_x11" "true"
assert_manifest_value "$MANIFESTS_DIR/current.manifest" "compositor_required" "false"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "picom.conf"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "shader.glsl"
assert_active_x11_runtime_enabled "true"
assert_active_compositor_required "false"

section "Generation / Static Output"

log "compatibility-check command runs and reports checks"
compat_output=""
compat_rc=0
set +e
compat_output="$(run_retrofx_x11 compatibility-check 2>&1)"
compat_rc=$?
set -e
case "$compat_rc" in
  0 | 1 | 2)
    ;;
  *)
    die "compatibility-check returned unexpected exit code: $compat_rc"
    ;;
esac
compat_header="$(printf '%s\n' "$compat_output" | head -n1)"
[[ "$compat_header" == "RetroFX compatibility-check" ]] || die "compatibility-check header mismatch"
assert_contains "$compat_output" "Shader compile"
assert_contains "$compat_output" "GLX backend"
assert_contains "$compat_output" "Blur capability"
assert_contains "$compat_output" "Degraded mode"
if ! printf '%s\n' "$compat_output" | grep -Eq 'PASS|FAIL'; then
  die "compatibility-check output missing PASS/FAIL tokens"
fi

log "apply hash skip + regeneration checks"
skip_profile="$TEST_TMP_DIR/skip-check.toml"
cat >"$skip_profile" <<'PROFILE'
name = "Skip Check"
version = 1
description = "skip check v1"

[mode]
type = "passthrough"

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
first_apply_output="$(run_retrofx_x11 apply "$skip_profile" 2>&1)"
assert_contains "$first_apply_output" "Compositor not required."
assert_contains "$first_apply_output" "apply: applied profile"
second_apply_output="$(run_retrofx_x11 apply "$skip_profile" 2>&1)"
assert_contains "$second_apply_output" "apply: No changes; skipping apply."
assert_not_contains "$second_apply_output" "applied profile"

cat >"$skip_profile" <<'PROFILE'
name = "Skip Check"
version = 1
description = "skip check v2"

[mode]
type = "passthrough"

[effects]
blur_strength = 0
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
third_apply_output="$(run_retrofx_x11 apply "$skip_profile" 2>&1)"
assert_not_contains "$third_apply_output" "No changes; skipping apply."
assert_contains "$third_apply_output" "apply: applied profile"
assert_not_contains "$third_apply_output" "picom not installed"
assert_not_contains "$third_apply_output" "x11-picom:"

log "apply --dry-run reports intent without mutating active state"
run_retrofx_x11 apply passthrough
dry_run_profile_hash_before="$(hash_file "$ACTIVE_DIR/profile.toml")"
dry_run_meta_hash_before="$(hash_file "$ACTIVE_DIR/meta")"
dry_run_manifest_hash_before="$(hash_file "$MANIFESTS_DIR/current.manifest")"
dry_run_last_good_hash_before="$(hash_file "$MANIFESTS_DIR/last_good.manifest")"
dry_run_output="$(run_retrofx_x11 apply crt-green-p1-4band --dry-run 2>&1)"
assert_contains "$dry_run_output" "RetroFX apply --dry-run"
assert_contains "$dry_run_output" "Profile: crt-green-p1-4band"
assert_contains "$dry_run_output" "Compositor required: yes"
assert_contains "$dry_run_output" "Static stage validation: passed"
assert_contains "$dry_run_output" "Would update active state: yes"
assert_contains "$dry_run_output" "apply --dry-run: no changes written to active/, manifests, or backups"
assert_contains "$dry_run_output" "apply --dry-run: runtime validation and backend hooks are skipped"
dry_run_profile_hash_after="$(hash_file "$ACTIVE_DIR/profile.toml")"
dry_run_meta_hash_after="$(hash_file "$ACTIVE_DIR/meta")"
dry_run_manifest_hash_after="$(hash_file "$MANIFESTS_DIR/current.manifest")"
dry_run_last_good_hash_after="$(hash_file "$MANIFESTS_DIR/last_good.manifest")"
[[ "$dry_run_profile_hash_before" == "$dry_run_profile_hash_after" ]] || die "apply --dry-run mutated active/profile.toml"
[[ "$dry_run_meta_hash_before" == "$dry_run_meta_hash_after" ]] || die "apply --dry-run mutated active/meta"
[[ "$dry_run_manifest_hash_before" == "$dry_run_manifest_hash_after" ]] || die "apply --dry-run mutated current manifest"
[[ "$dry_run_last_good_hash_before" == "$dry_run_last_good_hash_after" ]] || die "apply --dry-run mutated last_good manifest"
dry_run_noop_output="$(run_retrofx_x11 apply passthrough --dry-run 2>&1)"
assert_contains "$dry_run_noop_output" "Would update active state: no"

log "perf command outputs numeric stage timings"
perf_output="$(run_retrofx_x11 perf "$skip_profile")"
assert_contains "$perf_output" "RetroFX perf"
assert_regex "$perf_output" 'parse_ms=[0-9]+'
assert_regex "$perf_output" 'render_ms=[0-9]+'
assert_regex "$perf_output" 'file_writes_ms=[0-9]+'
assert_regex "$perf_output" 'picom_restart_ms=[0-9]+'
assert_regex "$perf_output" 'total_ms=[0-9]+'

log "safe-mode apply overrides high-risk profile settings"
safe_profile="$TEST_TMP_DIR/safe-check.toml"
cat >"$safe_profile" <<'PROFILE'
name = "Safe Check"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 64
phosphor = "green"
hotcore = true

[effects]
blur_strength = 6
scanlines = true
flicker = true
dither = "ordered"
vignette = true

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
safe_output="$(run_retrofx_x11 apply "$safe_profile" --safe 2>&1)"
assert_contains "$safe_output" "safe-mode overrides applied:"
validate_active_files
grep -q '^#define MONO_BANDS 8$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not cap monochrome bands"
grep -q '^#define HOTCORE 0$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not disable hotcore"
grep -q '^#define ENABLE_DITHER 0$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not disable dither"
grep -q '^#define ENABLE_SCANLINES 0$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not disable scanlines"
grep -q '^#define ENABLE_FLICKER 0$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not disable flicker"
grep -q 'blur-strength = 2;' "$ACTIVE_DIR/picom.conf" || die "safe-mode did not cap blur strength"

log "safe-mode downscales large custom palette to vga16"
safe_palette_file="$TEST_TMP_DIR/safe-custom-pal.txt"
: >"$safe_palette_file"
for idx in $(seq 0 31); do
  printf '#%02x%02x%02x\n' "$((idx * 7 % 256))" "$((idx * 13 % 256))" "$((idx * 19 % 256))" >>"$safe_palette_file"
done
safe_palette_profile="$TEST_TMP_DIR/safe-custom.toml"
cat >"$safe_palette_profile" <<PROFILE
name = "Safe Palette Check"
version = 1

[mode]
type = "palette"

[palette]
kind = "custom"
size = 32
custom_file = "$safe_palette_file"

[effects]
blur_strength = 2
scanlines = false
flicker = false
dither = "none"
vignette = false

[scope]
x11 = true
tty = false
tuigreet = false
PROFILE
safe_palette_output="$(run_retrofx_x11 apply "$safe_palette_profile" --safe 2>&1)"
assert_contains "$safe_palette_output" "safe-mode overrides applied:"
grep -q '^#define PALETTE_KIND_VGA16 1$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not force custom palette to vga16"
grep -q '^#define PALETTE_SIZE 16$' "$ACTIVE_DIR/shader.glsl" || die "safe-mode did not force palette size to 16"

profiles=("$PROFILES_DIR"/*.toml)
if [[ ! -e "${profiles[0]}" ]]; then
  die "no profiles found in $PROFILES_DIR"
fi

if [[ -z "${DISPLAY:-}" ]] || ! command -v picom >/dev/null 2>&1; then
  warn "live X11/picom runtime validation unavailable; simulated X11/static generation coverage continues"
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

log "shader glsl110 static safety checks (no array constructors)"
if grep -Fq 'vec3[' "$ACTIVE_DIR/shader.glsl"; then
  die "shader contains forbidden vec3[] array declaration/constructor"
fi
if grep -Fq 'mat[' "$ACTIVE_DIR/shader.glsl"; then
  die "shader contains forbidden matrix array declaration/constructor"
fi
if grep -Eq '^const[[:space:]]+vec3[[:space:]]+[A-Za-z0-9_]+\[' "$ACTIVE_DIR/shader.glsl"; then
  die "shader contains forbidden const vec3 array initializer"
fi
grep -q 'vga16_linear(' "$ACTIVE_DIR/shader.glsl" || die "shader missing vga16_linear() function"
grep -q 'custom_linear(' "$ACTIVE_DIR/shader.glsl" || die "shader missing custom_linear() function"
grep -q 'bayer4(' "$ACTIVE_DIR/shader.glsl" || die "shader missing bayer4() function"

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

section "Degraded / Backend / Diagnostics"
note "Wayland checks use simulated session vars; TTY backend checks run in mock mode"

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
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
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
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
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
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
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
validate_active_files no-x11-runtime
assert_active_x11_runtime_enabled "false"
assert_active_compositor_required "false"
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

section "Integrity / Repair / Install Cycle"

log "doctor JSON output"
doctor_json_output="$(run_retrofx_x11 doctor --json)"
assert_contains "$doctor_json_output" "\"mode\":"
assert_contains "$doctor_json_output" "\"session\":"
assert_contains "$doctor_json_output" "\"picom_present\":"
assert_contains "$doctor_json_output" "\"x11_runtime_active_for_current_profile\":"
assert_contains "$doctor_json_output" "\"compositor_required_for_current_profile\":"
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
    "runtime_contract_healthy",
    "generated_artifacts_complete",
    "install_assets_healthy",
    "x11_runtime_active_for_current_profile",
    "compositor_required_for_current_profile",
    "warnings",
    "errors",
]
missing = [k for k in required if k not in data]
if missing:
    raise SystemExit(f"doctor json missing keys: {missing}")
if not isinstance(data["warnings"], list) or not isinstance(data["errors"], list):
    raise SystemExit("doctor json warnings/errors must be arrays")
PY

log "self-check detects checksum corruption"
run_retrofx_x11 apply crt-green-p1-4band
require_file "$STATE_DIR/active_checksum"
printf 'deadbeef\n' >"$STATE_DIR/active_checksum"
checksum_selfcheck_output="$(run_retrofx_x11 self-check 2>&1 || true)"
assert_contains "$checksum_selfcheck_output" "last_good checksum mismatch"
assert_contains "$checksum_selfcheck_output" "Suggested action: run \`retrofx repair\`"
run_retrofx_x11 repair
run_retrofx_x11 self-check

log "self-check ignores zero-byte optional runtime artifacts"
run_retrofx_x11 apply crt-green-p1-4band
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "EPHEMERAL_RUNTIME" "picom-compat.log"
: >"$ACTIVE_DIR/picom-compat.log"
run_retrofx_x11 self-check

log "self-check detects missing required generated fontconfig artifact"
run_retrofx_x11 apply crt-green-fonts-aa
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "fontconfig.conf"
rm -f "$ACTIVE_DIR/fontconfig.conf"
missing_fontconfig_output="$(run_retrofx_x11 self-check 2>&1 || true)"
assert_contains "$missing_fontconfig_output" "Missing required artifacts:"
assert_contains "$missing_fontconfig_output" "active/fontconfig.conf"
if run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail when active/fontconfig.conf is missing"
fi

log "self-check detects zero-byte required generated shader artifact"
run_retrofx_x11 apply crt-green-p1-4band
: >"$ACTIVE_DIR/shader.glsl"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "shader.glsl"
zero_shader_output="$(run_retrofx_x11 self-check 2>&1 || true)"
assert_contains "$zero_shader_output" "active/shader.glsl is zero-byte"
if run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail for zero-byte active/shader.glsl"
fi

log "export-only artifacts do not fail self-check but do block no-op apply"
run_retrofx_x11 apply crt-green-p1-4band
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "EXPORT_ONLY" "xresources"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "EXPORT_ONLY" "Xresources"
rm -f "$ACTIVE_DIR/xresources" "$ACTIVE_DIR/Xresources"
run_retrofx_x11 self-check
export_gap_status_output="$(run_retrofx_x11 status 2>&1)"
assert_contains "$export_gap_status_output" "Runtime contract: healthy"
assert_contains "$export_gap_status_output" "Generated exports/support artifacts: incomplete"
reapply_after_export_gap_output="$(run_retrofx_x11 apply crt-green-p1-4band 2>&1)"
assert_not_contains "$reapply_after_export_gap_output" "No changes; skipping apply."
require_file "$ACTIVE_DIR/xresources"
require_file "$ACTIVE_DIR/Xresources"

log "sanity-perf command runs without failure"
sanity_perf_output="$(run_retrofx_x11 sanity-perf 2>&1)"
assert_contains "$sanity_perf_output" "sanity-perf"

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
assert_contains "$install_status_output" "Runtime contract: inactive"
assert_contains "$install_status_output" "Install assets: healthy"
install_list_output="$(HOME="$install_home" "$install_home/.local/bin/retrofx" list 2>&1)"
assert_contains "$install_list_output" "Core Pack:"
rm -f "$install_home/.config/retrofx/templates/shader.glsl.in"
install_status_broken_output="$(HOME="$install_home" "$install_home/.local/bin/retrofx" status 2>&1)"
assert_contains "$install_status_broken_output" "Runtime contract: inactive"
assert_contains "$install_status_broken_output" "Install assets: incomplete"
HOME="$install_home" run_retrofx_x11 uninstall --yes
assert_file_missing "$install_home/.config/retrofx"
assert_file_missing "$install_home/.local/bin/retrofx"

log "repair restores active from last_good"
run_retrofx_x11 apply crt-green-fonts-aa
require_file "$STATE_DIR/last_good/fontconfig.conf"
expected_repair_hash="$(hash_file "$STATE_DIR/last_good/fontconfig.conf")"
rm -f "$ACTIVE_DIR/fontconfig.conf"
if run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail for missing required fontconfig.conf"
fi
repair_output="$(run_retrofx_x11 repair 2>&1)"
assert_contains "$repair_output" "repair: restored active state from last_good"
assert_contains "$repair_output" "repair: runtime contract is healthy after repair"
repaired_hash="$(hash_file "$ACTIVE_DIR/fontconfig.conf")"
[[ "$repaired_hash" == "$expected_repair_hash" ]] || die "repair did not restore last_good fontconfig state"
run_retrofx_x11 self-check

log "verifying apply -> off returns to passthrough baseline"
run_retrofx_x11 apply passthrough
baseline_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ ! -f "$ACTIVE_DIR/fontconfig.conf" ]] || die "passthrough should not generate fontconfig.conf by default"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "picom.conf"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "fontconfig.conf"
run_retrofx_x11 apply "$mono_profile"
run_retrofx_x11 off
post_off_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ "$baseline_hash" == "$post_off_hash" ]] || die "off did not restore passthrough profile state"
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "picom.conf"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "fontconfig.conf"

log "repair after off restores passthrough last_good contract"
rm -f "$ACTIVE_DIR/profile.env"
if run_retrofx_x11 self-check >/dev/null 2>&1; then
  die "self-check should fail when active/profile.env is missing"
fi
repair_output="$(run_retrofx_x11 repair 2>&1)"
assert_contains "$repair_output" "repair: restored active state from last_good"
assert_contains "$repair_output" "repair: runtime contract is healthy after repair"
run_retrofx_x11 self-check
assert_manifest_has_entry "$MANIFESTS_DIR/current.manifest" "OPTIONAL_RUNTIME" "picom.conf"
assert_manifest_lacks_entry "$MANIFESTS_DIR/current.manifest" "REQUIRED_RUNTIME" "fontconfig.conf"

log "verifying wayland off keeps degraded outputs and succeeds"
RETROFX_TTY_MODE=mock run_retrofx_wayland apply "$tty_mono_profile"
RETROFX_TTY_MODE=mock run_retrofx_wayland off
validate_active_files wayland

log "checking audit log exists"
require_file "$STATE_DIR/logs/retrofx.log"

section "Summary"
note "static generation, artifact integrity, wrapper launch policy, pack relocation, and install-cycle regressions passed"
note "mocked coverage: wrapper launch tests, TTY backend application"
note "simulated session coverage: X11/Wayland intent, status, doctor, degraded mode"
note "outside automated guarantees: full live compositor/GLX behavior still requires host validation"

log "all tests passed"
