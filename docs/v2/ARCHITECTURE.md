# RetroFX 2.x Architecture

RetroFX 2.x is organized as a platform with a stable core and replaceable edges.
The core owns meaning and planning.
Target adapters own environment-specific compilation and emission.
Session orchestration owns lifecycle and recovery.

## Module Stack

1. Packs provide curated profile inputs and metadata.
2. Core turns source profiles into a resolved profile and artifact plan.
3. Theme and Render interpret different output domains from the resolved profile.
4. Targets and Adapters compile those domains into backend-specific artifacts.
5. Session applies, exports, installs, disables, or repairs those artifacts within declared scope.

## A. Core

Core is the architectural center of 2.x.
It must stay boring, deterministic, and backend-agnostic.

### Responsibilities

- parsing source profiles and pack metadata
- schema validation
- normalized profile model creation
- resolved profile creation
- token resolution
- environment and backend capability intersection
- artifact planning
- compile/apply plan generation
- deterministic logging inputs

### Core Rules

- Core does not emit backend-specific file syntax directly.
- Core does not own WM, toolkit, or session wrapper templates.
- Core does not guess support from file presence or host folklore.
- Core is the only place where profile meaning is normalized before compilation.

## B. Theme

Theme transforms resolved semantic intent into target-ready theme values and assets.

### Responsibilities

- colors and role mapping
- fonts and typography policy
- icons and icon-theme selection hints
- cursors and cursor-theme selection hints
- terminal themes
- WM and DE config themes
- toolkit export inputs for GTK, Qt, and similar targets

### Theme Rules

- Theme output must remain useful without render support.
- Theme decisions must not depend on runtime compositor assumptions.
- Theme may expose target-specific constraints, but not redefine profile semantics.

## C. Render

Render owns optional appearance transforms that change how output is visually presented at runtime or through render-capable targets.

### Responsibilities

- quantization
- dithering
- scanlines
- glow
- gamma, temperature, and bias
- optional display transforms where supported

### Render Rules

- Render is optional by design.
- A target without render support must still be able to consume the same resolved profile through theme-only compilation.
- Render modules describe intent and parameters; adapters decide whether they can host them.
- No global Wayland or compositor-wide behavior is assumed without an explicit capability path.

## D. Session

Session owns lifecycle, environment scoping, and the trustworthy application model.

### Responsibilities

- greetd and tuigreet integration
- TTY login integration
- Xsession integration
- WM or DE specific session integration
- environment scoping
- install, apply, export, off, and repair policy
- recovery metadata coordination

### Session Rules

- Session orchestration only manages declared paths.
- Session integration is explicit, auditable, and reversible.
- Exporting artifacts is not the same as applying a session plan.
- Session must remain trustworthy even when targets degrade.

## E. Packs

Packs are curated style families and reusable data bundles.

### Responsibilities

- curated style families
- palettes
- typography recommendations
- metadata
- preview metadata
- pack-level defaults and composition inputs

### Pack Rules

- Packs are data, not hidden imperative logic.
- Pack metadata may influence defaults and previews, but not bypass validation.
- Packs must resolve through the same core pipeline as user-authored profiles.

## F. Targets And Adapters

Targets are user-visible output domains.
Adapters are the concrete compilers for target and backend combinations.

### Responsibilities

- concrete target compilers
- capability declarations
- backend-specific emission
- adapter-specific validation
- target-level artifact shaping

### Adapter Rules

- Every adapter must declare capabilities before it can claim support.
- Adapters may narrow behavior, but cannot expand semantics beyond the resolved profile contract.
- Backend-specific quirks stay at the adapter edge and do not leak into the core profile model unless they become general product concepts.

## Conceptual Compile And Apply Flow

RetroFX 2.x follows this conceptual sequence:

`parse -> validate -> normalize -> resolve -> capability filter -> compile targets -> apply/export`

### Flow Meaning

1. `parse`
   Load the source profile, pack references, and selected target set.
2. `validate`
   Reject malformed input, unknown schema, or impossible combinations.
3. `normalize`
   Convert accepted input into one canonical profile model.
4. `resolve`
   Resolve tokens, defaults, pack inheritance or composition, and explicit intent.
5. `capability filter`
   Intersect requested intent with target and environment capabilities.
6. `compile targets`
   Run target adapters to emit artifacts from the filtered plan.
7. `apply/export`
   Either apply through session orchestration or emit explicit export-only artifacts.

## Architectural Boundaries

- One resolved profile model exists before any backend compilation happens.
- Theme, render, and session are separate concerns even when a single target uses all three.
- Target adapters compile from declared inputs; they do not reinterpret product scope locally.
- Recovery and lifecycle state are first-class architecture, not bolt-on scripts.
- Future prompts may extend adapters and packs, but should resist moving complexity into the core without a cross-target reason.

