# v2/tests

Purpose:

- home of 2.x-only tests, fixtures, and non-user-facing validation coverage

Implemented now:

- TOML fixtures for valid and invalid 2.x profiles
- isolated unit tests for load, validate, normalize, and resolve behavior
- end-to-end tests for the terminal/TUI compiler family
- end-to-end tests for the WM target compiler family
- end-to-end tests for the typography and font-policy compiler slice
- end-to-end tests for the advisory display-policy compiler slice
- environment-detection and session-planning tests
- local pack-manifest discovery and pack-aware resolution tests
- 1.x compatibility inspection and draft migration tests
- experimental bundle, install, status, and uninstall tests using temp HOME/XDG roots
- a small shell runner for 2.x-only tests

Do implement here later:

- schema and validator tests
- resolved-model planner tests
- adapter contract tests
- compatibility shim tests

Do not implement here:

- 1.x stable-line regression ownership
- user-facing demo scripts pretending the 2.x engine is done

Current rule:

- these tests cover only the experimental 2.x core scaffold
- they do not replace `scripts/test.sh` or the 1.x runtime checks
