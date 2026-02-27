#!/usr/bin/env bash
set -euo pipefail

cat <<'ENVVARS'
# Optional X11 toolkit theme hooks.
# This script only prints suggestions; it does not modify system settings.
# Example:
#   eval "$(/path/to/repo/scripts/integrate/x11-env.sh)"

export GTK_THEME='Adwaita:dark'
export QT_STYLE_OVERRIDE='Fusion'
export QT_QPA_PLATFORMTHEME='gtk3'
ENVVARS
