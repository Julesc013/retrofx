# RetroFX 2.x Alpha Remediation Backlog

This backlog records the first post-alpha remediation cycle for the 2.x branch.

Current evidence base:

- [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md)
- [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md)
- [ALPHA_READINESS.md](ALPHA_READINESS.md)
- latest controlled-alpha diagnostics capture under `/tmp/retrofx-v2-two25-diag.wbcEtm/20260321-102849z--alpha-smoke`
- latest post-remediation diagnostics capture under `/tmp/retrofx-v2-two26-final.ehxVzM/diag/20260321-103929z--candidate-pass`
- current unified status output from `scripts/dev/retrofx-v2 status`
- current green automated suite from `./v2/tests/test.sh`

There is not yet a broader external tester corpus recorded in-tree.
This backlog is therefore a first-pass remediation cycle derived from current in-branch alpha tooling evidence.

| ID | Severity | Area | Source evidence | Problem summary | Planned action | Requires regression? | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AR-001 | high | diagnostics/reporting | `/tmp/retrofx-v2-two25-diag.wbcEtm/20260321-102849z--alpha-smoke/capture-manifest.json` | diagnostics artifact inventory omitted the manifest itself, so the bundle was not fully self-describing | manifest inventory now includes `capture-manifest.json` and is covered by regression tests | yes | completed |
| AR-002 | high | diagnostics/reporting | `/tmp/retrofx-v2-two25-diag.wbcEtm/20260321-102849z--alpha-smoke/install-state.json`, `/tmp/retrofx-v2-two25-diag.wbcEtm/20260321-102849z--alpha-smoke/profile/output-inventory.json`, `scripts/dev/retrofx-v2 status` | diagnostics capture did not preserve enough repo-state and installed-bundle context for strong reproduction on repo-checkout-based internal alpha runs | diagnostics now capture source-control summary, installed bundle inventory, installed bundle manifest, and source package manifest for the selected profile | yes | completed |
| AR-003 | medium | docs/dev-surface | [ALPHA_READINESS.md](ALPHA_READINESS.md), [POST_ALPHA_DECISION_RULES.md](POST_ALPHA_DECISION_RULES.md) | branch docs did not yet answer the new local alpha tag-candidate question explicitly | readiness and decision docs now state the local alpha-candidate verdict and add candidate notes plus checklist docs | no | completed |
| AR-004 | medium | environment-specific | [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md), [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) | multi-host validation is still narrow and remains a broader-confidence risk | keep documented as residual risk; do not overstate readiness | no | accepted-risk |
| AR-005 | medium | migration/compat | [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md), [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) | migration validation is still representative rather than broad | keep documented as residual risk; do not claim broader compatibility confidence | no | accepted-risk |
