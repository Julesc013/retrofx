# v2/core/interfaces

Purpose:

- current home of the code-side contract shapes that the experimental 2.x branch now treats as explicitly implemented
- shared boundary definitions between the core pipeline and downstream targets, planning, install, apply, pack, and migration surfaces

Implemented here now:

- [contracts.py](contracts.py) contains the branch's current required-key sets for:
  - resolved profile output
  - target compiler results
  - session plans
  - apply-state and activation manifests
  - pack manifests
  - migration reports
  - install records

This module is intentionally narrow:

- it does not freeze the whole 2.x architecture as public API
- it does make the current experimental internal boundaries testable and auditable
- it is the code-side companion to `docs/v2/IMPLEMENTED_INTERFACES.md`

Expected future interface surfaces:

- capability-filtered resolved profile contract once that layer is no longer placeholder-only
- artifact plan contract once artifact planning becomes a real core output
- broader session handoff contracts once runtime ownership expands beyond the bounded current-state flow

Do not implement here:

- backend-specific config rendering
- live apply behavior
- ad hoc helper code with no contract value
