#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
FONTCONFIG_PATH="$ROOT_DIR/active/fontconfig.conf"

cat <<ENVVARS
# RetroFX session-local font hook.
# This script prints shell commands; use:
#   eval "\$($0)"

if [[ -f "$FONTCONFIG_PATH" ]]; then
  export FONTCONFIG_FILE="$FONTCONFIG_PATH"
else
  unset FONTCONFIG_FILE
fi
ENVVARS
