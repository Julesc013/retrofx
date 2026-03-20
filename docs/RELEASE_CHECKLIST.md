# RetroFX Release Checklist

Use this checklist before creating a release tag. Current target: `1.0.0-beta.1`.

## Validation Outcome

Latest local validation for `1.0.0-beta.1` was completed on `2026-03-21`.

- Automated checks passed: `./scripts/ci.sh`, `./scripts/test.sh`, `./scripts/retrofx --version`, `./scripts/retrofx list`, `./scripts/retrofx doctor`, `./scripts/retrofx status`, `./scripts/retrofx self-check`.
- Practical smoke checks passed: `./scripts/retrofx compatibility-check`, `./scripts/retrofx apply crt-green-p1-4band`, `./scripts/retrofx off`, `./scripts/retrofx repair`, and temp-HOME `install --yes` / `uninstall --yes`.
- Remaining human judgment: final publish approval still depends on the operator reviewing release notes, local archives, and any host-specific desktop smoke results they care about beyond the supported X11 path.

## 1. Automated Validation

Run from repository root:

```bash
./scripts/ci.sh
./scripts/test.sh
./scripts/retrofx --version
./scripts/retrofx list
./scripts/retrofx doctor
./scripts/retrofx status
./scripts/retrofx self-check
```

All commands must exit successfully.

## 2. Manual Validation

Supported X11 host:

```bash
./scripts/retrofx compatibility-check
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx status
./scripts/retrofx off
```

Installed-mode smoke test in a temporary home:

```bash
TMP_HOME="$(mktemp -d)"
HOME="$TMP_HOME" ./scripts/retrofx install --yes
HOME="$TMP_HOME" "$TMP_HOME/.local/bin/retrofx" --version
HOME="$TMP_HOME" "$TMP_HOME/.local/bin/retrofx" status
HOME="$TMP_HOME" ./scripts/retrofx uninstall --yes
rm -rf "$TMP_HOME"
```

Optional degraded Wayland smoke test:

```bash
DISPLAY= WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland ./scripts/retrofx explain crt-green-p1-4band
DISPLAY= WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland ./scripts/retrofx apply crt-green-p1-4band --dry-run
```

Optional TTY / tuigreet smoke test:

```bash
RETROFX_TTY_MODE=mock ./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx apply crt-green-fonts-aa
```

## 3. Cleanliness

- `git status --short --branch` is clean.
- No unintended untracked files are present.
- `VERSION`, `CHANGELOG.md`, README, and release notes agree on the candidate version.
- `docs/1x_PRODUCT.md`, `docs/CAPABILITIES.md`, and `docs/TESTING.md` still match the code.

## 4. Packaging

Generate local release archives:

```bash
./scripts/release-package.sh
```

Outputs are written under:

- `state/releases/<version>/retrofx-<version>-src.tar.gz`
- `state/releases/<version>/retrofx-<version>-src.zip`
- matching `.sha256` files

Optional tag-based rebuild after tagging:

```bash
./scripts/release-package.sh --ref v1.0.0-beta.1
```

## 5. Tagging

After the checklist passes and a human confirms the smoke results:

```bash
git status --short --branch
git tag -a v1.0.0-beta.1 -m "RetroFX v1.0.0-beta.1"
./scripts/release-package.sh --ref v1.0.0-beta.1
```

Do not push automatically. Push only after the operator confirms the local tag and archive contents.
