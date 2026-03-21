# RetroFX 2.x Technical Beta Release Checklist

This checklist is for local candidate preparation only.
It does not publish anything automatically.

## Preflight

- branch is clean
- `./v2/tests/test.sh` passes
- [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md) is current
- [PUBLIC_BETA_BLOCKERS.md](PUBLIC_BETA_BLOCKERS.md) has no open `public-beta-blocker`

## Validation

- `scripts/dev/retrofx-v2-techbeta --help` works
- `scripts/dev/retrofx-v2-techbeta status` works
- representative `resolve`, `plan`, and `compile` path works
- representative bounded `apply` and `off` path works on X11
- representative Wayland degraded-path scenario reports honestly
- candidate package flow works
- temp-HOME `install`, `diagnostics`, and `uninstall` work
- toolkit and X11 outputs were inspected as artifacts, not overclaimed as live ownership

## Candidate Artifact Generation

- technical-beta package generated under the configured release root
- version and status metadata included
- copied-toolchain wrapper included
- package manifest included
- notes, checklist, and readiness docs included

## Decision

- if blockers remain, do not create the candidate tag
- if validation is clean, local candidate tag preparation may proceed
