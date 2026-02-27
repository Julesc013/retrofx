#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
STATE_DIR="$ROOT_DIR/state"
TTY_BACKUPS_DIR="$STATE_DIR/tty-backups"
TTY_CURRENT_FILE="$STATE_DIR/tty-current.env"
ACTIVE_DIR_DEFAULT="$ROOT_DIR/active"
DEFAULT_TTY_DEVICE="${RETROFX_TTY_DEVICE:-/dev/tty}"

log() {
  printf 'tty backend: %s\n' "$*"
}

warn() {
  printf 'tty backend: warning: %s\n' "$*" >&2
}

die() {
  printf 'tty backend: error: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'USAGE'
Usage:
  backends/tty/apply.sh apply [active_dir]
  backends/tty/apply.sh off [active_dir]
  backends/tty/apply.sh check [active_dir]

Environment:
  RETROFX_TTY_MODE=auto|mock|apply|force
  RETROFX_TTY_DEVICE=/dev/ttyN (default: /dev/tty)
USAGE
}

ensure_dirs() {
  mkdir -p "$STATE_DIR" "$TTY_BACKUPS_DIR"
}

write_builtin_vga_palette_env() {
  local out_file="$1"
  cat >"$out_file" <<'PALETTE'
ANSI_0='#000000'
ANSI_1='#aa0000'
ANSI_2='#00aa00'
ANSI_3='#aa5500'
ANSI_4='#0000aa'
ANSI_5='#aa00aa'
ANSI_6='#00aaaa'
ANSI_7='#aaaaaa'
ANSI_8='#555555'
ANSI_9='#ff5555'
ANSI_10='#55ff55'
ANSI_11='#ffff55'
ANSI_12='#5555ff'
ANSI_13='#ff55ff'
ANSI_14='#55ffff'
ANSI_15='#ffffff'
SEM_BACKGROUND='#000000'
SEM_NORMAL='#aaaaaa'
SEM_DIM='#555555'
SEM_BRIGHT='#ffffff'
SEM_INFO='#0000aa'
SEM_SUCCESS='#00aa00'
SEM_WARNING='#aa5500'
SEM_ERROR='#aa0000'
PALETTE
}

write_palette_env_from_sys_defaults() {
  local out_file="$1"
  local rf gf bf
  local red_csv grn_csv blu_csv
  local -a rr gg bb
  local i

  rf='/sys/module/vt/parameters/default_red'
  gf='/sys/module/vt/parameters/default_grn'
  bf='/sys/module/vt/parameters/default_blu'

  [[ -r "$rf" && -r "$gf" && -r "$bf" ]] || return 1

  red_csv="$(cat "$rf")"
  grn_csv="$(cat "$gf")"
  blu_csv="$(cat "$bf")"

  IFS=',' read -r -a rr <<<"$red_csv"
  IFS=',' read -r -a gg <<<"$grn_csv"
  IFS=',' read -r -a bb <<<"$blu_csv"

  if ((${#rr[@]} < 16 || ${#gg[@]} < 16 || ${#bb[@]} < 16)); then
    return 1
  fi

  : >"$out_file"
  for ((i = 0; i < 16; i++)); do
    printf "ANSI_%d='#%02x%02x%02x'\n" "$i" "${rr[$i]}" "${gg[$i]}" "${bb[$i]}" >>"$out_file"
  done

  printf "SEM_BACKGROUND=%q\n" "$(grep '^ANSI_0=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_NORMAL=%q\n" "$(grep '^ANSI_7=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_DIM=%q\n" "$(grep '^ANSI_8=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_BRIGHT=%q\n" "$(grep '^ANSI_15=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_INFO=%q\n" "$(grep '^ANSI_4=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_SUCCESS=%q\n" "$(grep '^ANSI_2=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_WARNING=%q\n" "$(grep '^ANSI_3=' "$out_file" | cut -d\' -f2)" >>"$out_file"
  printf "SEM_ERROR=%q\n" "$(grep '^ANSI_1=' "$out_file" | cut -d\' -f2)" >>"$out_file"
}

validate_palette_env() {
  local palette_file="$1"
  local i key

  [[ -f "$palette_file" ]] || return 1
  # shellcheck source=/dev/null
  source "$palette_file"

  for ((i = 0; i < 16; i++)); do
    key="ANSI_$i"
    [[ -n "${!key:-}" ]] || return 1
  done

  return 0
}

detect_tty_mode() {
  local requested="${RETROFX_TTY_MODE:-auto}"
  local tty_path=""

  case "$requested" in
    mock)
      printf 'mock'
      return 0
      ;;
    force | apply)
      printf 'apply'
      return 0
      ;;
    auto)
      if tty_path="$(tty 2>/dev/null)" && [[ "$tty_path" =~ ^/dev/tty[0-9]+$ ]] && [[ -w "$DEFAULT_TTY_DEVICE" ]]; then
        printf 'apply'
      else
        printf 'mock'
      fi
      return 0
      ;;
    *)
      warn "invalid RETROFX_TTY_MODE '$requested'; falling back to auto"
      if tty_path="$(tty 2>/dev/null)" && [[ "$tty_path" =~ ^/dev/tty[0-9]+$ ]] && [[ -w "$DEFAULT_TTY_DEVICE" ]]; then
        printf 'apply'
      else
        printf 'mock'
      fi
      return 0
      ;;
  esac
}

apply_palette_to_tty_device() {
  local palette_file="$1"
  local tty_device="$2"
  local i key hex

  validate_palette_env "$palette_file" || return 1

  for ((i = 0; i < 16; i++)); do
    key="ANSI_$i"
    # shellcheck disable=SC2154
    hex="${!key#\#}"
    printf '\033]P%x%s' "$i" "${hex,,}" >"$tty_device" || return 1
  done

  return 0
}

capture_previous_palette() {
  local out_file="$1"

  if [[ -f "$TTY_CURRENT_FILE" ]]; then
    cp "$TTY_CURRENT_FILE" "$out_file"
    return 0
  fi

  if write_palette_env_from_sys_defaults "$out_file"; then
    return 0
  fi

  write_builtin_vga_palette_env "$out_file"
}

latest_backup_file() {
  find "$TTY_BACKUPS_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.env' -printf '%f\n' 2>/dev/null | sort | tail -n1
}

cmd_check() {
  local active_dir="$1"
  local palette_file="$active_dir/tty-palette.env"

  ensure_dirs
  if validate_palette_env "$palette_file"; then
    log "palette file is valid: $palette_file"
    return 0
  fi

  warn "palette file is invalid or missing: $palette_file"
  return 1
}

cmd_apply() {
  local active_dir="$1"
  local target_palette="$active_dir/tty-palette.env"
  local backup_file=""
  local mode=""

  ensure_dirs
  validate_palette_env "$target_palette" || die "missing or invalid palette file: $target_palette"

  backup_file="$TTY_BACKUPS_DIR/tty-$(date -u +%Y%m%d-%H%M%S)-pid$$.env"
  capture_previous_palette "$backup_file"

  mode="$(detect_tty_mode)"
  case "$mode" in
    mock)
      cp "$target_palette" "$TTY_CURRENT_FILE"
      log "mock mode: recorded palette only (no console write)"
      ;;
    apply)
      if ! apply_palette_to_tty_device "$target_palette" "$DEFAULT_TTY_DEVICE"; then
        warn "console palette write failed; restoring previous palette"
        apply_palette_to_tty_device "$backup_file" "$DEFAULT_TTY_DEVICE" || warn "failed to restore previous palette"
        return 1
      fi
      cp "$target_palette" "$TTY_CURRENT_FILE"
      log "applied tty palette to $DEFAULT_TTY_DEVICE"
      ;;
  esac

  return 0
}

cmd_off() {
  local _active_dir="$1"
  local restore_file=""
  local latest=""
  local mode=""

  ensure_dirs

  latest="$(latest_backup_file)"
  if [[ -n "$latest" ]]; then
    restore_file="$TTY_BACKUPS_DIR/$latest"
  else
    restore_file="$TTY_BACKUPS_DIR/tty-default.env"
    if ! write_palette_env_from_sys_defaults "$restore_file"; then
      write_builtin_vga_palette_env "$restore_file"
    fi
  fi

  mode="$(detect_tty_mode)"
  case "$mode" in
    mock)
      cp "$restore_file" "$TTY_CURRENT_FILE"
      log "mock mode: restored previous palette state only"
      ;;
    apply)
      if ! apply_palette_to_tty_device "$restore_file" "$DEFAULT_TTY_DEVICE"; then
        warn "failed to restore tty palette from $restore_file"
        return 1
      fi
      cp "$restore_file" "$TTY_CURRENT_FILE"
      log "restored tty palette from $restore_file"
      ;;
  esac

  if [[ -n "$latest" ]]; then
    rm -f "$TTY_BACKUPS_DIR/$latest"
  fi

  return 0
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
      die "unknown command '$cmd'"
      ;;
  esac
}

main "$@"
