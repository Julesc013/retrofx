# RetroFX 2.x Pre-Beta Release Checklist

This checklist is for deciding whether a non-public pre-beta candidate can exist.

For TWO-30, the expected result is still "do not create the candidate."

## Preflight

- branch is clean
- `./v2/tests/test.sh` passes
- [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md) is current
- [PRE_BETA_BLOCKERS.md](PRE_BETA_BLOCKERS.md) has been reviewed
- [PRE_BETA_READINESS.md](PRE_BETA_READINESS.md) still reflects the actual branch state

## Validation

- `scripts/dev/retrofx-v2 --help` works
- `scripts/dev/retrofx-v2 status` works and reports truthful release metadata
- one representative resolve or plan or compile path works
- one representative bounded apply or off path works
- `scripts/dev/retrofx-v2 package-alpha ...` works on a clean tree
- temp-HOME install or uninstall works if that flow is being validated
- diagnostics capture works and includes release-status plus install-state evidence
- X11 preview or probe is tested only where a supported X11 host actually exists
- toolkit-export outputs are inspected as advisory artifacts rather than live desktop ownership

## Candidate Artifact Generation

- if and only if the gates are satisfied, a non-public pre-beta candidate package may be created
- candidate metadata must include version, status, manifest, notes, and checklist references
- candidate metadata must not imply public beta or replacement of 1.x

## Decision Rules

- if any `pre-beta-blocker` remains open, do not create a pre-beta candidate
- if broader alpha is still not approved, do not create a pre-beta candidate
- if there is still no real Wayland-host validation pass, do not create a pre-beta candidate
- if the current build is still positioned as `internal-alpha`, do not create a local pre-beta tag
- if the branch is still only suitable for continued internal hardening, keep using the internal-alpha validation package flow instead
