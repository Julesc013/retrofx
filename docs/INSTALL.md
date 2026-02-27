# RetroFX Install Guide

RetroFX supports two usage modes:

- Repo-local mode: run directly from a cloned repository.
- User-local install mode: install under `~/.config/retrofx` with launcher at `~/.local/bin/retrofx`.

No root privileges are required. RetroFX does not modify `/etc`.

## Repo-Local Mode

```bash
cd /path/to/retrofx
./scripts/retrofx list
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx off
```

## User-Local Install Mode

Install into default location:

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
- runtime dirs: `active/`, `state/`, `profiles/`, `templates/`, etc.

Check mode and active profile:

```bash
retrofx status
```

## Uninstall

Remove user-local install and managed launcher:

```bash
retrofx uninstall --yes
```

Keep user profiles while uninstalling:

```bash
retrofx uninstall --yes --keep-profiles
```

`--keep-profiles` stores preserved profiles in a timestamped backup directory next to the install home.

For recovery and diagnostics see:

- `docs/TROUBLESHOOTING.md`

## X11 i3 Xsession Entry (User-Local)

Create a managed Xsession entry:

```bash
~/.config/retrofx/scripts/integrate/install-xsession.sh --profile crt-green-p1-4band
```

Remove managed Xsession entries:

```bash
~/.config/retrofx/scripts/integrate/remove-xsession.sh --all-managed --yes
```

The generated desktop file includes a RetroFX marker key so uninstall/removal only touches managed entries.

## greetd/tuigreet Integration (Manual)

RetroFX does not edit greetd configuration automatically.

Suggested flow:

1. Install RetroFX user-local.
2. Create the user-local Xsession entry with `install-xsession.sh`.
3. In tuigreet, select that session entry (or your existing `Default.desktop` flow that launches the RetroFX wrapper).
4. Keep `active/tuigreet.conf` as a generated snippet reference only; merge manually into your greetd setup if desired.

## Other Display Managers (High Level)

- SDDM/LightDM/other DMs: use user-local `.desktop` session entries when supported.
- Keep system-wide DM configs unchanged unless you explicitly choose to integrate them.
- Prefer session wrappers and env hooks to limit RetroFX impact to chosen sessions.
