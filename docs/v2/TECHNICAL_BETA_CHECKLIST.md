# RetroFX 2.x Technical Beta Checklist

This checklist applies to the limited technical-beta candidate prepared in TWO-32.

## Preflight

- read [TECHNICAL_BETA_NOTES.md](TECHNICAL_BETA_NOTES.md)
- confirm you are using the copied-toolchain candidate package rather than the broader internal developer surface
- run `bin/retrofx-v2-techbeta status`

## Safe Smoke Path

- run `bin/retrofx-v2-techbeta resolve --pack modern-minimal --profile-id warm-night`
- run `bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview`
- run `bin/retrofx-v2-techbeta compile --pack modern-minimal --profile-id warm-night`
- inspect toolkit and X11 outputs as artifacts, not as proof of global desktop ownership

## Bounded Runtime Checks

- on supported X11 only, run `bin/retrofx-v2-techbeta apply --pack modern-minimal --profile-id warm-night`
- run `bin/retrofx-v2-techbeta off` afterward
- do not expect `preview-x11` or live Wayland ownership on this surface

## Package, Install, And Diagnostics

- run `bin/retrofx-v2-techbeta install <package-dir>/bundle`
- run `bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --label techbeta`
- run `bin/retrofx-v2-techbeta uninstall <bundle-id>`
- attach the diagnostics directory when reporting issues

## Cleanup

This cleanup step is mandatory.

- verify no unexpected paths outside `retrofx-v2-dev` were touched
- remove temp HOME or temp XDG roots after testing
