# RetroFX 2.x Pre-Beta Candidate Summary

This is the concise operator summary for the currently blocked non-public pre-beta candidate.

It is not a release note.
It does not mean a pre-beta candidate exists today.

## Candidate

- proposed candidate version: `2.0.0-prebeta.internal.1`
- proposed status label: `pre-beta`
- proposed local tag candidate: `v2.0.0-prebeta.internal.1`
- current branch version: `2.0.0-alpha.internal.2`
- current branch status label: `internal-alpha`
- readiness verdict: `PRE_BETA_CANDIDATE_READY=no`

## Why It Is Blocked

- broader-alpha gates are still not satisfied
- there is still no real Wayland-host validation pass
- package, install, and diagnostics flows remain intentionally internal-only and repo-checkout dependent
- migration validation breadth is still too narrow for pre-beta positioning

## What Exists Instead

- a reproducible internal-alpha package under `v2/releases/internal-alpha/`
- bounded apply/off, package, install, uninstall, diagnostics, and status flows for internal testers
- explicit pre-beta notes and checklist documents for future use

## Next Human Steps

1. Keep the branch on the internal-alpha line.
2. Expand real-host validation breadth, especially one real Wayland host.
3. Re-run the broader-alpha and pre-beta matrices after that evidence exists.
4. Revisit the pre-beta candidate only after the broader-alpha gate is approved.
