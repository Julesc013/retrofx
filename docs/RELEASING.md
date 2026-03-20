# Releasing RetroFX

Current beta-candidate target: `1.0.0-beta.1`.

Use this file for the high-level sequence and `docs/RELEASE_CHECKLIST.md` for the exact pre-tag gate.

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
./scripts/retrofx status
```

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
