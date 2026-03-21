# RetroFX 2.x Local Alpha Release Checklist

Use this only for a local or internal alpha-candidate snapshot.
It is not a public release checklist.

## Candidate Preconditions

- [ ] `READY_FOR_INTERNAL_ALPHA_CONTINUATION = yes`
- [ ] `READY_FOR_LOCAL_ALPHA_TAG_CANDIDATE = yes`
- [ ] no open `alpha-blocker` items remain in [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md)
- [ ] no unresolved `high` items remain in [ALPHA_REMEDIATION_BACKLOG.md](ALPHA_REMEDIATION_BACKLOG.md)

## Tree And Test State

- [ ] working tree is clean before cutting the local candidate
- [ ] `./v2/tests/test.sh` is green
- [ ] `scripts/dev/retrofx-v2 status` is green and reports the expected internal-alpha metadata

## Required Workflow Checks

- [ ] `scripts/dev/retrofx-v2 package-alpha ...` succeeds
- [ ] package manifest shows the expected version, status label, and source-control summary
- [ ] temp-HOME `install` succeeds
- [ ] temp-HOME `diagnostics` succeeds and captures source-control plus installed bundle evidence
- [ ] temp-HOME `uninstall` succeeds

## Documentation Truth

- [ ] [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) reflects the latest remediation evidence
- [ ] [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md) reflects current open risks only
- [ ] [ALPHA_READINESS.md](ALPHA_READINESS.md) reflects the current verdict
- [ ] [ALPHA_CANDIDATE_NOTES.md](ALPHA_CANDIDATE_NOTES.md) still matches the branch truth

## Candidate Discipline

- [ ] any local tag remains unpushed and non-public
- [ ] 1.x is still described as the production line
- [ ] broader-testing or public-ready claims are not made
