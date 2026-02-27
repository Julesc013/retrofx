#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_SCRIPT="$SCRIPT_DIR/install-xsession.sh"

usage() {
  cat <<'USAGE'
Usage (compat wrapper):
  scripts/integrate/generate-xsession.sh [args...]

Forwards to:
  scripts/integrate/install-xsession.sh
USAGE
}

die() {
  printf 'generate-xsession: error: %s\n' "$*" >&2
  exit 1
}

main() {
  if [[ $# -gt 0 ]]; then
    case "$1" in
      -h | --help | help)
        usage
        return 0
        ;;
    esac
  fi

  [[ -x "$INSTALL_SCRIPT" ]] || die "missing install helper: $INSTALL_SCRIPT"
  exec "$INSTALL_SCRIPT" "$@"
}

main "$@"
