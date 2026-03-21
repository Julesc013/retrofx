# RetroFX 2.x Local Alpha Release Checklist

Use this only for a local or internal alpha-candidate snapshot.
It is not a public release checklist.

## Preflight

- [ ] `READY_FOR_INTERNAL_ALPHA_CONTINUATION = yes`
- [ ] `READY_FOR_LOCAL_ALPHA_TAG_CANDIDATE = yes`
- [ ] `ALPHA_CANDIDATE_READY = yes`
- [ ] no open `alpha-blocker` items remain in [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md)
- [ ] no unresolved `high` items remain in [ALPHA_REMEDIATION_BACKLOG.md](ALPHA_REMEDIATION_BACKLOG.md)
- [ ] working tree is clean before cutting the local candidate
- [ ] `./v2/tests/test.sh` is green
- [ ] `scripts/dev/retrofx-v2 status` is green and reports the expected internal-alpha metadata
- [ ] [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md), [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md), and [ALPHA_READINESS.md](ALPHA_READINESS.md) are current

## Validation

- [ ] `scripts/dev/retrofx-v2 --help` works
- [ ] `scripts/dev/retrofx-v2 status` works
- [ ] representative resolve or plan or compile flow works
- [ ] representative bounded apply or off flow works in a temp HOME or isolated XDG roots
- [ ] X11 render preview is re-checked where a supported X11 host exists
- [ ] `scripts/dev/retrofx-v2 package-alpha ...` succeeds
- [ ] package manifest shows the expected version, status label, and source-control summary
- [ ] package manifest shows the expected local tag candidate name
- [ ] temp-HOME `install` succeeds
- [ ] temp-HOME `diagnostics` succeeds and captures source-control plus installed bundle evidence
- [ ] temp-HOME `uninstall` succeeds

## Artifact Generation

- [ ] repo-local package output exists under `v2/releases/internal-alpha/` or the chosen safe package root
- [ ] package includes [ALPHA_CANDIDATE_NOTES.md](ALPHA_CANDIDATE_NOTES.md), [ALPHA_CANDIDATE_SUMMARY.md](ALPHA_CANDIDATE_SUMMARY.md), and [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md)
- [ ] install-state metadata shows the expected internal-alpha version and status

## Documentation Truth

- [ ] [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) reflects the latest candidate validation evidence
- [ ] [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md) reflects current open risks only
- [ ] [ALPHA_READINESS.md](ALPHA_READINESS.md) reflects the current verdict
- [ ] [ALPHA_CANDIDATE_NOTES.md](ALPHA_CANDIDATE_NOTES.md) still matches the branch truth
- [ ] [ALPHA_CANDIDATE_SUMMARY.md](ALPHA_CANDIDATE_SUMMARY.md) matches the current candidate package and tag name

## Decision

- [ ] if any blocker remains, do not create a local tag
- [ ] if the validation subset fails unexpectedly, do not create a local tag
- [ ] any local tag remains unpushed and non-public
- [ ] 1.x is still described as the production line
- [ ] broader-testing or public-ready claims are not made
