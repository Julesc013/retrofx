#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"

log() {
  printf '[ci] %s\n' "$*"
}

warn() {
  printf '[ci][warn] %s\n' "$*" >&2
}

die() {
  printf '[ci][error] %s\n' "$*" >&2
  exit 1
}

collect_script_files() {
  {
    printf '%s\n' "$ROOT_DIR/scripts/retrofx"
    find "$ROOT_DIR/scripts" -type f -name '*.sh' | sort
    find "$ROOT_DIR/backends" -type f -name '*.sh' | sort
  } | awk '!seen[$0]++'
}

run_format_checks() {
  local fail=0
  local file

  while IFS= read -r file; do
    [[ -f "$file" ]] || continue

    if grep -q $'\r' "$file"; then
      warn "CRLF detected: $file"
      fail=1
    fi

    if [[ ! -x "$file" ]]; then
      warn "expected executable bit on script: $file"
      fail=1
    fi
  done < <(collect_script_files)

  if [[ "$fail" -ne 0 ]]; then
    die "format/executable checks failed"
  fi
}

run_shellcheck_if_available() {
  local -a files=()
  local file

  while IFS= read -r file; do
    files+=("$file")
  done < <(collect_script_files)

  if command -v shellcheck >/dev/null 2>&1; then
    log "running shellcheck"
    shellcheck "${files[@]}"
  else
    warn "shellcheck not installed; skipping"
  fi
}

main() {
  log "running regression tests"
  "$ROOT_DIR/scripts/test.sh"

  run_shellcheck_if_available

  log "running LF/executable checks"
  run_format_checks

  log "ci checks passed"
}

main "$@"
