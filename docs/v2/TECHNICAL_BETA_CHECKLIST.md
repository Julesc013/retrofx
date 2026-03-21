# RetroFX 2.x Technical Beta Checklist

This checklist is preparatory only.
It does not mean the branch is approved for public technical beta today.

## Preflight

- read [TECHNICAL_BETA_NOTES.md](TECHNICAL_BETA_NOTES.md)
- confirm the branch is still explicitly experimental
- run `./v2/tests/test.sh`
- run `scripts/dev/retrofx-v2 status`

## Safe Smoke Path

- run `scripts/dev/retrofx-v2 resolve --pack modern-minimal --profile-id warm-night`
- run `scripts/dev/retrofx-v2 plan --pack modern-minimal --profile-id warm-night --write-preview`
- run `scripts/dev/retrofx-v2 compile --pack modern-minimal --profile-id warm-night`
- inspect toolkit and X11 outputs as artifacts, not as proof of live ownership

## Bounded Runtime Checks

- if using temp HOME, run `scripts/dev/retrofx-v2 apply <profile>` only when you understand the current caveats
- run `scripts/dev/retrofx-v2 off` afterward
- on supported X11 hosts only, use `scripts/dev/retrofx-v2 preview-x11 ... --probe-picom` as an explicit bounded probe

## Package And Diagnostics

- run `scripts/dev/retrofx-v2 package-alpha ...`
- run temp-HOME `install`
- run `scripts/dev/retrofx-v2 diagnostics ...`
- run temp-HOME `uninstall`
- attach the diagnostics directory when reporting issues

## Cleanup

This cleanup step is mandatory after bounded runtime checks.

- verify no unexpected paths outside `retrofx-v2-dev` were touched
- remove temp HOME or temp XDG roots after testing
