# RetroFX 2.x Principles

These principles are the architecture constitution for future 2.x prompts.
If a proposed implementation violates them, the proposal needs stronger justification than convenience.

## Constitution

### 1. One Resolved Profile Model Before Backend Compilation

All target compilers start from one resolved profile model.
Backend-specific config shapes come later.

### 2. Explicit Capability Typing

Support claims must be backed by declared capabilities in named domains.
No adapter gets to imply support informally.

### 3. Theme, Render, And Session Are Separate Concerns

Theme output, render transforms, and session orchestration may interact, but they are not the same module and should not collapse into one another.

### 4. Truthful Degradation

When a target cannot satisfy requested intent, RetroFX degrades explicitly.
It does not silently pretend the request succeeded.

### 5. Boring Core, Flexible Edges

The core should be stable, deterministic, and conservative.
Target adapters and packs are where environment-specific variety belongs.

### 6. Deterministic Generation

The same resolved profile and target plan should generate the same artifacts.
Nondeterminism is a bug unless explicitly justified.

### 7. Minimal Surprises

RetroFX should prefer explicit plans, explicit scope, and explicit output ownership over clever implicit behavior.

### 8. No Hidden Global Side Effects

Global or system-wide mutation is never assumed.
If a target requires broader integration, that scope must be explicit and recoverable.

### 9. Install, Apply, Off, And Repair Must Remain Trustworthy

Lifecycle operations are part of the product, not polish.
A target that cannot be disabled or repaired cleanly should not claim stronger support than it deserves.

### 10. Prefer Declarative Profiles Over Ad Hoc Imperative Hacks

New capability should usually be expressed through profile intent, tokens, and adapters rather than backend-specific scripting branches in the core.

### 11. Do Not Widen Target Promises Without An Explicit Capability Path

A new target or stronger support claim requires capability declarations, degradation behavior, lifecycle rules, and documentation.
Marketing language is not architecture.

### 12. Session-Local By Default

User-scoped and session-scoped behavior is the default posture.
Broader system ownership requires clear justification and recovery design.

### 13. Packs Are Data Products

Packs may be rich and opinionated, but they should remain inspectable data with metadata and previews, not arbitrary executable extension points.

### 14. Logs And Plans Over Guesswork

RetroFX should be able to explain what it intended to do and what it actually did.
When behavior is hard to explain, the design is probably too implicit.

