#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
ACTIVE_DIR_DEFAULT="$ROOT_DIR/active"

log() {
  printf 'tuigreet backend: %s\n' "$*"
}

warn() {
  printf 'tuigreet backend: warning: %s\n' "$*" >&2
}

usage() {
  cat <<'USAGE'
Usage:
  backends/tuigreet/apply.sh apply [active_dir]
  backends/tuigreet/apply.sh off [active_dir]
  backends/tuigreet/apply.sh check [active_dir]
USAGE
}

validate_semantic_env() {
  local semantic_env="$1"
  [[ -f "$semantic_env" ]] || return 1
  # shellcheck source=/dev/null
  source "$semantic_env"
  [[ -n "${SEM_BACKGROUND:-}" ]] || return 1
  [[ -n "${SEM_NORMAL:-}" ]] || return 1
  [[ -n "${SEM_BRIGHT:-}" ]] || return 1
  [[ -n "${SEM_INFO:-}" ]] || return 1
  [[ -n "${SEM_SUCCESS:-}" ]] || return 1
  [[ -n "${SEM_WARNING:-}" ]] || return 1
  [[ -n "${SEM_ERROR:-}" ]] || return 1
  return 0
}

write_tuigreet_conf() {
  local active_dir="$1"
  local semantic_env="$active_dir/semantic.env"
  local out_file="$active_dir/tuigreet.conf"
  local tmp_file

  validate_semantic_env "$semantic_env" || return 1
  # shellcheck source=/dev/null
  source "$semantic_env"

  tmp_file="$(mktemp "$active_dir/.tuigreet.XXXXXX")"
  {
    printf '# RetroFX tuigreet theme snippet\n'
    printf '# Generated from active profile semantic colors.\n'
    printf '# Integrate this file in your user-level greetd/tuigreet invocation.\n\n'
    printf 'background = "%s"\n' "$SEM_BACKGROUND"
    printf 'foreground = "%s"\n' "$SEM_NORMAL"
    printf 'accent = "%s"\n' "$SEM_BRIGHT"
    printf 'info = "%s"\n' "$SEM_INFO"
    printf 'success = "%s"\n' "$SEM_SUCCESS"
    printf 'warning = "%s"\n' "$SEM_WARNING"
    printf 'error = "%s"\n' "$SEM_ERROR"
  } >"$tmp_file"

  mv "$tmp_file" "$out_file"
}

cmd_apply() {
  local active_dir="$1"
  if write_tuigreet_conf "$active_dir"; then
    log "generated $active_dir/tuigreet.conf"
    return 0
  fi

  warn "unable to generate tuigreet theme snippet"
  return 1
}

cmd_off() {
  local active_dir="$1"
  rm -f "$active_dir/tuigreet.conf"
  log "removed $active_dir/tuigreet.conf"
}

cmd_check() {
  local active_dir="$1"
  if validate_semantic_env "$active_dir/semantic.env"; then
    log "semantic env is valid"
    return 0
  fi
  warn "missing or invalid semantic env in $active_dir"
  return 1
}

main() {
  local cmd="${1:-apply}"
  local active_dir="${2:-$ACTIVE_DIR_DEFAULT}"

  case "$cmd" in
    apply)
      cmd_apply "$active_dir"
      ;;
    off)
      cmd_off "$active_dir"
      ;;
    check)
      cmd_check "$active_dir"
      ;;
    -h | --help | help)
      usage
      ;;
    *)
      warn "unknown command '$cmd'"
      return 1
      ;;
  esac
}

main "$@"
