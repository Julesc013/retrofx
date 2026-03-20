# RetroFX Beta Triage

Use this file to classify incoming 1.x beta issues and decide whether they block the next tag.

For product scope and support boundaries, cross-check:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`
- `docs/TESTING.md`

Always classify the report in the context where it occurs:

- `Supported`
- `Degraded`
- `Export-only`
- `Unsupported`

Bugs in unsupported contexts do not normally block release unless they are destructive or the docs materially misstate support.

## Severity Classes

| Class | Typical examples | Blocks next beta | Blocks RC | Blocks stable |
| --- | --- | --- | --- | --- |
| Release blocker | `apply`/`off`/`repair` corrupt state, supported X11 shader path fails broadly, install/uninstall damages user state, `self-check`/`repair` lies, compositor starts incorrectly, docs materially misstate supported behavior | Yes | Yes | Yes |
| High severity | Supported profile family broken, degraded mode behaves destructively, pack install breaks assets, import/export is misleading enough to cause bad results, install assets or wrappers regress in supported paths | Usually yes | Yes unless clearly isolated and documented | Yes |
| Medium | UX confusion, noisy or inconsistent warnings, non-core profile issues, docs drift that does not change support truth, edge-case bugs in degraded paths | Usually no | Maybe, if clustered or support truth becomes muddy | No by itself |
| Low | Cosmetic messaging, wording improvements, minor preview quirks, maintainability cleanup without behavioral impact | No | No | No |

## Post-Beta Fix Rule

Every accepted 1.x beta fix must include:

1. a clear bug statement or reproduction
2. severity classification
3. supported/degraded/unsupported context
4. the smallest correct fix
5. a regression test, or a written reason why automation is not practical
6. a changelog update if the fix is user-visible
7. a release-notes update if the fix changes operator expectations, support boundaries, or recovery guidance

Do not merge release-branch bugfixes as undocumented one-offs.

## Triage Flow

1. Confirm the reported version and environment.
2. Decide whether the report is in a supported, degraded, export-only, or unsupported context.
3. Assign severity.
4. Decide release impact:
   - next beta only
   - blocks RC
   - blocks stable
5. Reproduce the issue or narrow it to a clear operator-visible failure.
6. Land the smallest correct fix with regression coverage.
7. Re-run the affected tests plus `./scripts/test.sh`.
8. Record any host-only manual validation that was still required.

## Version Progression

Use the 1.x prerelease line deliberately:

- `1.0.0-beta.1`
- `1.0.0-beta.2`
- `1.0.0-beta.3`
- `1.0.0-rc1`
- `1.0.0`

Move from one beta to the next while blocker/high-severity fixes are still landing or supported-host confidence is still being expanded.

Move from beta to RC only when:

- all known release blockers are closed
- docs and support matrix match the code
- supported X11 + picom + GLX behavior has been revalidated on real hosts
- no major ambiguity remains around supported vs degraded behavior

Move from RC to stable only when:

- no release blockers remain
- no unresolved high-severity bugs remain in supported environments
- release checklist and automation pass cleanly
- install/uninstall/repair/self-check are trustworthy
- degraded paths are honest and non-destructive

## Done For 1.0

RetroFX 1.0 is ready when:

- all release blockers are closed
- no unresolved high-severity bugs remain in supported environments
- support matrix and docs match actual behavior
- the release checklist passes cleanly
- install/uninstall/repair/self-check are trustworthy
- the supported X11 path has been validated on real host(s)
- degraded paths remain honest and non-destructive

Anything outside those conditions stays in beta/RC; it does not get hand-waved into stable.
