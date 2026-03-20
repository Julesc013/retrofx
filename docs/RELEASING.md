# Releasing RetroFX

Current beta-candidate target: `1.0.0-beta.1`.

Use this file for the high-level sequence and `docs/RELEASE_CHECKLIST.md` for the exact pre-tag gate.

For post-beta bug triage and fix discipline, also use:

- `docs/BETA_TRIAGE.md`
- `docs/BUGFIX_CHECKLIST.md`
- `docs/BUG_REPORT_TEMPLATE.md`
- `docs/ENVIRONMENT_REPORT_TEMPLATE.md`

## 0. Post-Beta Intake Rule

Every accepted post-beta 1.x bugfix must include:

1. a reproducible bug statement or clear operator-visible failure description
2. the smallest correct code or doc fix
3. a regression test, or a written reason why the bug cannot be automated safely
4. a changelog update if the fix is user-visible
5. a release-notes update if the fix materially changes operator expectations, support boundaries, or recovery guidance

Do not land release-branch fixes as untracked one-offs.

## 0.1 Release Progression

Use the 1.x beta/stable sequence explicitly:

- `1.0.0-beta.1`
- `1.0.0-beta.2`
- `1.0.0-beta.3`
- `1.0.0-rc1`
- `1.0.0`

Advance to the next stage only when these conditions hold:

- Beta to next beta:
  - blocker/high-severity fixes are still landing
  - supported-host confidence is still being broadened
  - docs or support boundaries are still being corrected
- Beta to RC:
  - all known release blockers are closed
  - support matrix and docs match the code
  - supported X11 path has been validated on real hosts
  - no major support ambiguity remains
- RC to stable:
  - no release blockers or unresolved high-severity bugs remain in supported environments
  - `apply`, `off`, `self-check`, `repair`, `install`, and `uninstall` are boringly reliable
  - the release checklist passes cleanly
  - degraded paths are honest and non-destructive

Do not cut a new tag from the same version after a user-visible fix lands. Bump the prerelease identifier first.

## 1. Align Release Metadata

Update and cross-check:

- `VERSION`
- `CHANGELOG.md`
- `README.md`
- `docs/BETA_NOTES.md`
- `docs/BETA_RELEASE_NOTES.md`
- versioned release notes such as `docs/RELEASE_NOTES_1.0.0-beta.1.md`

Do not ship a release with mixed version strings or mixed beta/stable wording.

## 2. Recheck Truth Docs

If support boundaries changed during the release cycle, sync:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`
- `docs/ROADMAP.md`
- `docs/TESTING.md`
- `docs/INSTALL.md`

Do not ship a release with docs that overstate capability.

## 3. Run The Release Checklist

Follow `docs/RELEASE_CHECKLIST.md` in order.

Minimum automated validation:

```bash
./scripts/ci.sh
./scripts/test.sh
./scripts/retrofx --version
./scripts/retrofx doctor
./scripts/retrofx status
```

For blocker/high-severity fixes that cannot be fully validated in automation, record the manual host validation that was run and the outcome in the release checklist, release summary, or issue notes before tagging.

## 4. Build Local Release Archives

Use the helper:

```bash
./scripts/release-package.sh
```

This writes deterministic local archives under `state/releases/<version>/`.

## 5. Tag Only After Human Smoke Verification

Recommended local sequence after the checklist passes:

```bash
git status --short --branch
git tag -a vX.Y.Z -m "RetroFX vX.Y.Z"
./scripts/release-package.sh --ref vX.Y.Z
```

Do not push automatically. Push only after a human confirms the final smoke results and the tag contents.

## 6. Push When Approved

```bash
git push
git push --tags
```
