# RetroFX 2.x Alpha Execution Checklist

Use this as the short per-tester run sheet.

## Preparation

- [ ] repo checkout or internal-alpha package is available
- [ ] temp HOME or isolated XDG roots are ready if testing apply or install flows
- [ ] current branch or commit is recorded

## Sanity Check

- [ ] run `scripts/dev/retrofx-v2 --help`
- [ ] run `scripts/dev/retrofx-v2 status`
- [ ] confirm `release_status.status_label = "internal-alpha"`

## Core Flow

- [ ] run `resolve` on one profile
- [ ] run `plan` on the same profile
- [ ] run `compile` for at least terminal plus WM or toolkit targets

## Bounded Runtime Flow

- [ ] run `apply` in a temp HOME if the scenario calls for it
- [ ] run `status` after apply
- [ ] run `off`

## Package Or Install Flow

- [ ] run `bundle` or `package-alpha`
- [ ] run `install` in a temp HOME
- [ ] run `uninstall`

## Continuity Flow

- [ ] run `migrate inspect-1x` on at least one real 1.x profile

## X11 Flow If Applicable

- [ ] if on X11, run `preview-x11`
- [ ] only if appropriate, run the bounded explicit `--probe-picom` path

## Diagnostics And Feedback

- [ ] run `scripts/dev/retrofx-v2 diagnostics ...`
- [ ] fill out [ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md](ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md)
- [ ] fill out [ALPHA_FEEDBACK_TEMPLATE.md](ALPHA_FEEDBACK_TEMPLATE.md)
- [ ] if needed, create an [ALPHA_ISSUE_TEMPLATE.md](ALPHA_ISSUE_TEMPLATE.md) entry

## Final Check

- [ ] note whether the pass was `pass`, `degraded-pass`, `partial`, `fail`, `blocked`, or `not-tested`
- [ ] attach diagnostics path and commit hash to the report
