# RetroFX 2.x Alpha Environment Report Template

Fill out one environment report per host or test environment.

## Branch And Build

- branch:
- commit:
- release version:
- status label:
- package or mode used:
  repo-local / internal-alpha package / installed dev footprint

## Host Environment

- session type:
  X11 / Wayland / TTY / headless
- WM or DE:
- distro:
- kernel:
- GPU:
- driver stack:
- terminal:

## 2.x Execution Context

- temp HOME used:
  yes / no
- XDG roots isolated:
  yes / no
- package installed:
  yes / no
- active 2.x state before testing:
  yes / no

## Commands Run

List the actual commands used:

```text
scripts/dev/retrofx-v2 status
scripts/dev/retrofx-v2 plan ...
scripts/dev/retrofx-v2 diagnostics ...
```

## Observed Capability Summary

- planning result:
- degraded targets:
- live-eligible targets:
- toolkit status:
- X11 render status:

## Diagnostics

- diagnostics directory path:
- current-state manifest path if active:
- install-state path:
- relevant `v2/out/` or package path:

## Notes

- anything environment-specific that may affect reproduction:
