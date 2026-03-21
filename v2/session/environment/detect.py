"""Environment detection for the early 2.x session-planning scaffold."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys
from typing import Any, Callable, Mapping

REPO_ROOT = Path(__file__).resolve().parents[3]
FORCE_SESSION_TYPE_ENV = "RETROFX_V2_FORCE_SESSION_TYPE"
FORCE_WM_OR_DE_ENV = "RETROFX_V2_FORCE_WM_OR_DE"
FORCE_CONTEXT_CLASS_ENV = "RETROFX_V2_FORCE_CONTEXT_CLASS"
KNOWN_SESSION_TYPES = {"tty", "x11", "wayland", "remote-ssh", "unknown-headless"}
KNOWN_WM_OR_DE = {"i3", "sway", "gnome", "plasma", "unknown"}
KNOWN_CONTEXT_CLASSES = {"repo-local-dev", "installed"}


def detect_environment(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
) -> dict[str, Any]:
    env_map = {str(key): str(value) for key, value in (env or os.environ).items()}
    current_workdir = Path(cwd or os.getcwd()).resolve()
    stdin_tty = sys.stdin.isatty() if stdin_isatty is None else bool(stdin_isatty)
    lookup = path_lookup or shutil.which

    notes: list[str] = [
        "Environment detection is best-effort and uses local process context only.",
        "TWO-11 planning is dev-only and does not mutate the live session.",
    ]
    warnings: list[str] = []

    display = _clean(env_map.get("DISPLAY"))
    wayland_display = _clean(env_map.get("WAYLAND_DISPLAY"))
    term = _clean(env_map.get("TERM"))
    xdg_session_type = _lower_or_none(env_map.get("XDG_SESSION_TYPE"))
    current_desktop = " ".join(
        value
        for value in (
            _clean(env_map.get("XDG_CURRENT_DESKTOP")),
            _clean(env_map.get("DESKTOP_SESSION")),
        )
        if value
    ).lower()
    remote_ssh = any(_clean(env_map.get(key)) for key in ("SSH_CONNECTION", "SSH_TTY", "SSH_CLIENT"))

    forced_session = _normalize_forced(env_map.get(FORCE_SESSION_TYPE_ENV), KNOWN_SESSION_TYPES)
    forced_wm = _normalize_forced(env_map.get(FORCE_WM_OR_DE_ENV), KNOWN_WM_OR_DE)
    forced_context = _normalize_forced(env_map.get(FORCE_CONTEXT_CLASS_ENV), KNOWN_CONTEXT_CLASSES)

    if forced_session:
        session_type = forced_session
        notes.append(f"Session type was forced via `{FORCE_SESSION_TYPE_ENV}` for dev/test simulation.")
    else:
        session_type = _detect_session_type(
            xdg_session_type=xdg_session_type,
            display=display,
            wayland_display=wayland_display,
            remote_ssh=remote_ssh,
            term=term,
            stdin_isatty=stdin_tty,
            notes=notes,
        )

    if forced_wm:
        wm_or_de = forced_wm
        wm_detection = "forced"
        notes.append(f"WM or DE was forced via `{FORCE_WM_OR_DE_ENV}` for dev/test simulation.")
    else:
        wm_or_de, wm_detection = _detect_wm_or_de(env_map, current_desktop)

    if forced_context:
        context_class = forced_context
        notes.append(f"Execution context was forced via `{FORCE_CONTEXT_CLASS_ENV}` for dev/test simulation.")
    else:
        context_class = _detect_context_class(current_workdir)

    if display and wayland_display and session_type == "wayland":
        notes.append("`DISPLAY` is also present, so Xwayland-compatible terminal exports may still be meaningful.")

    if session_type == "unknown-headless":
        warnings.append("No trustworthy live session could be inferred; planning will stay conservative.")

    executables = {
        "picom": bool(lookup("picom")),
        "xrdb": bool(lookup("xrdb")),
        "i3-msg": bool(lookup("i3-msg")),
        "swaymsg": bool(lookup("swaymsg")),
        "waybar": bool(lookup("waybar")),
    }

    environment = {
        "session_type": session_type,
        "display_server": _display_server_for_session(session_type),
        "wm_or_de": wm_or_de,
        "wm_detection": wm_detection,
        "context_class": context_class,
        "installed_mode": context_class == "installed",
        "repo_root": str(REPO_ROOT),
        "cwd": str(current_workdir),
        "interactive_shell_context": {
            "stdin_isatty": stdin_tty,
            "term": term,
            "shell": _clean(env_map.get("SHELL")),
        },
        "signals": {
            "display": display,
            "wayland_display": wayland_display,
            "xdg_session_type": xdg_session_type,
            "xdg_current_desktop": _clean(env_map.get("XDG_CURRENT_DESKTOP")),
            "desktop_session": _clean(env_map.get("DESKTOP_SESSION")),
            "remote_ssh": remote_ssh,
        },
        "executables": executables,
        "capability_hints": {
            "terminal_outputs_meaningful": session_type in {"tty", "x11", "wayland", "remote-ssh"},
            "wm_outputs_meaningful": session_type in {"x11", "wayland"},
            "x11_render_path_environment": {
                "session_capable": session_type == "x11",
                "picom_available": executables["picom"],
                "implemented_now": False,
            },
        },
        "notes": notes,
        "warnings": warnings,
    }
    return environment


def _detect_session_type(
    *,
    xdg_session_type: str | None,
    display: str | None,
    wayland_display: str | None,
    remote_ssh: bool,
    term: str | None,
    stdin_isatty: bool,
    notes: list[str],
) -> str:
    if xdg_session_type == "wayland" or wayland_display:
        notes.append("Detected a Wayland session from `WAYLAND_DISPLAY` or `XDG_SESSION_TYPE`.")
        return "wayland"
    if xdg_session_type == "x11" or display:
        notes.append("Detected an X11 session from `DISPLAY` or `XDG_SESSION_TYPE`.")
        return "x11"
    if remote_ssh:
        notes.append("Detected a remote shell context from SSH environment variables.")
        return "remote-ssh"
    if stdin_isatty or _looks_like_tty(term):
        notes.append("Detected a TTY-like context from terminal signals without GUI session variables.")
        return "tty"
    return "unknown-headless"


def _detect_wm_or_de(env_map: Mapping[str, str], current_desktop: str) -> tuple[str, str]:
    if _clean(env_map.get("SWAYSOCK")) or "sway" in current_desktop:
        return "sway", "high"
    if _clean(env_map.get("I3SOCK")) or "i3" in current_desktop:
        return "i3", "high"
    if _clean(env_map.get("GNOME_DESKTOP_SESSION_ID")) or "gnome" in current_desktop:
        return "gnome", "medium"
    if _clean(env_map.get("KDE_FULL_SESSION")) or "plasma" in current_desktop or "kde" in current_desktop:
        return "plasma", "medium"
    return "unknown", "low"


def _detect_context_class(current_workdir: Path) -> str:
    try:
        current_workdir.relative_to(REPO_ROOT)
    except ValueError:
        return "installed"
    return "repo-local-dev" if (REPO_ROOT / ".git").exists() else "installed"


def _display_server_for_session(session_type: str) -> str:
    if session_type in {"x11", "wayland"}:
        return session_type
    return "none"


def _normalize_forced(value: str | None, allowed: set[str]) -> str | None:
    normalized = _lower_or_none(value)
    if normalized in allowed:
        return normalized
    return None


def _looks_like_tty(term: str | None) -> bool:
    if not term:
        return False
    normalized = term.strip().lower()
    return normalized not in {"", "dumb", "unknown"}


def _lower_or_none(value: str | None) -> str | None:
    cleaned = _clean(value)
    if cleaned is None:
        return None
    return cleaned.lower()


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = str(value).strip()
    return stripped or None
