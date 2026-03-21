# RetroFX 2.x Technical Beta Notes

This document is written in a form that could be shown to outside advanced testers later.

It is not approval for publication.
For TWO-31, the branch is still not ready for a limited public technical beta.

## Intended Tester Audience

- technically literate testers
- users comfortable with repo checkouts, temp-HOME runs, and machine-readable JSON output
- users who understand explicit environment caveats and export-only behavior

## What The Branch Currently Supports

- `status`, `resolve`, `plan`, `compile`, `bundle`, `install`, `uninstall`, `diagnostics`, and `smoke`
- pack-aware profile resolution and curated built-in packs
- deterministic terminal, WM, toolkit-export, typography, display-policy, and bounded X11 compiler outputs
- bounded apply/off inside isolated `retrofx-v2-dev` roots

## Important Limitations

- this branch is still not approved for publication
- 1.x remains the production runtime and CLI
- live Wayland render is not implemented
- toolkit outputs are advisory exports, not desktop ownership
- the package flow still assumes a repo checkout rather than a standalone copied toolchain
- the strongest real-host evidence still centers on one X11 plus `i3` host

## Explicitly Unsupported Right Now

The following areas are unsupported in the current branch:

- public/general-user beta expectations
- live Wayland render ownership
- global desktop mutation
- standalone copied-toolchain distribution

## Recommended Smoke Path

1. `scripts/dev/retrofx-v2 status`
2. `scripts/dev/retrofx-v2 smoke --pack modern-minimal --profile-id warm-night`
3. `scripts/dev/retrofx-v2 package-alpha --pack modern-minimal --profile-id warm-night`
4. temp-HOME `install`, `diagnostics`, and `uninstall`
5. bounded `apply` or `off` only if you understand the current internal caveats

## Revert And Cleanup

- `scripts/dev/retrofx-v2 off`
- `scripts/dev/retrofx-v2 uninstall <bundle-id>`
- prefer temp HOME or isolated XDG roots for validation

## Useful Feedback

- deterministic output regressions
- install, uninstall, or cleanup ownership problems
- misleading status, help, or docs wording
- capability misclassification across environments
- diagnostics bundles missing evidence needed to reproduce a bug

## Not Useful As “Bug” Reports Right Now

- lack of live Wayland render
- lack of global GNOME, Plasma, or Xfce ownership
- advisory toolkit exports not acting like live desktop integration
- lack of 1.x runtime compatibility takeover
