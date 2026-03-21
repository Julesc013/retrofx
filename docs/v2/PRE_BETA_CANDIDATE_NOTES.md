# RetroFX 2.x Non-Public Pre-Beta Candidate Notes

This document records the current non-public pre-beta-candidate position for the 2.x branch.

It is not a public release note.
It is not a statement that a non-public pre-beta candidate exists today.

## Candidate Identity

- proposed candidate version: `2.0.0-prebeta.internal.1`
- proposed status label: `pre-beta`
- proposed local tag candidate: `v2.0.0-prebeta.internal.1`
- current branch version: `2.0.0-alpha.internal.2`
- current branch status label: `internal-alpha`
- candidate approval: blocked
- readiness verdict: `PRE_BETA_CANDIDATE_READY=no`

## Implemented And Candidate-Worthy Surface

If the branch eventually clears the gates, the candidate-worthy implemented surface would be:

- resolve, plan, compile, bundle, install, uninstall, diagnostics, and status through `scripts/dev/retrofx-v2`
- bounded apply or off inside isolated `retrofx-v2-dev` roots
- deterministic terminal, WM, toolkit-export, display-policy, and bounded X11 compiler families
- pack-aware profile resolution and curated built-in packs
- 1.x inspection plus draft migration output

## Still Experimental Or Partial

- bounded X11 `picom` probing remains an explicit internal-only action
- toolkit outputs remain advisory exports rather than live desktop ownership
- Wayland render remains degraded or export-only
- migration validation remains representative rather than broad
- the package flow still assumes a repo checkout rather than a copied standalone toolchain

## Supported Or Validated Scenarios

- clean-tree `status`, `resolve`, `plan`, `compile`, `bundle`, `package-alpha`, `install`, `uninstall`, `apply`, `off`, `diagnostics`, and `smoke`
- deterministic compiler output for CRT, palette, passthrough, and warm-night style families
- bounded temp-HOME install or uninstall and diagnostics capture
- one real X11 plus `i3` bounded preview or probe validation path

## Degraded Or Export-Only Areas

- non-sway Wayland desktops remain export-oriented validation environments
- TTY or headless environments remain planning or export paths only
- toolkit outputs remain advisory rather than owned DE state
- live Wayland render is not implemented

## Known Limitations

- broader-alpha gates are still not satisfied
- there is still no real Wayland-host validation pass
- real-host validation breadth still centers on one strong X11 plus `i3` host
- migration validation breadth is still too narrow for pre-beta positioning
- public packaging, standalone copied-toolchain distribution, and default runtime takeover do not exist

## Tester Focus If This Candidate Is Revisited Later

- multi-host validation, especially at least one real Wayland host
- one additional real X11 host beyond the current strongest validation machine
- broader curated migration-corpus review
- verification that current package, install, uninstall, and diagnostics surfaces remain deterministic on clean trees

## Explicitly Out Of Scope

- public beta or stable claims
- replacement of the 1.x runtime or CLI
- live Wayland render ownership
- global GNOME, Plasma, or Xfce settings mutation
- standalone copied-toolchain distribution

## Revert And Cleanup

- use `scripts/dev/retrofx-v2 off` to clear bounded current activation state
- use `scripts/dev/retrofx-v2 uninstall <bundle-id>` to remove installed bundles from `retrofx-v2-dev`
- prefer temp HOME or isolated XDG roots for validation runs
- diagnostics capture is local-file based and does not remove state by itself

## Approval Verdict

- `READY_FOR_LOCAL_PRE_BETA_TAG_CANDIDATE=no`
- `PRE_BETA_CANDIDATE_READY=no`
- reason: the branch remains an internal-alpha hardening build and has not cleared the broader-alpha or pre-beta gates
