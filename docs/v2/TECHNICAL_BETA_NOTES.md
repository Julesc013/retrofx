# RetroFX 2.x Technical Beta Notes

These notes apply to the limited public technical-beta candidate prepared in TWO-32.

This is still experimental.
It is not a general-public beta.
It does not replace RetroFX 1.x.

## Intended Tester Audience

- advanced testers
- technically literate testers
- users comfortable with JSON output, temp-HOME runs, and explicit cleanup
- users who understand support-matrix caveats and export-only behavior

## Supported Candidate Surface

- `retrofx-v2-techbeta status`
- `resolve`, `plan`, `compile`, `bundle`, and `smoke`
- `install`, `uninstall`, and `diagnostics`
- bounded `apply` and `off` on X11-oriented environments only
- pack-aware profile resolution through the copied toolchain

## Supported And Validated Scenarios

- X11 plus `i3`-like environment for bounded runtime checks
- temp-HOME install, uninstall, and diagnostics capture
- deterministic terminal, WM, toolkit-export, typography, display-policy, and X11 artifact generation

## Degraded Or Export-Only Areas

- Wayland plus `sway`-like environments are acceptable for `status`, `resolve`, `plan`, `compile`, `bundle`, `diagnostics`, and `smoke`
- toolkit outputs are advisory exports, not live desktop ownership

## Explicitly Unsupported In This Candidate

These unsupported areas are not bugs for the limited technical-beta line:

- general-user beta expectations
- global desktop mutation
- live Wayland render ownership
- migration assurance beyond the internal developer surface
- the explicit bounded X11 `picom` probe

## Recommended Smoke Path

1. `bin/retrofx-v2-techbeta status`
2. `bin/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night`
3. `bin/retrofx-v2-techbeta install <package-dir>/bundle`
4. `bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --label first-pass`
5. `bin/retrofx-v2-techbeta uninstall <bundle-id>`
6. on supported X11 only, `bin/retrofx-v2-techbeta apply --pack modern-minimal --profile-id warm-night` followed by `bin/retrofx-v2-techbeta off`

## Revert And Cleanup

- `bin/retrofx-v2-techbeta off`
- `bin/retrofx-v2-techbeta uninstall <bundle-id>`
- prefer temp HOME or isolated XDG roots for validation

## Useful Feedback

- deterministic output regressions
- install, uninstall, or cleanup ownership problems
- misleading status, help, or docs wording
- capability misclassification across X11 and Wayland environments
- diagnostics bundles missing evidence needed to reproduce a bug

## Not Useful As Bug Reports For This Candidate

- lack of live Wayland render
- lack of global GNOME, Plasma, or Xfce ownership
- advisory toolkit exports not acting like live desktop integration
- lack of 1.x runtime takeover
- absence of the internal-only `preview-x11` probe on the technical-beta wrapper
