#!/usr/bin/env bash

retrofx_runtime_trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

retrofx_runtime_reset() {
  RETROFX_RUNTIME_META_FILE=""
  RETROFX_RUNTIME_PROFILE_REF=""
  RETROFX_RUNTIME_SESSION_TYPE=""
  RETROFX_RUNTIME_X11_RUNTIME_ENABLED=""
  RETROFX_RUNTIME_COMPOSITOR_REQUIRED=""
  RETROFX_RUNTIME_SHADER_REQUIRED=""
  RETROFX_RUNTIME_DEGRADED=""
  RETROFX_RUNTIME_SCOPE_X11=""
  RETROFX_RUNTIME_SCOPE_TTY=""
  RETROFX_RUNTIME_SCOPE_TUIGREET=""
  RETROFX_RUNTIME_BLUR_ENABLED=""
  RETROFX_RUNTIME_METADATA_ERROR=""
}

retrofx_runtime_bool_valid() {
  case "$1" in
    true | false)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

retrofx_runtime_load_metadata() {
  local meta_path="$1"
  local line="" key="" value=""
  local saw_profile=0
  local saw_session=0
  local saw_compositor=0

  retrofx_runtime_reset
  RETROFX_RUNTIME_META_FILE="$meta_path"

  if [[ ! -f "$meta_path" ]]; then
    RETROFX_RUNTIME_METADATA_ERROR="missing runtime metadata: $meta_path"
    return 1
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    line="$(retrofx_runtime_trim "$line")"
    [[ -z "$line" || "$line" == \#* ]] && continue

    if [[ "$line" != *=* ]]; then
      RETROFX_RUNTIME_METADATA_ERROR="invalid runtime metadata line: $line"
      return 1
    fi

    key="${line%%=*}"
    value="${line#*=}"
    key="$(retrofx_runtime_trim "$key")"
    value="$(retrofx_runtime_trim "$value")"

    case "$key" in
      profile | profile_id)
        [[ -n "$value" ]] || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field '$key' is empty"
          return 1
        }
        RETROFX_RUNTIME_PROFILE_REF="$value"
        saw_profile=1
        ;;
      session_type)
        case "$value" in
          x11 | wayland | unknown)
            ;;
          *)
            RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'session_type' is invalid: $value"
            return 1
            ;;
        esac
        RETROFX_RUNTIME_SESSION_TYPE="$value"
        saw_session=1
        ;;
      x11_runtime_enabled)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'x11_runtime_enabled' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_X11_RUNTIME_ENABLED="$value"
        ;;
      compositor_required)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'compositor_required' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_COMPOSITOR_REQUIRED="$value"
        saw_compositor=1
        ;;
      shader_required)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'shader_required' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_SHADER_REQUIRED="$value"
        ;;
      degraded)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'degraded' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_DEGRADED="$value"
        ;;
      scope_x11)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'scope_x11' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_SCOPE_X11="$value"
        ;;
      scope_tty)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'scope_tty' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_SCOPE_TTY="$value"
        ;;
      scope_tuigreet)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'scope_tuigreet' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_SCOPE_TUIGREET="$value"
        ;;
      blur_enabled)
        retrofx_runtime_bool_valid "$value" || {
          RETROFX_RUNTIME_METADATA_ERROR="runtime metadata field 'blur_enabled' is invalid: $value"
          return 1
        }
        RETROFX_RUNTIME_BLUR_ENABLED="$value"
        ;;
      apply_input_hash)
        ;;
      *)
        ;;
    esac
  done <"$meta_path"

  [[ "$saw_profile" -eq 1 ]] || {
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata is missing profile identity"
    return 1
  }
  [[ "$saw_session" -eq 1 ]] || {
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata is missing session_type"
    return 1
  }
  [[ "$saw_compositor" -eq 1 ]] || {
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata is missing compositor_required"
    return 1
  }

  if [[ -z "$RETROFX_RUNTIME_SHADER_REQUIRED" ]]; then
    if [[ "$RETROFX_RUNTIME_SESSION_TYPE" == "wayland" ]]; then
      RETROFX_RUNTIME_SHADER_REQUIRED="false"
    else
      RETROFX_RUNTIME_SHADER_REQUIRED="$RETROFX_RUNTIME_COMPOSITOR_REQUIRED"
    fi
  fi

  if [[ -z "$RETROFX_RUNTIME_DEGRADED" ]]; then
    RETROFX_RUNTIME_DEGRADED="false"
  fi

  if [[ -z "$RETROFX_RUNTIME_X11_RUNTIME_ENABLED" ]]; then
    if [[ "$RETROFX_RUNTIME_SESSION_TYPE" != "wayland" ]] &&
      ([[ "${RETROFX_RUNTIME_SCOPE_X11:-false}" == "true" ]] ||
        [[ "${RETROFX_RUNTIME_COMPOSITOR_REQUIRED:-false}" == "true" ]] ||
        [[ "${RETROFX_RUNTIME_SHADER_REQUIRED:-false}" == "true" ]]); then
      RETROFX_RUNTIME_X11_RUNTIME_ENABLED="true"
    else
      RETROFX_RUNTIME_X11_RUNTIME_ENABLED="false"
    fi
  fi

  if [[ "$RETROFX_RUNTIME_SESSION_TYPE" == "wayland" && "$RETROFX_RUNTIME_COMPOSITOR_REQUIRED" == "true" ]]; then
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata cannot require a compositor for wayland active state"
    return 1
  fi

  if [[ "$RETROFX_RUNTIME_COMPOSITOR_REQUIRED" == "true" && "$RETROFX_RUNTIME_X11_RUNTIME_ENABLED" != "true" ]]; then
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata cannot require a compositor when x11_runtime_enabled=false"
    return 1
  fi

  if [[ "$RETROFX_RUNTIME_SHADER_REQUIRED" == "true" && "$RETROFX_RUNTIME_COMPOSITOR_REQUIRED" != "true" ]]; then
    RETROFX_RUNTIME_METADATA_ERROR="runtime metadata cannot require shader output without compositor_required=true"
    return 1
  fi

  return 0
}

retrofx_runtime_load_active_metadata() {
  local root_dir="${1:-.}"
  retrofx_runtime_load_metadata "$root_dir/active/meta"
}

retrofx_runtime_current_requires_compositor() {
  local root_dir="${1:-}"

  if [[ -n "$root_dir" ]]; then
    retrofx_runtime_load_active_metadata "$root_dir" || return 1
  fi

  [[ "${RETROFX_RUNTIME_COMPOSITOR_REQUIRED:-false}" == "true" ]]
}

retrofx_runtime_current_enables_x11_runtime() {
  local root_dir="${1:-}"

  if [[ -n "$root_dir" ]]; then
    retrofx_runtime_load_active_metadata "$root_dir" || return 1
  fi

  [[ "${RETROFX_RUNTIME_X11_RUNTIME_ENABLED:-false}" == "true" ]]
}

retrofx_runtime_active_is_degraded() {
  local root_dir="${1:-}"

  if [[ -n "$root_dir" ]]; then
    retrofx_runtime_load_active_metadata "$root_dir" || return 1
  fi

  [[ "${RETROFX_RUNTIME_DEGRADED:-false}" == "true" ]]
}
