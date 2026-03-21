# v2/compat

Purpose:

- future home of the 2.x compatibility shell

Do implement here later:

- 1.x profile import and upgrade helpers
- bridges between legacy workflows and the 2.x engine
- future dispatcher shims once explicit prompts cover that transition

Do not implement here:

- core semantic planning logic
- target emission ownership
- experimental feature dumping ground logic

Current rule:

- `./scripts/retrofx` remains the working 1.x CLI until a later migration phase explicitly changes that.

