# v2/core/interfaces

Purpose:

- future home of stable contracts between the core pipeline and downstream modules

Expected future interface surfaces:

- normalized profile contract
- resolved semantic model contract
- capability-filtered target plan contract
- artifact plan contract
- target-adapter input and output contracts
- session handoff contracts

Do implement here later:

- interface definitions that targets and session can consume without depending on raw authored input

Do not implement here:

- backend-specific config rendering
- live apply behavior
- ad hoc helper code with no contract value

