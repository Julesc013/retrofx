# RetroFX 2.x Post-Alpha Decision Rules

This document defines what happens after a controlled internal alpha round.

It exists to prevent endless experimentation without branch decisions.

## Continue Alpha As-Is

Continue the current narrow internal alpha when:

- no `alpha-blocker` is open
- `high` issues are isolated to non-core flows or one environment
- diagnostics and feedback quality are good enough to reproduce issues
- docs still match the actual branch behavior

## Enter Alpha Remediation

Enter a focused remediation sprint when:

- any `alpha-blocker` appears
- multiple `high` issues cluster around apply, install, state, or diagnostics capture
- evidence shows current readiness docs are materially overstating reality

During remediation:

- stop expanding the tester set
- fix or fence off the affected surfaces
- add regression coverage for every resolved blocker

## Expand The Tester Set

Expand the internal tester cohort only when:

- no `alpha-blocker` remains
- `high` issues are down to a manageable, environment-specific minority
- at least one additional real host has passed the core checklist
- diagnostics and templates are being used consistently

## Prepare A Local Alpha Tag Candidate

Prepare a local or internal-only alpha candidate when:

- no `alpha-blocker` remains
- no open `high` remediation item remains
- the working tree can be made clean on the candidate commit
- the local package, install, diagnostics, and uninstall flow all pass together
- [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md) and [ALPHA_CANDIDATE_NOTES.md](ALPHA_CANDIDATE_NOTES.md) match the current branch truth

This still does not imply a public release.
It is only a disciplined local snapshot for continued internal use.

## Declare Readiness For Broader Alpha

Only consider broader alpha when:

- multi-host validation is materially better than the current single strong X11 host
- at least one real Wayland environment has completed the checklist successfully enough for current claims
- migration validation has expanded beyond the current representative subset
- the validation matrix and blocker docs have been refreshed with current evidence

## Freeze Features And Begin Pre-Release Stabilization

Begin a feature freeze toward a later pre-release milestone when:

- the branch has consistent multi-host evidence
- blocker churn is low
- docs and dev surface no longer need frequent truth corrections
- the remaining issues are mostly polish or platform-specific refinement

## Required Inputs For Any Decision

Before making a post-alpha branch decision, review:

- [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md)
- [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md)
- [ALPHA_REMEDIATION_BACKLOG.md](ALPHA_REMEDIATION_BACKLOG.md)
- [ALPHA_READINESS.md](ALPHA_READINESS.md)
- [ALPHA_TRIAGE.md](ALPHA_TRIAGE.md)
- [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md)
- the collected diagnostics directories from the current alpha round
