#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
FONTCONFIG_PATH="$ROOT_DIR/active/fontconfig.conf"
CURRENT_MANIFEST="$ROOT_DIR/state/manifests/current.manifest"
FONTCONFIG_CLASS=""

current_manifest_artifact_class() {
  local rel="$1"
  local class

  [[ -f "$CURRENT_MANIFEST" ]] || return 1

  for class in REQUIRED_RUNTIME OPTIONAL_RUNTIME EXPORT_ONLY EPHEMERAL_RUNTIME IGNORED_LOG_OR_CACHE INSTALL_ASSET; do
    if grep -Fqx "artifact=$class|$rel" "$CURRENT_MANIFEST"; then
      printf '%s' "$class"
      return 0
    fi
  done

  if grep -Fqx 'manifest_version=1' "$CURRENT_MANIFEST" &&
    [[ "$rel" == "fontconfig.conf" ]] &&
    grep -Fqx 'required_file=fontconfig.conf' "$CURRENT_MANIFEST"; then
    printf 'REQUIRED_RUNTIME'
    return 0
  fi

  return 1
}

FONTCONFIG_CLASS="$(current_manifest_artifact_class "fontconfig.conf" 2>/dev/null || true)"

cat <<ENVVARS
# RetroFX session-local font hook.
# This script prints shell commands; use:
#   eval "\$($0)"

if [[ "$FONTCONFIG_CLASS" == "REQUIRED_RUNTIME" && -f "$FONTCONFIG_PATH" ]]; then
  export FONTCONFIG_FILE="$FONTCONFIG_PATH"
else
  if [[ "$FONTCONFIG_CLASS" == "REQUIRED_RUNTIME" ]]; then
    printf '# RetroFX manifest requires active/fontconfig.conf, but the file is missing.\n' >&2
  fi
  unset FONTCONFIG_FILE
fi
ENVVARS
