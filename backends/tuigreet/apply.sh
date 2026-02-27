#!/usr/bin/env bash
set -euo pipefail

ACTIVE_DIR="${2:-${1:-}}"

printf 'tuigreet backend: scaffold only in Phase 1 (no system changes made).\n'
if [[ -n "$ACTIVE_DIR" ]]; then
  printf 'tuigreet backend: generated resources remain in %s\n' "$ACTIVE_DIR"
fi
printf 'tuigreet backend: planned in Phase 2 (theme integration hooks).\n'
