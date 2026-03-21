# RetroFX 2.x Dev Workflow

RetroFX 2.x now has a real developer workflow, but it is still explicitly experimental and separate from 1.x.

## Core Rule

The 2.x dev workflow must remain:

- repo-local by default
- user-local when installed
- non-destructive to 1.x
- explicit about what is only exported, bundled, or installed

## Repo-Local Flow

Recommended flow:

1. Resolve a profile:
   `v2/core/dev/resolve-profile <profile>`
2. Preview the environment-aware plan:
   `v2/core/dev/plan-session <profile>`
3. Compile target artifacts:
   `v2/core/dev/compile-targets <profile>`
4. Package a deterministic dev bundle:
   `scripts/dev/retrofx-v2-bundle <profile>`

Pack-aware flow:

1. Inspect packs:
   `v2/core/dev/list-packs`
2. Inspect one pack:
   `v2/core/dev/show-pack <pack-id>`
3. Bundle a curated profile:
   `scripts/dev/retrofx-v2-bundle --pack <pack-id> --profile-id <profile-id>`

## Installed Dev Flow

The first installed dev flow is still managed from the repository checkout.

Recommended flow:

1. Build a bundle:
   `scripts/dev/retrofx-v2-bundle --pack crt-core --profile-id green-crt`
2. Install that bundle into the user-local 2.x footprint:
   `scripts/dev/retrofx-v2-install --bundle-id crt-core--green-crt`
3. Inspect current installed state:
   `scripts/dev/retrofx-v2-status`
4. Remove the installed bundle:
   `scripts/dev/retrofx-v2-uninstall crt-core--green-crt`

## Safe Validation Workflow

For tests or local experimentation, prefer a temp HOME or explicit XDG roots.

Example:

```bash
HOME="$(mktemp -d)" \
XDG_CONFIG_HOME="$HOME/.config" \
XDG_DATA_HOME="$HOME/.local/share" \
XDG_STATE_HOME="$HOME/.local/state" \
scripts/dev/retrofx-v2-install --bundle-id crt-core--green-crt
```

This keeps the experimental 2.x install slice isolated from both 1.x and real user data.

## What This Workflow Does Not Do

The current dev workflow does not:

- replace `scripts/retrofx`
- perform live session apply
- install system-wide assets
- publish bundles remotely
- switch defaults for 1.x users

## Discipline For Later Prompts

Later prompts should extend this workflow by adding:

- richer bundle contents
- standalone toolchain install
- repair and cleanup helpers
- public release packaging

Later prompts should not:

- bypass bundles with ad hoc installers
- reuse 1.x install paths
- turn experimental 2.x helpers into the default `retrofx` command before the platform is ready
