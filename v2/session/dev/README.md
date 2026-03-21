# v2/session/dev

Purpose:

- home of explicit dev-only session preview helpers that sit above target compilation but below any future production apply layer

Implemented now:

- `preview_x11_render.py` and the `scripts/dev/retrofx-v2-preview-x11` wrapper for bounded X11 render artifact staging and optional short-lived `picom` probing

What does not belong here:

- replacements for the 1.x runtime
- hidden default apply paths
- global desktop/session mutation

Current rule:

- every command here must stay explicit, experimental, and reversible
- any live action must be local to the current session and must not touch 1.x state or install paths
