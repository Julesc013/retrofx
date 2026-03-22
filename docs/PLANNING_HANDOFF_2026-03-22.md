# RetroFX Planning Handoff

Date: 2026-03-22

Audience: planning agents, maintainers, and future implementation prompts for both the stable `1.x` line and the experimental `2.x` line.

Scope: this report summarizes the current repository after the `TWO-33` technical-beta execution pass and the later branch consolidation onto `main`.

## Executive Summary

RetroFX now contains two distinct product lines in one repository:

- `1.x` is the production line. Its repo-visible version remains `1.0.0`, its release artifacts exist under `state/releases/1.0.0/`, and its policy is explicitly patch-only.
- `2.x` is a large experimental platform under `v2/` and `docs/v2/`. It has moved far beyond architecture notes and now includes implemented compilers, planning, bounded apply/off, packaging, diagnostics, migration inspection, and a narrowed `technical-beta` wrapper for advanced testers.

The most important planning fact is not technical, but operational:

- the repository is now consolidated onto `main`
- the historical local side branches used during the long `TWO-*` run are gone
- this means future discipline must come from process and release policy, not from assuming 1.x and 2.x are physically isolated in separate long-lived local branches

Current strategic truth:

- `1.x` is stable and should stay boring
- `2.x` is credible enough for continued limited technical beta
- `2.x` is not yet ready for broader beta stabilization
- `2.x` is not a replacement for `1.x`
- `main` now carries both the stable product line and the experimental redesign track, which increases the need for explicit planning boundaries

## Verified Repository State

Shell-verified at report time:

- branch: `main`
- branch tracking: `origin/main`
- working tree: clean
- `main` and `origin/main` point at `4e5ffcb`
- local side branches removed: `next/2.0-architecture`, `release/1.0`
- local tags present: `v0.1.0-beta.1`, `v1.0.0-beta.1`, `v1.0.0`, `v2.0.0-alpha.internal.1`, `v2.0.0-techbeta.1`
- remote technical-beta tags are not visible from the shell as of this report

Implication:

- the repo is operationally simplified, but history and scope are not
- planning should assume one branch with two maturity tracks rather than one maturity track

## Tracked Repository Inventory

Tracked file count from `git ls-files`: `384`

Tracked file distribution by top-level area:

| Area | Tracked files | Notes |
| --- | ---: | --- |
| `<root>` | 4 | repo metadata such as `README.md`, `VERSION`, `CHANGELOG.md`, `.gitignore` |
| `backends/` | 6 | 1.x backend scripts and docs |
| `docs/` | 127 | includes both stable-line docs and the large 2.x design/status corpus |
| `profiles/` | 24 | 1.x pack and profile inputs |
| `scripts/` | 25 | 1.x CLI, release helpers, and 2.x dev wrappers |
| `templates/` | 4 | 1.x output templates |
| `tests/` | 1 | 1.x shell fixture set is mostly embedded in `scripts/test.sh` |
| `v2/` | 192 | 2.x implementation, packs, tests, dev tooling, compilers, and session orchestration |

Tracked file distribution by type:

| Extension | Tracked count |
| --- | ---: |
| `.md` | 174 |
| `.py` | 111 |
| `.toml` | 57 |
| no extension | 21 |
| `.sh` | 15 |
| `.in` | 4 |
| `.txt` | 1 |
| `.json` | 1 |

Planning interpretation:

- this repository is documentation-heavy by design
- `docs/v2/` is now a large product/architecture/status corpus, not a speculative appendix
- future planning must budget for doc maintenance explicitly or doc drift will become a real cost center

## Current Repository Layout

The effective repo shape is now:

### Stable-line runtime and release surface

- `scripts/retrofx`
- `backends/`
- `profiles/`
- `templates/`
- `state/`
- top-level docs under `docs/`

### Experimental 2.x platform

- `v2/core/`
- `v2/targets/`
- `v2/session/`
- `v2/compat/`
- `v2/packs/`
- `v2/dev/`
- `v2/tests/`
- `docs/v2/`
- `scripts/dev/retrofx-v2*`

### Local/generated artifact areas worth knowing about

- `state/releases/1.0.0*/` contains stable-line release artifacts
- `v2/releases/internal-alpha/` contains local/internal 2.x package artifacts
- `v2/releases/reports/` contains generated report zips

Planning implication:

- maintainers should treat `state/releases/` and `v2/releases/` as operational outputs, not as the source of product truth
- source truth for 1.x remains the root docs and `scripts/retrofx`
- source truth for 2.x remains `docs/v2/` plus `v2/` code

## 1.x Current State

### Product Truth

The stable line is clearly defined in:

- `README.md`
- `docs/1x_PRODUCT.md`
- `docs/1x_MAINTENANCE.md`
- `docs/ROADMAP.md`

Verified stable-line summary:

- current repository version is `1.0.0`
- support target is still the documented `X11 + picom + GLX` path
- Wayland remains degraded by design
- TTY and `tuigreet` remain scoped secondary outputs
- install/uninstall, rollback, manifest integrity, and repair are part of the core 1.x contract
- 1.x is patch-only after `1.0.0`

### 1.x Command Surface

The production CLI is still `scripts/retrofx`.

Command classes documented in `docs/1x_PRODUCT.md`:

- inspect: `status`, `list`, `search`, `info`, `explain`, `gallery`, `preview`, `doctor`, `compatibility-check`
- lifecycle: `apply`, `apply --dry-run`, `off`, `self-check`, `repair`
- profiles and interop: `new`, `install-pack`, `import base16`, `export`
- install mode: `install`, `uninstall`
- diagnostics: `perf`, `sanity-perf`

Planning implication:

- 1.x already has a full operator-facing CLI and should not absorb 2.x experiments
- future 1.0.x work should stay within bug-fix, doc-truth, safety, and supported-path compatibility boundaries

### 1.x Support Matrix

From the current root docs:

- supported:
  - X11 + picom + GLX
  - repo-local mode
  - user-local install mode
  - TTY ANSI16 backend
  - `tuigreet` snippet generation
  - Base16 import/export
- degraded:
  - Wayland sessions
  - X11 sessions outside the documented i3 wrapper path
  - TTY font apply
  - Base16 round-trip fidelity
- unsupported:
  - broad DE orchestration
  - global Wayland shader/compositor control
  - GTK/Qt/icon/cursor ownership

### 1.x Safety Model

1.x safety and maturity claims are concrete rather than aspirational:

- atomic apply/off
- rollback snapshots under `state/last_good/`
- manifest-based `self-check`
- `repair`
- bounded user-local installation

This is a mature stable-line shape. Planning should preserve that constraint.

### 1.x Validation Status

Fresh shell run in this repo:

- `./scripts/test.sh`
- result: passed

Important nuance from the test harness itself:

- wrapper tests use stubbed `picom` and `i3`
- Wayland checks use simulated session variables
- TTY tests use mock mode
- full live compositor/GLX validation still requires host validation outside the automated suite
- `shellcheck` was not installed in the local environment during the run, so the suite skipped it with a warning

Planning implication:

- do not confuse “1.x tests pass” with “all host-validation work is done forever”
- future 1.0.x planning should preserve periodic real-host supported-path validation

### 1.x Release State

Existing release artifacts are present under:

- `state/releases/1.0.0/`
- `state/releases/1.0.0-beta.1/`

That means the stable line has an actual release/distribution story, not just docs.

### 1.x Planning Direction

Recommended 1.x planning posture:

- patch-only
- fix only supported-path bugs and doc-truth issues
- resist feature temptation
- keep `scripts/retrofx` boring
- keep support statements conservative

Good 1.0.x work:

- bug fixes
- repair/apply/install safety fixes
- docs truth corrections
- supported-host validation
- pack/profile fixes that restore documented behavior

Bad 1.0.x work:

- new rendering families
- new orchestration concepts
- DE-wide theming automation
- profile-schema redesign
- anything that smells like 2.x architecture work

## 2.x Current State

### Overall Position

2.x is no longer just a design branch in spirit, even though it remains experimental in policy.

It now includes:

- schema validation
- normalization
- resolved profile model
- real target compiler families
- pack-aware resolution
- environment detection and planning
- bounded apply/off
- bundle/install/uninstall flows
- diagnostics capture
- migration inspection
- internal-alpha packaging
- limited technical-beta packaging and wrapper
- readiness, blocker, and validation docs for multiple maturity stages

This is a real platform-in-progress, not a draft.

### 2.x Implementation Surface

The most accurate code-side summary remains in `docs/v2/IMPLEMENTED_STATUS.md`.

Currently implemented and real:

- `v2/core/validation/`
- `v2/core/normalization/`
- `v2/core/resolution/`
- terminal compilers under `v2/targets/terminal/`
- WM compilers under `v2/targets/wm/`
- toolkit exporters under `v2/targets/toolkit/`
- X11 render/compiler slice under `v2/targets/x11/`
- session planning under `v2/session/planning/`
- bounded apply/off under `v2/session/apply/`
- bundle/install/uninstall under `v2/session/install/`
- compatibility and migration inspection under `v2/compat/`
- pack system under `v2/packs/`
- release/status/diagnostics/package tooling under `v2/dev/`

Not implemented:

- global desktop integration
- live Wayland render ownership
- full compatibility/runtime replacement for 1.x
- production CLI takeover

### 2.x CLI Surfaces

There are now two meaningfully different 2.x command surfaces:

#### Internal developer surface

Entrypoint: `scripts/dev/retrofx-v2`

Purpose:

- broad internal experimentation
- dev inspection
- migration inspection
- preview and diagnostic operations
- packaging across alpha and technical-beta flows

Representative commands:

- `status`
- `resolve`
- `compile`
- `plan`
- `packs`
- `migrate inspect-1x`
- `bundle`
- `install`
- `uninstall`
- `apply`
- `off`
- `preview-x11`
- `package-alpha`
- `package-technical-beta`
- `diagnostics`
- `smoke`

#### Narrowed outside-facing technical-beta surface

Entrypoint: `scripts/dev/retrofx-v2-techbeta`

Purpose:

- advanced tester workflow only
- copied-toolchain package entrypoint
- smaller support promise

Exposed commands:

- `status`
- `capabilities`
- `resolve`
- `compile`
- `plan`
- `bundle`
- `diagnostics`
- `install`
- `uninstall`
- `apply`
- `off`
- `packs`
- `smoke`

Not exposed on the technical-beta wrapper:

- `migrate inspect-1x`
- `preview-x11`
- broader internal packaging/status surfaces

Planning implication:

- planning agents should not collapse these two surfaces into one story
- the internal developer surface is broader than the external technical-beta promise by design

### 2.x Validation and Readiness

Current decision chain from the 2.x docs:

- internal alpha continuation: yes
- broader alpha: no
- non-public pre-beta: no
- limited public technical beta: yes
- limited technical beta continuation: yes
- broader beta stabilization: no

The most current documents are:

- `docs/v2/TECHNICAL_BETA_READINESS.md`
- `docs/v2/TECHNICAL_BETA_MATRIX.md`
- `docs/v2/PUBLIC_BETA_READINESS.md`
- `docs/v2/NEXT_STAGE_VERDICT.md`

Fresh automation status:

- `./v2/tests/test.sh`
- result: `Ran 143 tests in 2.981s`
- result: `OK`

### 2.x Technical Beta Truth

The limited technical-beta candidate is intentionally narrow.

Current outside-facing promise:

- copied-toolchain package exists
- advanced testers can use it without repo archaeology
- bounded X11-oriented apply/off exists
- install/uninstall is temp-HOME/user-local and reversible
- diagnostics are sufficient for structured bug reports
- Wayland is export-oriented or degraded, not live-owned
- toolkit outputs are advisory exports, not desktop ownership

What remains internal-only:

- explicit X11 preview/probe workflows
- migration inspection as an assurance story
- the broader internal `retrofx-v2` command surface

### 2.x Validation Breadth Limits

The main reason 2.x is not yet approved for broader beta stabilization is not “obvious breakage”.

It is evidence breadth.

Current limiting factors called out repeatedly in the docs:

- validation is still centered on one real X11 + `i3`-like host
- broader outside tester evidence has not been gathered yet
- Wayland remains degraded/export-only in the technical-beta story
- migration is representative rather than broad

Planning implication:

- the next 2.x cycle should be evidence expansion and operational hardening, not architecture expansion
- if planning reopens large product questions now, it will destabilize a line that is finally narrow enough to be testable

### 2.x Packaging and Artifact State

Source-controlled package and release infrastructure exists, but most outputs are generated locally.

Known local output locations:

- `v2/releases/internal-alpha/retrofx-v2--2.0.0-alpha.internal.1--modern-minimal--warm-night/package-manifest.json`
- `v2/releases/reports/retrofx-v2-two33-full-report-20260322.zip`
- `v2/releases/reports/retrofx-main-sync-report-20260322.zip`

Important nuance:

- the `v2.0.0-techbeta.1` tag exists locally
- it is not visible on the remote via shell `ls-remote` as of this report
- planning should decide whether local-only tags are acceptable or whether candidate tags must always be pushed once approved

### 2.x Timeline Summary

The `TWO-*` sequence has now covered three broad phases:

1. architecture and contract definition (`TWO-01` to `TWO-08`)
2. implementation build-out (`TWO-09` to `TWO-19`)
3. consolidation, validation, remediation, packaging, gating, and technical-beta execution (`TWO-20` to `TWO-33`)

That matters because:

- 2.x is no longer in early architecture discovery
- the current bottleneck is trust and evidence, not feature imagination

## Cross-Line Observations

### 1. One repo, two maturity models

This is now the central planning challenge.

`main` contains:

- a stable `1.0.0` product line
- a large experimental `2.x` platform

That is workable, but only if planning keeps strong boundaries:

- 1.x changes must stay patch-like
- 2.x work must stay clearly experimental unless promoted by explicit gates
- docs must keep distinguishing “production line” from “experimental line”

### 2. Root version and branch reality can confuse people

The repo root still says:

- `VERSION = 1.0.0`

That is correct because 1.x remains the production line.

But the same branch also contains:

- 2.x technical-beta tooling
- 2.x candidate docs
- 2.x package builders

Planning implication:

- external messaging must not infer repo-wide maturity from the root version alone
- future operator docs should keep saying “1.x is production; 2.x is experimental”

### 3. Documentation is an asset and a maintenance cost

There are more tracked markdown files than Python files.

That is justified because:

- 2.x relied on design-first execution
- readiness gating has been doc-driven and explicit

But it also means:

- future planning must budget for doc pruning, indexing, or consolidation
- otherwise `docs/v2/` will become harder to navigate than the code it describes

### 4. Generated report artifacts are becoming part of the workflow

The repo now has a real habit of producing:

- release artifacts
- package manifests
- readiness summaries
- report zips

That is good for auditability.

But planning should decide:

- which artifacts are canonical
- which are purely local outputs
- which should eventually be reproducible in CI or release automation

### 5. Testing maturity differs sharply between 1.x and 2.x

1.x:

- one large shell/integration harness
- strong workflow coverage
- host realism still partly manual

2.x:

- structured Python unittest suite
- contract and surface coverage
- more deterministic component-level validation
- real-host evidence still comparatively narrow

Planning implication:

- future shared quality work could standardize reporting, but should not force the 1.x shell suite into a redesign unless there is a maintenance reason

## Recommended Planning Workstreams

### Workstream A: 1.0.x Stable Maintenance

Goal:

- keep the shipping line trustworthy without reopening design scope

Good next tasks:

- validate supported X11 + picom + GLX host behavior on real machines
- tighten docs if any repo-main consolidation caused ambiguity
- patch user-visible bugs in `apply`, `off`, `repair`, install, uninstall, or pack relocation
- keep `CHANGELOG.md` and release notes disciplined if 1.0.x work lands

Avoid:

- new capabilities
- schema changes
- 2.x backports
- broad DE/Wayland ambitions

### Workstream B: 2.x Technical-Beta Continuation

Goal:

- widen evidence without widening promises

Good next tasks:

- run the technical-beta package on more real hosts
- collect structured reports via the new templates
- compare diagnostics bundles across hosts
- validate cleanup and status semantics under more outside-style usage
- keep migration and explicit X11 probe internal-only until evidence justifies promotion

Avoid:

- adding new target families
- reopening architecture
- public/general-user beta framing
- pretending Wayland live ownership exists

### Workstream C: Repo and Release Governance

Goal:

- reduce confusion now that both lines live on `main`

Good next tasks:

- define whether future 2.x tags must be pushed or may remain local-only
- define whether experimental candidate packaging belongs only in local outputs or should gain a more formal release lane later
- decide how planners should distinguish “production”, “experimental internal”, and “advanced external tester” materials in one branch
- decide whether a small top-level governance doc is needed to explain the single-branch model

### Workstream D: Documentation Governance

Goal:

- keep the docs corpus useful as it grows

Good next tasks:

- identify redundant `docs/v2/` files
- define a canonical index for planners vs implementers vs testers
- prune or collapse docs that duplicate the same readiness decision

## Recommended Near-Term Sequence

### Immediate

1. Treat `1.x` and `2.x` as separate planning lanes even though they now share `main`.
2. Keep `1.x` patch-only.
3. Continue `2.x` limited technical beta with real outside-style evidence capture.
4. Do not start broader beta stabilization until the evidence base actually widens.

### Near-Term

1. Gather multiple real-host technical-beta reports.
2. Compare diagnostics bundles and classify real regressions vs unsupported-environment noise.
3. Reassess whether the current limited technical-beta support matrix remains accurate.
4. Only then revisit broader-beta gating.

### Later

1. Decide whether 2.x should aim next for broader beta stabilization or remain a long-running advanced-tester line.
2. Decide what a future public-facing packaging/promotion story looks like.
3. Decide whether single-branch governance is still helping or starting to obscure product-line boundaries.

## Explicit Planning Questions

These are the questions planning agents should answer next, not just list:

1. In a `main`-only world, what process keeps `1.x` patch work from being diluted by `2.x` experimentation?
2. What exact outside-tester evidence is required before `2.x` can move from limited technical beta to broader beta stabilization?
3. Should `v2.0.0-techbeta.1` remain a local-only tag, or should technical-beta tags be pushed once branch sync is complete?
4. Is migration breadth important enough to invest in before broader beta, or should it remain explicitly internal-only for longer?
5. Should Wayland stay intentionally export-oriented for the next cycle, or is there pressure to reopen architecture prematurely?
6. Does `docs/v2/` need a doc-governance pass before more implementation continues?
7. Should the repo gain a short top-level governance doc explaining how `1.x production` and `2.x experimental` coexist on `main`?

## Suggested Reading Order For Planning Agents

### For 1.x planning

1. `README.md`
2. `docs/1x_PRODUCT.md`
3. `docs/1x_MAINTENANCE.md`
4. `docs/ROADMAP.md`
5. `CHANGELOG.md`

### For 2.x planning

1. `docs/v2/README.md`
2. `docs/v2/IMPLEMENTED_STATUS.md`
3. `docs/v2/TECHNICAL_BETA_READINESS.md`
4. `docs/v2/TECHNICAL_BETA_MATRIX.md`
5. `docs/v2/PUBLIC_BETA_READINESS.md`
6. `docs/v2/NEXT_STAGE_VERDICT.md`
7. `docs/v2/ROADMAP.md`

### For command-surface truth

1. `scripts/retrofx`
2. `v2/dev/cli.py`
3. `v2/dev/technical_beta_cli.py`

### For quality/trust planning

1. `scripts/test.sh`
2. `v2/tests/test.sh`
3. `v2/tests/`

## Bottom Line

RetroFX is no longer a small project with one maturity level.

The repo now contains:

- a stable `1.0.0` shipping line that should stay conservative
- a substantial `2.x` experimental platform that has successfully reached limited technical beta, but not broader beta stabilization

The most useful next planning move is not “add more”.

It is:

- preserve 1.x trust
- expand 2.x evidence carefully
- keep the public promise narrower than the internal implementation surface
- and make branch/process governance explicit now that everything lives on `main`
