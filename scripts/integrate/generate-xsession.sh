#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
WRAPPER_PATH="$ROOT_DIR/scripts/integrate/i3-retro-session.sh"

SESSION_NAME_DEFAULT="RetroFX i3"
SESSION_FILE_NAME_DEFAULT="retrofx-i3.desktop"

usage() {
  cat <<'USAGE'
Usage:
  scripts/integrate/generate-xsession.sh [--name "Display Name"] [--filename retrofx-i3.desktop]

Writes a user-local Xsession entry under:
  ~/.local/share/xsessions/
USAGE
}

die() {
  printf 'generate-xsession: error: %s\n' "$*" >&2
  exit 1
}

main() {
  local session_name="$SESSION_NAME_DEFAULT"
  local session_filename="$SESSION_FILE_NAME_DEFAULT"
  local xsessions_dir out_file tmp_file

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name)
        [[ $# -ge 2 ]] || die "--name requires a value"
        session_name="$2"
        shift 2
        ;;
      --filename)
        [[ $# -ge 2 ]] || die "--filename requires a value"
        session_filename="$2"
        shift 2
        ;;
      -h | --help | help)
        usage
        return 0
        ;;
      *)
        die "unknown argument: $1"
        ;;
    esac
  done

  [[ -x "$WRAPPER_PATH" ]] || die "wrapper script is not executable: $WRAPPER_PATH"

  xsessions_dir="${XDG_DATA_HOME:-$HOME/.local/share}/xsessions"
  out_file="$xsessions_dir/$session_filename"
  mkdir -p "$xsessions_dir"

  tmp_file="$(mktemp "$xsessions_dir/.retrofx-i3.desktop.XXXXXX")"
  {
    printf '[Desktop Entry]\n'
    printf 'Type=Application\n'
    printf 'Name=%s\n' "$session_name"
    printf 'Comment=RetroFX i3 session wrapper\n'
    printf 'Exec=%s\n' "$WRAPPER_PATH"
    printf 'TryExec=i3\n'
    printf 'DesktopNames=i3\n'
  } >"$tmp_file"

  mv "$tmp_file" "$out_file"
  printf 'generate-xsession: wrote %s\n' "$out_file"
}

main "$@"
