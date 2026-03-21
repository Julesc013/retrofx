# RetroFX 2.x Target Families

This document defines the major target families in RetroFX 2.x and why they remain separate.

## Why Families Exist

Target families group adapters that share:

- token consumption patterns
- artifact types
- execution modes
- capability limits

Keeping these families explicit prevents 2.x from collapsing into one generic "backend" bucket.

## 1. TTY Family

What it compiles:

- ANSI palette outputs
- console-font hints or console-font apply data where supported

Typical mode:

- apply-capable and export-capable

Typical artifacts:

- palette files or env maps
- console-font apply or restore data

Typical capability class:

- palette-heavy
- typography-limited
- no general render path

Common limitations:

- host console constraints
- narrow typography scope
- no chrome or compositor semantics

## 2. Tuigreet/Login Family

What it compiles:

- greet or login presentation fragments
- terminal-style palette and typography mappings for login contexts

Typical mode:

- export-oriented with limited apply or install integration

Typical artifacts:

- generated config snippets
- palette or typography fragments

Typical capability class:

- theme-capable
- limited session integration
- no meaningful render path

Common limitations:

- should not take over global display-manager ownership by default

## 3. Terminal/TUI Family

What it compiles:

- terminal app configs
- TUI app theme exports
- ANSI-derived palette outputs

Typical mode:

- both apply-like and export-like depending on the target

Typical artifacts:

- config files
- palette fragments
- app-specific theme snippets

Typical capability class:

- strong theme and typography support
- no compositor-style render requirement

Common limitations:

- limited ability to represent chrome or session semantics
- no global post-processing

## 4. X11 Render/Compositor Family

What it compiles:

- compositor config
- shader or render-source artifacts
- X11 render-adjacent helper outputs

Typical mode:

- apply-capable, install-capable, and export-capable depending on integration path

Typical artifacts:

- compositor config files
- shader sources
- runtime helper fragments

Typical capability class:

- strongest render support
- environment-dependent session integration

Common limitations:

- not equivalent to whole-desktop theming
- depends on truthful compositor and environment support

## 5. WM Config Family

What it compiles:

- WM-specific config fragments
- bar, launcher, and notification-adjacent outputs where the WM family owns them

Typical mode:

- export-capable
- sometimes install-capable
- sometimes apply-capable with scoped session reload behavior

Typical artifacts:

- WM config fragments
- palette variables
- style snippets

Typical capability class:

- theme-heavy
- mixed session relevance
- render support varies by environment

Common limitations:

- Wayland WMs may expose theme/config targets without exposing global render transforms

## 6. Toolkit/Desktop Export Family

What it compiles:

- GTK exports
- Qt exports
- cursor and icon theme hints
- desktop-policy hint outputs

Typical mode:

- mostly export-only in early 2.x

Typical artifacts:

- toolkit config fragments
- theme metadata exports
- cursor and icon selection hints

Typical capability class:

- theme and typography heavy
- render light or absent

Common limitations:

- does not imply DE-wide ownership
- often cannot claim full apply or repair semantics

## 7. Session/Integration Helper Family

This is a target-like family, but it is not a replacement for `v2/session/`.

What it compiles:

- wrapper fragments
- session helper snippets
- environment export helpers

Typical mode:

- install-capable or apply-capable only when session orchestration explicitly owns the path

Typical artifacts:

- session fragments
- wrapper scripts
- environment files

Common limitations:

- must remain subordinate to session orchestration
- must not invent session policy on its own

## Family Separation Rule

Families remain separate because:

- TTY and terminal targets share palettes but not runtime behavior
- X11 render targets consume render policy that toolkit exports cannot represent
- WM targets may own config fragments while session orchestration owns lifecycle
- toolkit exports may be useful even when apply is not truthful

The adapter layer should respect those differences instead of hiding them behind one generic emitter.

