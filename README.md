# RetroFX

RetroFX is a profile-driven retro rendering and theming tool for Linux sessions.

This repository now carries two distinct tracks on `main`:

- `1.x`: the production line, currently `1.0.0`
- `2.x`: the experimental redesign line under [`v2/`](v2/README.md) and [`docs/v2/`](docs/v2/README.md)

`1.x` remains the shipping product.
`2.x` remains explicitly experimental, even though it now has real compilers, bounded apply/off, packages, diagnostics, and a narrow limited-technical-beta surface for advanced testers.

## Current Repository Position

### 1.x

RetroFX `1.0.0` is stable for its documented support matrix:

- supported X11 + `picom` + GLX runtime path
- deterministic terminal/theme exports
- scoped TTY and `tuigreet` outputs
- user-local install mode
- explicit recovery tooling (`self-check`, `repair`, `state/last_good/`)

### 2.x

RetroFX `2.x` is a separate implementation track that now includes:

- schema validation, normalization, and resolved-profile scaffolding
- terminal, WM, toolkit, display-policy, and bounded X11 render compilers
- pack-aware resolution and 1.x migration inspection
- bounded experimental apply/off
- bundle/install/uninstall flows
- diagnostics capture
- a narrower `technical-beta` wrapper for advanced testers

Current 2.x planning truth:

- limited public technical beta: yes, through the narrower `retrofx-v2-techbeta` surface only
- broader beta stabilization: no
- another fast remediation cycle before broader beta stabilization: yes
- 1.x replacement: no

The broader `scripts/dev/retrofx-v2` surface remains internal-only.

See [docs/PLANNING_HANDOFF_2026-03-22.md](docs/PLANNING_HANDOFF_2026-03-22.md) for the current repo-wide planning brief.

## 1.x Support Matrix

| Target / Environment | Status | Notes |
| --- | --- | --- |
| X11 + picom + GLX | Supported | Full shader/runtime path. Best-supported session flow is i3 + the RetroFX wrapper. |
| Other X11 sessions | Degraded | Core apply/export logic works, but session integration is more manual and less documented. |
| Wayland sessions | Degraded | No global shader/compositor path. Palette and session-local outputs only. |
| TTY palette backend | Supported | Optional 16-color backend. Real apply requires a compatible console. |
| `tuigreet` snippet generation | Supported | Generates `active/tuigreet.conf`; global greetd edits stay manual. |
| Base16 import/export | Supported | Deterministic, lossy ANSI16 bridge. |
| Broad DE orchestration / global Wayland shaders | Unsupported | Out of scope for 1.x. |

## Use The Right CLI

### Stable 1.x CLI

Use this for the production line:

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx status
./scripts/retrofx off
```

### Internal 2.x Developer Surface

Use this only for the broader experimental platform:

```bash
./scripts/dev/retrofx-v2 status
./scripts/dev/retrofx-v2 smoke v2/tests/fixtures/strict-green-crt.toml
./scripts/dev/retrofx-v2 smoke --pack modern-minimal --profile-id warm-night
```

### Narrow 2.x Technical-Beta Surface

Use this for the copied-toolchain advanced-tester flow:

```bash
./scripts/dev/retrofx-v2-techbeta status
./scripts/dev/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night
```

## Safety And Recovery

### 1.x

- `apply` is atomic and keeps `state/last_good/` as the rollback snapshot.
- `self-check` validates the active state against the artifact contract in `state/manifests/`.
- `repair` restores a manifest-valid `last_good` snapshot or falls back conservatively.
- user-local install mode lives under `~/.config/retrofx`; RetroFX does not edit `/etc` by default.

### 2.x

- current apply/off behavior is bounded to the isolated `retrofx-v2-dev` footprint
- cleanup is intentionally limited to 2.x-owned paths
- live runtime support remains intentionally narrow
- `1.x` is not mutated by 2.x experimental flows

## Documentation

Start with the documentation index:

- [Documentation Index](docs/README.md)

Stable-line docs:

- [1.x Product Truth](docs/1x_PRODUCT.md)
- [1.x Maintenance](docs/1x_MAINTENANCE.md)
- [Install Guide](docs/INSTALL.md)
- [Testing](docs/TESTING.md)
- [Roadmap](docs/ROADMAP.md)

Experimental-line docs:

- [2.x Docs Index](docs/v2/README.md)
- [2.x Implemented Status](docs/v2/IMPLEMENTED_STATUS.md)
- [2.x Experimental Status](docs/v2/EXPERIMENTAL_STATUS.md)
- [2.x Technical Beta Readiness](docs/v2/TECHNICAL_BETA_READINESS.md)
- [2.x Current Execution Baseline](docs/v2/CURRENT_EXECUTION_BASELINE.md)
- [2.x Public Beta Readiness](docs/v2/PUBLIC_BETA_READINESS.md)
- [2.x Next Stage Verdict](docs/v2/NEXT_STAGE_VERDICT.md)

Planning:

- [Planning Handoff](docs/PLANNING_HANDOFF_2026-03-22.md)

## Development

Stable-line checks:

```bash
./scripts/test.sh
./scripts/ci.sh
```

2.x checks:

```bash
./v2/tests/test.sh
```

If `shellcheck` is not installed, the 1.x shell checks still run with a warning.

## License

See profile metadata for per-profile authorship/license notes where provided.
