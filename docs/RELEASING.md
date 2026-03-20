# Releasing RetroFX

## 1. Bump Version

Update `VERSION` to the next release value.

Also update any user-facing release markers that still carry an explicit version string:

- `README.md`
- `docs/BETA_NOTES.md`
- `docs/BETA_RELEASE_NOTES.md` (when relevant)

## 2. Recheck Product Truth Docs

If support boundaries changed during the release cycle, sync:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`
- `docs/ROADMAP.md`
- `docs/TESTING.md`

Do not ship a release with docs that overstate capability.

## 3. Update Changelog

Edit `CHANGELOG.md`:

- add release date
- summarize notable changes
- keep Keep a Changelog structure

## 4. Run Validation

```bash
./scripts/ci.sh
./scripts/retrofx --version
./scripts/retrofx list
./scripts/retrofx doctor
```

Optional installed-mode smoke test:

```bash
./scripts/retrofx install --yes
~/.local/bin/retrofx --version
~/.local/bin/retrofx status
```

## 5. Create Commit And Tag

```bash
git add -A
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
```

## 6. Push

```bash
git push
git push --tags
```
