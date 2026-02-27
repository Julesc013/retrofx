#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
ACTIVE_DIR_DEFAULT="$ROOT_DIR/active"

log() {
  printf 'x11-picom: %s\n' "$*"
}

warn() {
  printf 'x11-picom: warning: %s\n' "$*" >&2
}

usage() {
  cat <<'USAGE'
Usage:
  backends/x11-picom/apply.sh apply [active_dir]
  backends/x11-picom/apply.sh check [active_dir]
  backends/x11-picom/apply.sh run [active_dir]

Notes:
- Phase 1 does not daemonize picom.
- Use `run` to launch picom in the foreground for testing.
USAGE
}

validate_active_dir() {
  local dir="$1"
  [[ -f "$dir/picom.conf" ]] || { warn "missing $dir/picom.conf"; return 1; }
  [[ -f "$dir/shader.glsl" ]] || { warn "missing $dir/shader.glsl"; return 1; }
  return 0
}

check_runtime() {
  local dir="$1"
  local rc=0

  validate_active_dir "$dir" || return 1

  if ! command -v picom >/dev/null 2>&1; then
    warn "picom not installed"
    return 1
  fi

  if [[ -z "${DISPLAY:-}" ]]; then
    warn "DISPLAY is not set; cannot run live picom check"
    return 1
  fi

  if command -v pgrep >/dev/null 2>&1 && pgrep -x picom >/dev/null 2>&1; then
    warn "picom is already running; skip launching test instance"
    return 0
  fi

  if command -v timeout >/dev/null 2>&1; then
    (cd "$dir" && timeout 3s picom --config picom.conf >/dev/null 2>&1) || rc=$?
  else
    (cd "$dir" && picom --config picom.conf >/dev/null 2>&1) || rc=$?
  fi

  case "$rc" in
    0 | 124)
      log "picom check passed"
      return 0
      ;;
    *)
      warn "picom check failed with exit code $rc"
      return 1
      ;;
  esac
}

run_foreground() {
  local dir="$1"

  validate_active_dir "$dir" || return 1

  if ! command -v picom >/dev/null 2>&1; then
    warn "picom not installed"
    return 1
  fi

  if [[ -z "${DISPLAY:-}" ]]; then
    warn "DISPLAY is not set"
    return 1
  fi

  log "starting picom in foreground from $dir"
  cd "$dir"
  exec picom --config picom.conf
}

apply_hint() {
  local dir="$1"

  validate_active_dir "$dir" || return 1

  if [[ -z "${DISPLAY:-}" ]]; then
    warn "not in an X11 session; generated config is ready at $dir"
    return 0
  fi

  if command -v picom >/dev/null 2>&1; then
    check_runtime "$dir" || warn "runtime check did not complete cleanly"
  else
    warn "picom not installed; cannot validate"
  fi

  log "RetroFX config staged for X11 + picom."
  log "Run in foreground: (cd '$dir' && picom --config picom.conf)"
  log "Integrate with i3 by pointing your picom launch command to this active config."
}

main() {
  local cmd="${1:-apply}"
  local active_dir="${2:-$ACTIVE_DIR_DEFAULT}"

  case "$cmd" in
    apply)
      apply_hint "$active_dir"
      ;;
    check)
      check_runtime "$active_dir"
      ;;
    run)
      run_foreground "$active_dir"
      ;;
    -h | --help | help)
      usage
      ;;
    *)
      warn "unknown command '$cmd'"
      usage
      return 1
      ;;
  esac
}

main "$@"
