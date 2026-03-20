# RetroFX Install Guide

RetroFX 1.x supports two normal usage modes:

- Repo-local mode: run directly from a cloned repository.
- User-local install mode: install under `~/.config/retrofx` with launcher at `~/.local/bin/retrofx`.

No root privileges are required. RetroFX does not modify `/etc`.

## Mode Summary

| Mode | Status | Notes |
| --- | --- | --- |
| Repo-local | Supported | Primary workflow for development and testing. |
| User-local install | Supported | Managed copy under `~/.config/retrofx`; launcher at `~/.local/bin/retrofx`. |
| User-local i3 Xsession helper | Supported | Generates managed user Xsession entries only. |
| greetd / other display managers | Degraded | Manual integration only. No automatic global config edits. |

## Repo-Local Mode

```bash
cd /path/to/retrofx
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx off
```

## User-Local Install Mode

Install into the default location:

```bash
./scripts/retrofx install --yes
```

Custom install home:

```bash
./scripts/retrofx install --yes --path ~/.config/retrofx
```

After install:

- launcher: `~/.local/bin/retrofx`
- home: `~/.config/retrofx`
- managed assets: `scripts/`, `templates/`, `backends/`, `profiles/`, `docs/`, `VERSION`, and related runtime files
- runtime state: `active/`, `state/`
- user-owned pack assets: `profiles/user_assets/`

`retrofx status` reports runtime health separately from install-asset health so an incomplete install is not mistaken for a broken applied profile.

## Pack Installs In User Space

```bash
retrofx install-pack core
```

`install-pack <packname>` copies pack profiles into `profiles/user/`. If a pack profile references a local support file such as a custom palette, RetroFX copies that asset into `profiles/user_assets/<profile-id>/` and rewrites the installed profile to use the copied asset path.

## Uninstall

Remove the user-local install and managed launcher:

```bash
retrofx uninstall --yes
```

Keep user profiles while uninstalling:

```bash
retrofx uninstall --yes --keep-profiles
```

`--keep-profiles` stores preserved profiles in a timestamped backup directory next to the install home.

## Optional X11 i3 Integration

Create a managed user-local Xsession entry:

```bash
~/.config/retrofx/scripts/integrate/install-xsession.sh --profile crt-green-p1-4band
```

Remove managed Xsession entries:

```bash
~/.config/retrofx/scripts/integrate/remove-xsession.sh --all-managed --yes
```

These helpers only touch user-local `.desktop` entries that carry the RetroFX marker key.

## Manual greetd / Other DM Integration

RetroFX does not edit greetd or system display-manager configuration automatically.

Suggested flow:

1. Install RetroFX user-local.
2. Create the user-local Xsession entry with `install-xsession.sh` if you want the i3 wrapper path.
3. Select that session entry in tuigreet or wire your own session launcher manually.
4. Treat `active/tuigreet.conf` as a generated snippet, not a global config writer.

For recovery and diagnostics see `docs/TROUBLESHOOTING.md`. For pre-tag smoke tests and local release packaging, see `docs/RELEASE_CHECKLIST.md`.
