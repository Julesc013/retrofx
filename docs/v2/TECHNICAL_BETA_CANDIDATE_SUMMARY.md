# RetroFX 2.x Technical Beta Candidate Summary

TECHNICAL_BETA_CANDIDATE_READY=yes

Candidate version: `2.0.0-techbeta.1`

Candidate status: `technical-beta`

Candidate tag name: `v2.0.0-techbeta.1`

Current `main` note: this tag is the latest local technical-beta candidate snapshot, but current `main` may be ahead of it.

Default package root: `v2/releases/technical-beta/`

Primary supported environment: X11 plus `i3`-like

Major supported capabilities:

- deterministic resolve, plan, compile, and bundle flows
- temp-HOME install, diagnostics, and uninstall
- bounded apply and off on supported X11 environments
- advisory toolkit exports and bounded X11 artifacts

Major limitations:

- Wayland remains compile or export-oriented rather than supported live runtime ownership
- toolkit exports remain advisory only
- migration assurance and the explicit X11 probe remain internal-only
- 1.x remains the production line

Next human steps:

1. generate the copied-toolchain candidate package from the current tree when you need a fresh tester artifact
2. run the release checklist and the technical-beta execution plan
3. use the local tag as a reference snapshot, not as proof that current `main` is unchanged
4. circulate the package only to advanced testers who match the documented support matrix
