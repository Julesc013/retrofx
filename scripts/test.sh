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

  require_file "$ACTIVE_DIR/profile.toml"
  require_file "$ACTIVE_DIR/profile.env"
  require_file "$ACTIVE_DIR/picom.conf"
  require_file "$ACTIVE_DIR/shader.glsl"
  require_file "$ACTIVE_DIR/xresources"
  require_file "$ACTIVE_DIR/meta"
done

log "verifying apply -> off returns to passthrough baseline"
"$RETROFX" apply passthrough
baseline_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"

non_passthrough=""
for profile_path in "${profiles[@]}"; do
  [[ -e "$profile_path" ]] || continue
  candidate="$(basename "$profile_path" .toml)"
  if [[ "$candidate" != "passthrough" ]]; then
    non_passthrough="$candidate"
    break
  fi
done

if [[ -z "$non_passthrough" ]]; then
  non_passthrough_path="$TEST_TMP_DIR/temp-monochrome.toml"
  cat >"$non_passthrough_path" <<'PROFILE'
name = "Temp Test Monochrome"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 4
phosphor = "green"
hotcore = false

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
  log "apply temp test profile"
  "$RETROFX" apply "$non_passthrough_path"
else
  log "apply $non_passthrough"
  "$RETROFX" apply "$non_passthrough"
fi

"$RETROFX" off
post_off_hash="$(hash_file "$ACTIVE_DIR/profile.toml")"
[[ "$baseline_hash" == "$post_off_hash" ]] || die "off did not restore passthrough profile state"

log "checking audit log exists"
require_file "$STATE_DIR/logs/retrofx.log"

log "all tests passed"
