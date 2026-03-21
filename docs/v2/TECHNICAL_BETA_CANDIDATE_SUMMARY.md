# RetroFX 2.x Technical Beta Candidate Summary

TECHNICAL_BETA_CANDIDATE_READY=yes

Candidate version: `2.0.0-techbeta.1`

Candidate status: `technical-beta`

Candidate tag name: `v2.0.0-techbeta.1`

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

1. generate the copied-toolchain candidate package
2. run the release checklist
3. create the local candidate tag if the final validation pass stays clean
4. circulate the package only to advanced testers who match the documented support matrix
