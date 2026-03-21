# RetroFX 2.x Public Beta Gates

This document defines what must be true before the 2.x branch can claim a limited public technical beta.

This gate is stricter than the current internal-alpha position and also stricter than a blocked non-public pre-beta placeholder.

## A. Documentation

Required:

- README and readiness docs are truthful
- install, uninstall, diagnostics, and cleanup flow are documented clearly
- supported versus degraded versus unsupported environments are explicit
- known limitations and non-goals are obvious to outside advanced testers

Current TWO-31 state:

- not met for public beta
- docs are now clearer, but they still describe an internal-only toolchain and repo-checkout-dependent workflow

## B. Workflow Safety

Required:

- no hidden destructive side effects
- bounded apply/off remains trustworthy in supported environments
- package, install, uninstall, and diagnostics flows are deterministic
- cleanup and ownership are explicit

Current TWO-31 state:

- partially satisfied
- the flows are bounded and deterministic for internal use, but the overall operator burden is still too high for outside testers

## C. Implementation Trust

Required:

- compiler outputs remain deterministic
- status, manifests, and install-state are trustworthy
- migration tooling is clearly honest and validated broadly enough for outside use
- X11 render is clearly classified and not overclaimed
- degraded/export-only paths are surfaced explicitly

Current TWO-31 state:

- not met for public beta
- deterministic behavior is good, but migration breadth and real-host breadth are still too narrow

## D. Audience Suitability

Required:

- a technically literate tester can succeed without source archaeology
- the branch does not impersonate production quality
- the support burden remains manageable for maintainers

Current TWO-31 state:

- not met
- the branch still assumes internal context, repo access, and high operator familiarity

## Gate Result

For TWO-31:

- limited public technical beta: not ready
- continued non-public pre-beta: not ready
- continued internal alpha: yes
- next step: another internal hardening cycle focused on real-host breadth and external-surface discipline
