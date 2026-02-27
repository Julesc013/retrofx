#!/usr/bin/env bash
set -euo pipefail

cat <<'ENVVARS'
# Optional Wayland toolkit theme hooks.
# This script only prints suggestions; it does not modify system settings.
# Example:
#   eval "$(/path/to/repo/scripts/integrate/wayland-env.sh)"

export GTK_THEME='Adwaita:dark'
export QT_STYLE_OVERRIDE='Fusion'
export QT_QPA_PLATFORMTHEME='gtk3'
ENVVARS
