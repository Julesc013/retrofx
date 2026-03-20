#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)"
RETROFX="$ROOT_DIR/scripts/retrofx"
PROFILES_DIR="$ROOT_DIR/profiles"
PROFILES_PACKS_DIR="$PROFILES_DIR/packs"
ACTIVE_DIR="$ROOT_DIR/active"
CURRENT_MANIFEST="$ROOT_DIR/state/manifests/current.manifest"
RETROFX_ENV_HELPER="$ROOT_DIR/scripts/integrate/retrofx-env.sh"

readonly DEFAULT_PRIMARY_PROFILE="crt-green-p1-4band"
readonly DEFAULT_FALLBACK_PROFILE="passthrough"

log() {
  printf 'i3-retro-session: %s\n' "$*"
}

warn() {
  printf 'i3-retro-session: warning: %s\n' "$*" >&2
}

profile_exists() {
  local ref="$1"
  [[ -f "$PROFILES_DIR/$ref.toml" || -f "$PROFILES_DIR/$ref" || -f "$ref" ]] && return 0
  [[ -f "$PROFILES_PACKS_DIR/$ref.toml" || -f "$PROFILES_PACKS_DIR/$ref" ]] && return 0
  if [[ -d "$PROFILES_PACKS_DIR" ]]; then
    find "$PROFILES_PACKS_DIR" -type f -name '*.toml' -printf '%f\n' 2>/dev/null | sed 's/\.toml$//' | grep -Fxq "$ref" && return 0
  fi
  return 1
}

current_manifest_artifact_class() {
  local rel="$1"
  local class session_type compositor_required

  [[ -f "$CURRENT_MANIFEST" ]] || return 1

  for class in REQUIRED_RUNTIME OPTIONAL_RUNTIME EXPORT_ONLY EPHEMERAL_RUNTIME IGNORED_LOG_OR_CACHE INSTALL_ASSET; do
    if grep -Fqx "artifact=$class|$rel" "$CURRENT_MANIFEST"; then
      printf '%s' "$class"
      return 0
    fi
  done

  if grep -Fqx 'manifest_version=1' "$CURRENT_MANIFEST"; then
    session_type="$(grep '^session_type=' "$CURRENT_MANIFEST" | head -n1 | cut -d= -f2 || true)"
    compositor_required="$(grep '^compositor_required=' "$CURRENT_MANIFEST" | head -n1 | cut -d= -f2 || true)"
    case "$rel" in
      picom.conf | shader.glsl)
        [[ "$session_type" == "wayland" ]] && return 1
        if [[ "$compositor_required" == "true" ]]; then
          printf 'REQUIRED_RUNTIME'
        else
          printf 'OPTIONAL_RUNTIME'
        fi
        return 0
        ;;
      fontconfig.conf)
        if grep -Fqx 'required_file=fontconfig.conf' "$CURRENT_MANIFEST"; then
          printf 'REQUIRED_RUNTIME'
          return 0
        fi
        ;;
    esac
  fi

  return 1
}

current_artifact_is_required_runtime() {
  local rel="$1"
  [[ "$(current_manifest_artifact_class "$rel" 2>/dev/null || true)" == "REQUIRED_RUNTIME" ]]
}

pick_profile() {
  local requested="${1:-}"
  local first_profile

  if [[ -n "$requested" ]]; then
    printf '%s' "$requested"
    return 0
  fi

  if [[ -n "${RETROFX_PROFILE:-}" ]]; then
    printf '%s' "$RETROFX_PROFILE"
    return 0
  fi

  if profile_exists "$DEFAULT_PRIMARY_PROFILE"; then
    printf '%s' "$DEFAULT_PRIMARY_PROFILE"
    return 0
  fi

  if profile_exists "$DEFAULT_FALLBACK_PROFILE"; then
    printf '%s' "$DEFAULT_FALLBACK_PROFILE"
    return 0
  fi

  first_profile="$(find "$PROFILES_DIR" -mindepth 1 -maxdepth 1 -name '*.toml' -printf '%f\n' 2>/dev/null | sort | head -n1 || true)"
  if [[ -n "$first_profile" ]]; then
    printf '%s' "${first_profile%.toml}"
    return 0
  fi

  printf 'passthrough'
}

start_picom_if_possible() {
  if [[ -z "${DISPLAY:-}" ]]; then
    warn "DISPLAY is not set; skipping picom launch"
    return 0
  fi

  if ! current_artifact_is_required_runtime "picom.conf"; then
    log "current artifact contract does not require picom; skipping compositor launch"
    return 0
  fi

  if [[ ! -f "$ACTIVE_DIR/picom.conf" ]]; then
    warn "artifact contract requires active/picom.conf but the file is missing; skipping picom launch"
    return 0
  fi

  if ! command -v picom >/dev/null 2>&1; then
    warn "picom not installed; continuing without compositor"
    return 0
  fi

  if command -v pgrep >/dev/null 2>&1 && pgrep -x picom >/dev/null 2>&1; then
    log "picom is already running; not launching another instance"
    return 0
  fi

  (
    cd "$ACTIVE_DIR"
    nohup picom --config picom.conf >/dev/null 2>&1 &
  ) || warn "failed to launch picom; continuing with plain i3 session"
}

main() {
  local requested_profile="${1:-}"
  local profile=""
  local apply_ok=0

  if [[ $# -gt 0 ]]; then
    shift
  fi

  profile="$(pick_profile "$requested_profile")"

  if [[ ! -x "$RETROFX" ]]; then
    warn "retrofx script is missing or not executable at $RETROFX"
  else
    if "$RETROFX" apply "$profile"; then
      apply_ok=1
      log "applied profile '$profile'"
    else
      warn "profile apply failed for '$profile'; starting i3 without RetroFX compositor settings"
    fi
  fi

  if [[ "$apply_ok" -eq 1 ]]; then
    if [[ -x "$RETROFX_ENV_HELPER" ]]; then
      eval "$("$RETROFX_ENV_HELPER")" || warn "failed to apply retrofx font environment helper"
    fi
    start_picom_if_possible
  fi

  exec i3 "$@"
}

main "$@"
