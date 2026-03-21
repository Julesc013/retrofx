# RetroFX 2.x Internal Alpha Runbook

This runbook is for controlled internal testers of the 2.x branch.

It assumes:

- you have a repo checkout
- you are using the experimental 2.x surface only
- you understand that 1.x remains the production line

## 1. Inspect Branch Status

Run:

```bash
scripts/dev/retrofx-v2 status
```

Confirm:

- `release_status.status_label = "internal-alpha"`
- environment detection looks plausible
- no unexpected active 2.x state is already present

## 2. Resolve One Profile

Run either:

```bash
scripts/dev/retrofx-v2 resolve v2/tests/fixtures/strict-green-crt.toml
```

or pack-aware:

```bash
scripts/dev/retrofx-v2 resolve --pack modern-minimal --profile-id warm-night
```

## 3. Plan For The Current Environment

Run:

```bash
scripts/dev/retrofx-v2 plan --pack modern-minimal --profile-id warm-night --write-preview
```

Check:

- `compile_targets`
- `apply_preview_targets`
- `degraded_targets`
- `x11_render` and `toolkit_style` summaries

## 4. Compile Outputs

Run:

```bash
scripts/dev/retrofx-v2 compile --pack modern-minimal --profile-id warm-night
```

Inspect:

- `v2/out/<profile-id>/...`
- target-specific artifacts you care about

## 5. Inspect Packs Or Migration If Relevant

Pack inspection:

```bash
scripts/dev/retrofx-v2 packs list
scripts/dev/retrofx-v2 packs show modern-minimal
```

Legacy inspection:

```bash
scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/crt-green-p1-4band.toml --write-draft
```

## 6. Test Bounded Apply Or Off

Use a temp HOME when possible:

```bash
tmp_home="$(mktemp -d)"
HOME="$tmp_home" XDG_CONFIG_HOME="$tmp_home/.config" XDG_DATA_HOME="$tmp_home/.local/share" XDG_STATE_HOME="$tmp_home/.local/state" \
  scripts/dev/retrofx-v2 apply v2/tests/fixtures/warm-night-theme-only.toml
HOME="$tmp_home" XDG_CONFIG_HOME="$tmp_home/.config" XDG_DATA_HOME="$tmp_home/.local/share" XDG_STATE_HOME="$tmp_home/.local/state" \
  scripts/dev/retrofx-v2 status
HOME="$tmp_home" XDG_CONFIG_HOME="$tmp_home/.config" XDG_DATA_HOME="$tmp_home/.local/share" XDG_STATE_HOME="$tmp_home/.local/state" \
  scripts/dev/retrofx-v2 off
```

Check:

- `current-state.json`
- activation manifest
- `removed_paths` and `skipped_cleanup_paths`

## 7. Test X11 Render Preview Where Supported

Only on a safe X11 host:

```bash
scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --probe-picom --probe-seconds 1.0
```

Check:

- generated shader and picom config
- `preview.probe.status`
- `preview-state.json`

Do not treat this as a production runtime path.

## 8. Test Bundle Or Install Flow In Isolation

Use a temp HOME:

```bash
tmp_home="$(mktemp -d)"
scripts/dev/retrofx-v2 bundle --pack modern-minimal --profile-id warm-night
HOME="$tmp_home" XDG_CONFIG_HOME="$tmp_home/.config" XDG_DATA_HOME="$tmp_home/.local/share" XDG_STATE_HOME="$tmp_home/.local/state" \
  scripts/dev/retrofx-v2 install v2/bundles/modern-minimal--warm-night
HOME="$tmp_home" XDG_CONFIG_HOME="$tmp_home/.config" XDG_DATA_HOME="$tmp_home/.local/share" XDG_STATE_HOME="$tmp_home/.local/state" \
  scripts/dev/retrofx-v2 uninstall modern-minimal--warm-night
```

## 9. Test Internal-Alpha Packaging

Run:

```bash
scripts/dev/retrofx-v2 package-alpha --pack modern-minimal --profile-id warm-night
```

Inspect:

- `v2/releases/internal-alpha/<package-id>/package-manifest.json`
- bundled docs under `docs/`
- included bundle under `bundle/`

You can install the packaged bundle with:

```bash
scripts/dev/retrofx-v2 install v2/releases/internal-alpha/<package-id>/bundle
```

## 10. Capture Validation Results

Run:

```bash
scripts/dev/retrofx-v2 diagnostics --pack modern-minimal --profile-id warm-night --label alpha-pass
```

Record:

- environment
- command run
- expected result
- actual result
- whether it was pass, degraded-pass, partial, fail, blocked, or not-tested

Update or compare against:

- `docs/v2/VALIDATION_MATRIX.md`
- `docs/v2/ALPHA_BLOCKERS.md`
- `docs/v2/CONTROLLED_ALPHA_PLAN.md`
- `docs/v2/ALPHA_TRIAGE.md`

## 11. Report Blockers

When reporting a blocker, include:

- exact command
- environment details
- relevant JSON output
- whether temp HOME or repo-local mode was used
- whether 1.x paths were touched unexpectedly

Use:

- `docs/v2/ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md`
- `docs/v2/ALPHA_FEEDBACK_TEMPLATE.md`
- `docs/v2/ALPHA_ISSUE_TEMPLATE.md`

If a behavior is merely missing and already documented as out of scope, report it as a limitation rather than a regression.
