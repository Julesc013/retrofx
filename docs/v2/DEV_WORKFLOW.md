# RetroFX 2.x Dev Workflow

RetroFX 2.x now has a real developer workflow, but it is still explicitly experimental and separate from 1.x.

## Core Rule

The 2.x dev workflow must remain:

- repo-local by default
- user-local when installed
- non-destructive to 1.x
- explicit about what is only exported, bundled, or installed

## Preferred Entry Point

Use the unified experimental dispatcher first:

1. Inspect platform status:
   `scripts/dev/retrofx-v2 status`
2. Run a non-destructive smoke flow:
   `scripts/dev/retrofx-v2 smoke v2/tests/fixtures/strict-green-crt.toml`
3. Run the same flow against a curated pack profile:
   `scripts/dev/retrofx-v2 smoke --pack modern-minimal --profile-id warm-night`

The older individual helpers still exist and remain truthful.
The unified dispatcher just makes the implemented branch surface easier to discover.

## Repo-Local Flow

Recommended flow:

1. Resolve a profile:
   `scripts/dev/retrofx-v2 resolve <profile>`
2. Preview the environment-aware plan:
   `scripts/dev/retrofx-v2 plan <profile>`
3. Compile target artifacts:
   `scripts/dev/retrofx-v2 compile <profile>`
4. Package a deterministic dev bundle:
   `scripts/dev/retrofx-v2 bundle <profile>`

Pack-aware flow:

1. Inspect packs:
   `scripts/dev/retrofx-v2 packs list`
2. Inspect one pack:
   `scripts/dev/retrofx-v2 packs show <pack-id>`
3. Bundle a curated profile:
   `scripts/dev/retrofx-v2 bundle --pack <pack-id> --profile-id <profile-id>`

1.x migration review flow:

1. Inspect a 1.x profile:
   `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/crt-green-p1-4band.toml`
2. Optionally emit a generated draft:
   `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/crt-green-p1-4band.toml --write-draft`

## Installed Dev Flow

The first installed dev flow is still managed from the repository checkout.

Recommended flow:

1. Build a bundle:
   `scripts/dev/retrofx-v2 bundle --pack crt-core --profile-id green-crt`
2. Install that bundle into the user-local 2.x footprint:
   `scripts/dev/retrofx-v2 install --bundle-id crt-core--green-crt`
3. Inspect current installed state:
   `scripts/dev/retrofx-v2 status`
4. Remove the installed bundle:
   `scripts/dev/retrofx-v2 uninstall crt-core--green-crt`

## Optional Bounded Apply Flow

This is still experimental and should be run in a temp HOME or other isolated XDG roots.

1. Stage the bounded current activation:
   `scripts/dev/retrofx-v2 apply v2/tests/fixtures/warm-night-theme-only.toml`
2. Inspect the current activation:
   `scripts/dev/retrofx-v2 status`
3. Clear it:
   `scripts/dev/retrofx-v2 off`

## Safe Validation Workflow

For tests or local experimentation, prefer a temp HOME or explicit XDG roots.

Example:

```bash
HOME="$(mktemp -d)" \
XDG_CONFIG_HOME="$HOME/.config" \
XDG_DATA_HOME="$HOME/.local/share" \
XDG_STATE_HOME="$HOME/.local/state" \
scripts/dev/retrofx-v2 install --bundle-id crt-core--green-crt
```

This keeps the experimental 2.x install slice isolated from both 1.x and real user data.

## What This Workflow Does Not Do

The current dev workflow does not:

- replace `scripts/retrofx`
- perform broad live session apply
- install system-wide assets
- publish bundles remotely
- switch defaults for 1.x users

## Discipline For Later Prompts

Later prompts should extend this workflow by adding:

- stronger stabilization and cleanup
- interface hardening and real-world test passes
- standalone toolchain install when the branch is ready
- public release packaging only after the experimental platform stabilizes

Later prompts should not:

- bypass bundles with ad hoc installers
- reuse 1.x install paths
- turn experimental 2.x helpers into the default `retrofx` command before the platform is ready
