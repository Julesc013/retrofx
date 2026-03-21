"""Code-side interface contracts for the current experimental 2.x branch."""

from __future__ import annotations

RESOLVED_PROFILE_TOP_LEVEL_KEYS = (
    "schema",
    "source",
    "pack",
    "implementation",
    "identity",
    "semantics",
    "target_requests",
    "capability_context",
    "target_plan",
    "artifact_plan",
    "decisions",
)

RESOLVED_PROFILE_SEMANTICS_KEYS = (
    "color",
    "typography",
    "render",
    "chrome",
    "session",
)

RESOLVED_PROFILE_DECISIONS_KEYS = (
    "warnings",
    "errors",
    "normalization",
    "notes",
)

TARGET_ARTIFACT_KEYS = (
    "target_name",
    "file_name",
    "relative_path",
    "output_path",
    "content_sha256",
    "byte_count",
)

TARGET_COMPILE_RESULT_KEYS = (
    "target_name",
    "family_name",
    "mode",
    "output_dir",
    "artifacts",
    "consumed_sections",
    "ignored_sections",
    "warnings",
    "notes",
)

SESSION_PLAN_KEYS = (
    "requested_targets",
    "implemented_targets",
    "implemented_target_families",
    "implemented_target_classes",
    "session_policy",
    "display_policy",
    "x11_render",
    "toolkit_style",
    "environment_capabilities",
    "family_plans",
    "target_entries",
    "compile_targets",
    "export_only_targets",
    "apply_preview_targets",
    "degraded_targets",
    "skipped_targets",
    "warnings",
    "notes",
)

SESSION_PLAN_ENTRY_KEYS = (
    "kind",
    "target_name",
    "family_name",
    "supported_target_classes",
    "requested_by",
    "status_class",
    "plan_action",
    "current_implementation_mode",
    "apply_preview_candidate",
    "reasons",
    "warnings",
)

CURRENT_STATE_KEYS = (
    "schema",
    "active",
    "profile",
    "pack",
    "bundle",
    "activation",
    "manifest",
    "cleanup",
    "warnings",
    "layout",
)

ACTIVATION_MANIFEST_KEYS = (
    "schema",
    "activation_id",
    "activated_at",
    "profile",
    "source",
    "pack",
    "environment",
    "bundle",
    "activation",
    "plan_summary",
    "cleanup",
    "previous_state",
    "warnings",
    "notes",
    "preview_probe",
)

PACK_MANIFEST_KEYS = (
    "schema",
    "id",
    "name",
    "description",
    "family",
    "tags",
    "author",
    "source",
    "root",
    "manifest_path",
    "profiles",
    "assets",
    "recommendations",
)

PACK_PROFILE_ENTRY_KEYS = (
    "id",
    "name",
    "description",
    "family",
    "tags",
    "relative_path",
    "path",
)

MIGRATION_REPORT_KEYS = (
    "legacy_profile",
    "mapping_contract",
    "proposed_identity",
    "mapping_summary",
    "mapped_cleanly",
    "mapped_with_degradation",
    "requires_manual_follow_up",
    "unsupported_or_ignored",
    "warnings",
    "draft_profile",
    "draft_validation",
)

MIGRATION_SUMMARY_KEYS = (
    "mapped_cleanly",
    "mapped_with_degradation",
    "requires_manual_follow_up",
    "unsupported_or_ignored",
)

INSTALL_RECORD_KEYS = (
    "schema",
    "install_name",
    "bundle_id",
    "installed_at",
    "profile",
    "pack",
    "source_bundle",
    "install_roots",
    "install_targets",
    "owned_paths",
    "launcher",
    "notes",
)

IMPLEMENTED_INTERFACES = (
    {
        "name": "resolved-profile",
        "producer": "v2.core.resolution.build_resolved_profile",
        "consumer": "target compilers, session planning, bundle and apply flows",
        "stability": "experimental-internal",
        "required_keys": RESOLVED_PROFILE_TOP_LEVEL_KEYS,
        "notes": "Consumes normalized pipeline output only. Capability filtering and artifact planning are still placeholder sections inside this shape.",
    },
    {
        "name": "target-compile-result",
        "producer": "v2.targets.interfaces.TargetCompileResult",
        "consumer": "compile, bundle, plan, and apply surfaces",
        "stability": "experimental-internal",
        "required_keys": TARGET_COMPILE_RESULT_KEYS,
        "notes": "Compilers must consume resolved profile data rather than raw authored TOML.",
    },
    {
        "name": "session-plan",
        "producer": "v2.session.planning.build_session_plan",
        "consumer": "plan, bundle, apply, preview, and status surfaces",
        "stability": "experimental-internal",
        "required_keys": SESSION_PLAN_KEYS,
        "notes": "Preview-oriented. Categories must remain explicit for compile, export-only, apply-preview, degraded, and skipped outcomes.",
    },
    {
        "name": "activation-state",
        "producer": "v2.session.apply.apply_dev_profile",
        "consumer": "off, status, and later repair or validation work",
        "stability": "experimental-internal",
        "required_keys": CURRENT_STATE_KEYS,
        "notes": "Tracks only the 2.x-owned bounded activation footprint.",
    },
    {
        "name": "activation-manifest",
        "producer": "v2.session.apply.apply_dev_profile",
        "consumer": "off, status, last-good, and future repair flows",
        "stability": "experimental-internal",
        "required_keys": ACTIVATION_MANIFEST_KEYS,
        "notes": "Machine-readable record of one bounded TWO-19 activation.",
    },
    {
        "name": "pack-manifest",
        "producer": "v2.packs.load_pack_manifest",
        "consumer": "pack inspection and pack-aware profile resolution",
        "stability": "experimental-internal",
        "required_keys": PACK_MANIFEST_KEYS,
        "notes": "Local-only `retrofx.pack/v2alpha1` contract; no network registry behavior is implied.",
    },
    {
        "name": "migration-report",
        "producer": "v2.compat.inspect_legacy_profile",
        "consumer": "migration inspection and draft-generation tooling",
        "stability": "experimental-internal",
        "required_keys": MIGRATION_REPORT_KEYS,
        "notes": "Must distinguish clean, degraded, manual, and unsupported mappings explicitly.",
    },
    {
        "name": "install-record",
        "producer": "v2.session.install.install_dev_bundle",
        "consumer": "install status, uninstall, and apply reuse of installed bundles",
        "stability": "experimental-internal",
        "required_keys": INSTALL_RECORD_KEYS,
        "notes": "User-local only. Does not imply live session ownership or 1.x replacement.",
    },
)
