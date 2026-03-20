# RetroFX Bugfix Checklist

Use this for every accepted post-beta 1.x fix.

- Reproduce the bug or write a clear operator-visible failure statement.
- Classify severity using `docs/BETA_TRIAGE.md`.
- Mark the context:
  - Supported / Degraded / Export-only / Unsupported
- Decide whether the issue blocks:
  - next beta
  - RC
  - stable
- Add a failing regression if feasible.
- If automation is not feasible, write down why and what manual validation is required.
- Implement the smallest correct fix.
- Re-run the affected commands/tests plus `./scripts/test.sh`.
- Update docs if behavior changed or was clarified.
- Update `CHANGELOG.md` if the fix is user-visible.
- Update release notes if operator expectations, support truth, or recovery guidance changed.
- Record any host-only validation needed for blocker/high-severity fixes.
- Decide the target release:
  - next beta
  - next RC
  - stable only after the release criteria are met
