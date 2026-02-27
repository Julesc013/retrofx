#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
RETROFX="$ROOT_DIR/scripts/retrofx"
PROFILES_DIR="$ROOT_DIR/profiles"
ACTIVE_DIR="$ROOT_DIR/active"

readonly DEFAULT_PRIMARY_PROFILE="crt-green-4band"
readonly DEFAULT_FALLBACK_PROFILE="passthrough"

log() {
  printf 'i3-retro-session: %s\n' "$*"
}

warn() {
  printf 'i3-retro-session: warning: %s\n' "$*" >&2
}

profile_exists() {
  local ref="$1"
  [[ -f "$PROFILES_DIR/$ref.toml" || -f "$PROFILES_DIR/$ref" || -f "$ref" ]]
}

pick_profile() {
  local requested="${1:-}"
  local first_profile

  if [[ -n "$requested" ]]; then
    printf '%s' "$requested"
    return 0
  fi

  if [[ -n "${RETROFX_PROFILE:-}" ]]; then
    printf '%s' "$RETROFX_PROFILE"
    return 0
  fi

  if profile_exists "$DEFAULT_PRIMARY_PROFILE"; then
    printf '%s' "$DEFAULT_PRIMARY_PROFILE"
    return 0
  fi

  if profile_exists "$DEFAULT_FALLBACK_PROFILE"; then
    printf '%s' "$DEFAULT_FALLBACK_PROFILE"
    return 0
  fi

  first_profile="$(find "$PROFILES_DIR" -mindepth 1 -maxdepth 1 -name '*.toml' -printf '%f\n' 2>/dev/null | sort | head -n1 || true)"
  if [[ -n "$first_profile" ]]; then
    printf '%s' "${first_profile%.toml}"
    return 0
  fi

  printf 'passthrough'
}

start_picom_if_possible() {
  if [[ -z "${DISPLAY:-}" ]]; then
    warn "DISPLAY is not set; skipping picom launch"
    return 0
  fi

  if [[ ! -f "$ACTIVE_DIR/picom.conf" ]]; then
    warn "active/picom.conf is missing; skipping picom launch"
    return 0
  fi

  if ! command -v picom >/dev/null 2>&1; then
    warn "picom not installed; continuing without compositor"
    return 0
  fi

  if command -v pgrep >/dev/null 2>&1 && pgrep -x picom >/dev/null 2>&1; then
    log "picom is already running; not launching another instance"
    return 0
  fi

  (
    cd "$ACTIVE_DIR"
    nohup picom --config picom.conf >/dev/null 2>&1 &
  ) || warn "failed to launch picom; continuing with plain i3 session"
}

main() {
  local requested_profile="${1:-}"
  local profile=""
  local apply_ok=0

  if [[ $# -gt 0 ]]; then
    shift
  fi

  profile="$(pick_profile "$requested_profile")"

  if [[ ! -x "$RETROFX" ]]; then
    warn "retrofx script is missing or not executable at $RETROFX"
  else
    if "$RETROFX" apply "$profile"; then
      apply_ok=1
      log "applied profile '$profile'"
    else
      warn "profile apply failed for '$profile'; starting i3 without RetroFX compositor settings"
    fi
  fi

  if [[ "$apply_ok" -eq 1 ]]; then
    start_picom_if_possible
  fi

  exec i3 "$@"
}

main "$@"
