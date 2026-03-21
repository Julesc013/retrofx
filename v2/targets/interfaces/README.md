# v2/targets/interfaces

Purpose:

- future home of target-layer interface contracts shared across adapter families

What belongs here:

- adapter input and output contracts
- capability declaration shapes
- common emission and validation result shapes
- shared degradation-reporting contracts

What does not belong here:

- family-specific config rendering
- raw profile parsing
- session orchestration logic

Governing docs:

- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/ADAPTER_INTERFACE.md`
- `docs/v2/TARGET_CAPABILITY_DECLARATIONS.md`

Later prompts should implement:

- stable adapter contracts that all target families can consume consistently

