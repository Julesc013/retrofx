#!/usr/bin/env bash
set -euo pipefail

SESSION_FILE_NAME_DEFAULT="retrofx-i3.desktop"
MARKER_KEY="X-RetroFX-Managed=true"

usage() {
  cat <<'USAGE'
Usage:
  scripts/integrate/remove-xsession.sh [--yes] [--filename retrofx-i3.desktop] [--all-managed]

Removes RetroFX-managed Xsession entries from:
  ~/.local/share/xsessions/
USAGE
}

die() {
  printf 'remove-xsession: error: %s\n' "$*" >&2
  exit 1
}

confirm_or_die() {
  local question="$1"
  local auto_yes="$2"
  local answer=""

  if [[ "$auto_yes" == "true" ]]; then
    return 0
  fi

  if [[ ! -t 0 ]]; then
    die "$question (use --yes in non-interactive mode)"
  fi

  read -r -p "$question [y/N]: " answer || die "aborted"
  case "$answer" in
    y | Y | yes | YES)
      return 0
      ;;
    *)
      die "aborted"
      ;;
  esac
}

is_managed_entry() {
  local file="$1"
  [[ -f "$file" ]] || return 1
  grep -Fxq "$MARKER_KEY" "$file" || grep -Fq '# RetroFX-Managed: true' "$file"
}

main() {
  local auto_yes="false"
  local all_managed="false"
  local filename="$SESSION_FILE_NAME_DEFAULT"
  local xsessions_dir target_file removed=0
  local file

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --yes)
        auto_yes="true"
        shift
        ;;
      --all-managed)
        all_managed="true"
        shift
        ;;
      --filename)
        [[ $# -ge 2 ]] || die "--filename requires a value"
        filename="$2"
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

  xsessions_dir="${XDG_DATA_HOME:-$HOME/.local/share}/xsessions"
  [[ -d "$xsessions_dir" ]] || {
    printf 'remove-xsession: no xsessions directory at %s\n' "$xsessions_dir"
    return 0
  }

  if [[ "$all_managed" == "true" ]]; then
    confirm_or_die "Remove all RetroFX-managed xsession entries from $xsessions_dir?" "$auto_yes"
    while IFS= read -r file; do
      if is_managed_entry "$file"; then
        rm -f "$file"
        removed=$((removed + 1))
      fi
    done < <(find "$xsessions_dir" -mindepth 1 -maxdepth 1 -type f -name '*.desktop' | sort)
    printf 'remove-xsession: removed %d managed entries\n' "$removed"
    return 0
  fi

  target_file="$xsessions_dir/$filename"
  [[ -f "$target_file" ]] || {
    printf 'remove-xsession: no xsession file at %s\n' "$target_file"
    return 0
  }

  is_managed_entry "$target_file" || die "refusing to remove unmanaged file: $target_file"
  confirm_or_die "Remove RetroFX xsession file $target_file?" "$auto_yes"
  rm -f "$target_file"
  printf 'remove-xsession: removed %s\n' "$target_file"
}

main "$@"
