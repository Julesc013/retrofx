# RetroFX 2.x Alpha Blockers

This document lists the remaining blockers and residual risks for the current 2.x branch.

Controlled internal alpha remains acceptable.
Broader alpha does not.

It is not a future wish list.
It is a concrete blocker list derived from [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md).

## Current Alpha-Blocker Status

There are no current `alpha-blocker` items for the supported internal-alpha surface after the TWO-28 hardening pass.

Resolved in TWO-23:

- the explicit bounded X11 `picom` probe was run manually on a real X11 plus `i3` host
- the unified delegated help surface now reports `retrofx-v2 ...` usage headers rather than leaking `cli.py`
- bounded apply or off and uninstall now refuse cleanup targets outside the managed 2.x roots, with regression coverage

Resolved in TWO-26:

- diagnostics capture now records a truthful self-inventory including `capture-manifest.json`
- diagnostics capture now records repo source-control state for reproduction on repo-checkout-based internal alpha runs
- diagnostics capture now records installed bundle inventory plus installed and packaged manifest evidence for the selected profile

Resolved in TWO-27:

- release-status metadata now carries the candidate-ready flag and local tag name consistently through `status`, `package-alpha`, and diagnostics capture
- alpha-candidate notes, summary, and release checklist are now aligned around one local-only candidate version and tag name
- the default repo-local package output root is now treated as generated output so the local candidate package flow can be exercised without contaminating branch state
- the full local candidate subset now passes again on the current branch state, including repo-local package generation, temp-HOME install or diagnostics or uninstall, and the bounded X11 preview probe

## Current High-Severity Status

There are no current open `high` items in the supported internal-alpha surface after TWO-28 hardening.

## Medium

### 1. Validation is still narrow compared with broader-alpha needs

- Severity: `medium`
- Evidence: the strongest real-host evidence is still one X11 plus `i3` host, with broader environment coverage still relying on simulation or forced classification
- Why it matters: this no longer blocks narrow internal alpha use, but it still blocks broader-alpha and pre-beta claims
- Recommended next step: run the broader-alpha matrix on at least one additional real environment, ideally one real Wayland session and one more X11 host

### 2. Real Wayland-host validation is still absent

- Severity: `medium`
- Evidence: TWO-28 now explicitly fences GNOME-like and Plasma-like Wayland sessions as export-oriented validation paths, but that fencing is still based on simulated or forced planning rather than real-host runs
- Why it matters: honest fencing is better than silent overclaiming, but it still means broader-alpha evidence is incomplete
- Recommended next step: run the supported checklist on a real Wayland host and update the broader-alpha matrix with the result

### 3. Legacy migration validation is still representative rather than broad

- Severity: `medium`
- Evidence: current migration validation still centers on a representative subset of legacy profiles rather than a wider curated corpus
- Why it matters: migration remains explicitly dev-only, but broader-alpha positioning needs a wider truth sample before the branch can claim stronger continuity evidence
- Recommended next step: expand the validated legacy profile corpus and record the outcomes in the matrices

## Low

### 4. Internal-alpha package and diagnostics surfaces still assume internal context

- Severity: `low`
- Evidence: package, diagnostics, and release metadata are now honest about internal-only use, but they still assume a repo checkout and an internal operator who understands the current surface
- Why it matters: this does not block internal alpha, but it still argues against broader external circulation
- Recommended next step: keep package and diagnostics flows positioned as internal-only until broader-alpha gates are satisfied

## Not Blockers

These are intentionally incomplete but do not block continued internal alpha on their own because the branch already documents them honestly:

- live Wayland render
- global desktop integration
- full 1.x runtime compatibility mode
- public packaging or distro integration

Those remain planned future scope, not regressions against the current branch promise.
