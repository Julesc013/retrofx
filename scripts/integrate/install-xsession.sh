#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME_DEFAULT="RetroFX i3"
SESSION_FILE_NAME_DEFAULT="retrofx-i3.desktop"
PROFILE_DEFAULT="crt-green-p1-4band"
MARKER_KEY="X-RetroFX-Managed=true"

usage() {
  cat <<'USAGE'
Usage:
  scripts/integrate/install-xsession.sh [--name "Display Name"] [--filename retrofx-i3.desktop] [--profile <profile>] [--retrofx-home <dir>]

Creates a user-local Xsession desktop entry at:
  ~/.local/share/xsessions/<filename>
USAGE
}

die() {
  printf 'install-xsession: error: %s\n' "$*" >&2
  exit 1
}

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

validate_profile_token() {
  local profile="$1"
  [[ "$profile" =~ ^[A-Za-z0-9._/-]+$ ]]
}

main() {
  local session_name="$SESSION_NAME_DEFAULT"
  local session_filename="$SESSION_FILE_NAME_DEFAULT"
  local profile="${RETROFX_PROFILE:-$PROFILE_DEFAULT}"
  local retrofx_home="${RETROFX_HOME:-$HOME/.config/retrofx}"
  local wrapper_path xsessions_dir out_file tmp_file exec_cmd

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
      --profile)
        [[ $# -ge 2 ]] || die "--profile requires a value"
        profile="$2"
        shift 2
        ;;
      --retrofx-home)
        [[ $# -ge 2 ]] || die "--retrofx-home requires a value"
        retrofx_home="$2"
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

  retrofx_home="$(trim "$retrofx_home")"
  [[ -n "$retrofx_home" ]] || die "retrofx home cannot be empty"

  if [[ "$profile" == "$PROFILE_DEFAULT" && -t 0 ]]; then
    local chosen
    read -r -p "Default profile [$profile]: " chosen || true
    chosen="$(trim "${chosen:-}")"
    if [[ -n "$chosen" ]]; then
      profile="$chosen"
    fi
  fi

  validate_profile_token "$profile" || die "profile contains unsupported characters"

  wrapper_path="$retrofx_home/scripts/integrate/i3-retro-session.sh"
  [[ -x "$wrapper_path" ]] || die "missing executable wrapper: $wrapper_path"

  xsessions_dir="${XDG_DATA_HOME:-$HOME/.local/share}/xsessions"
  out_file="$xsessions_dir/$session_filename"
  mkdir -p "$xsessions_dir"

  exec_cmd="env RETROFX_PROFILE=$profile $wrapper_path"
  tmp_file="$(mktemp "$xsessions_dir/.retrofx-xsession.XXXXXX")"
  {
    printf '# RetroFX-Managed: true\n'
    printf '[Desktop Entry]\n'
    printf 'Type=Application\n'
    printf 'Name=%s\n' "$session_name"
    printf 'Comment=RetroFX i3 session wrapper\n'
    printf 'Exec=%s\n' "$exec_cmd"
    printf 'TryExec=i3\n'
    printf 'DesktopNames=i3\n'
    printf '%s\n' "$MARKER_KEY"
    printf 'X-RetroFX-Profile=%s\n' "$profile"
    printf 'X-RetroFX-Home=%s\n' "$retrofx_home"
  } >"$tmp_file"

  mv "$tmp_file" "$out_file"
  printf 'install-xsession: wrote %s\n' "$out_file"
}

main "$@"
