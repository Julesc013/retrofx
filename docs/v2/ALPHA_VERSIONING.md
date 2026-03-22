# RetroFX 2.x Versioning And Status Identities

RetroFX 2.x now uses two explicit identities:

- an internal developer-line identity
- a narrower technical-beta candidate identity

That split is deliberate.
It keeps the broader internal surface from being mistaken for the outside-facing advanced-tester package.

## Current Identities

### Internal Developer Line

- version: `2.0.0-alpha.internal.2`
- status label: `internal-alpha`
- intended surface: `scripts/dev/retrofx-v2`
- current prompt milestone in code metadata: `TWO-35`
- matching local tag for this exact version: none
- latest historical local alpha tag: `v2.0.0-alpha.internal.1`
- note: the current `main` HEAD uses this identity by default, but it is not represented by a current local tag

### Limited Technical-Beta Candidate

- version: `2.0.0-techbeta.1`
- status label: `technical-beta`
- intended surface: `scripts/dev/retrofx-v2-techbeta`
- matching local candidate tag: `v2.0.0-techbeta.1`
- note: the technical-beta tag is a historical candidate tag and may not point at the current `main` HEAD after later documentation or execution-only commits

### Reserved But Blocked

- reserved non-public pre-beta version: `2.0.0-prebeta.internal.1`
- reserved non-public pre-beta tag: `v2.0.0-prebeta.internal.1`
- current state: blocked, not approved

Code-side source of truth:

- `v2/dev/release.py`

## Why The Split Exists

The internal developer line needs to keep reporting the broader experimental platform truth:

- internal package flows
- migration inspection
- preview and internal-only X11 probe paths
- broader implementation status

The technical-beta candidate needs a narrower promise:

- copied-toolchain package
- advanced tester workflow
- explicit support matrix
- bounded cleanup and diagnostics expectations

One version/status label cannot express both surfaces honestly.

## Format Rules

### Internal Developer Line

Format:

- `2.0.0-alpha.internal.<n>`

Why:

- clearly distinct from `1.x`
- clearly non-public
- clearly experimental
- suitable for internal package, install-state, and release-status metadata

### Technical-Beta Candidate

Format:

- `2.0.0-techbeta.<n>`

Why:

- clearly distinct from the internal developer line
- clearly narrower than a general public beta
- suitable for copied-toolchain candidate packages and outside-facing status output

## What These Identities Apply To

Internal developer-line identity applies to:

- `package-alpha`
- internal release-status metadata
- user-local experimental install-state derived from internal bundles
- `retrofx-v2` status output

Technical-beta candidate identity applies to:

- `package-technical-beta`
- copied-toolchain candidate metadata
- `retrofx-v2-techbeta` status output
- technical-beta diagnostics and install-state records

## Version Discipline

- keep the internal developer line and technical-beta candidate line separate
- increment the internal-alpha suffix only when the internal testing contract changes materially
- increment the technical-beta suffix only when the outside-facing candidate contract changes materially
- do not mint pre-beta, public-beta, or stable-looking metadata until their gates are actually satisfied
- do not treat a historical local tag as proof that the current `main` HEAD is the same candidate

## Readiness Versus Version

Version identity and readiness are related, but not identical.

Current example:

- internal developer line: `2.0.0-alpha.internal.2`
- technical-beta candidate: `2.0.0-techbeta.1`
- limited technical beta continuation: approved
- broader beta stabilization: not approved

That means the repo can expose a narrowed advanced-tester surface without claiming that the broader internal platform has crossed the same maturity gate.
