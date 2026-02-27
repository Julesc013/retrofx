# Releasing RetroFX

## 1) Bump Version

Edit `VERSION` to the next semver value (for example `0.2.0`).

## 2) Update Changelog

Edit `CHANGELOG.md`:

- add release date
- summarize notable changes
- keep Keep a Changelog structure

## 3) Run CI Checks

```bash
./scripts/ci.sh
```

## 4) Create Commit + Tag

```bash
git add -A
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
```

## 5) Push

```bash
git push
git push --tags
```

## 6) Verify Installed Mode

Optional smoke test:

```bash
./scripts/retrofx install --yes
~/.local/bin/retrofx --version
~/.local/bin/retrofx status
```
