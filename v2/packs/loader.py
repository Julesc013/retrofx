"""Local built-in pack discovery for the experimental RetroFX 2.x scaffold."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib
from typing import Any, Mapping

from v2.core.load import load_profile_document
from v2.core.models.types import Issue, RawProfile

PACK_SCHEMA = "retrofx.pack/v2alpha1"
PACK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
PACK_TOP_LEVEL_KEYS = {"schema", "pack", "profiles", "assets", "recommendations"}
PACK_METADATA_KEYS = {"id", "name", "description", "family", "tags", "author", "source"}
PACK_PROFILE_KEYS = {"id", "file", "name", "description", "family", "tags"}
DEFAULT_PACKS_ROOT = Path(__file__).resolve().parent


class PackLoadError(Exception):
    """Raised when a 2.x pack manifest or profile cannot be resolved."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(issue.message)
        self.issue = issue


def discover_packs(packs_root: str | Path | None = None) -> list[dict[str, Any]]:
    root = _coerce_packs_root(packs_root)
    manifests: list[dict[str, Any]] = []

    if not root.is_dir():
        return manifests

    for candidate in sorted(root.iterdir(), key=lambda item: item.name):
        if not candidate.is_dir():
            continue
        manifest_path = candidate / "pack.toml"
        if manifest_path.is_file():
            manifests.append(load_pack_manifest(candidate.name, packs_root=root))

    return sorted(manifests, key=lambda manifest: manifest["id"])


def load_pack_manifest(pack_id: str, packs_root: str | Path | None = None) -> dict[str, Any]:
    root = _coerce_packs_root(packs_root)
    manifest_path = root / pack_id / "pack.toml"
    if not manifest_path.is_file():
        raise PackLoadError(
            Issue(
                severity="error",
                code="pack-manifest-missing",
                message=f"Pack manifest does not exist for `{pack_id}` under {root}.",
                path="pack",
            )
        )

    try:
        with manifest_path.open("rb") as handle:
            document = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise PackLoadError(
            Issue(
                severity="error",
                code="pack-toml-parse-error",
                message=str(exc),
                path="pack",
            )
        ) from exc

    if not isinstance(document, dict):
        raise PackLoadError(
            Issue(
                severity="error",
                code="invalid-pack-document",
                message="Pack manifest root must be a TOML table.",
                path="pack",
            )
        )

    return _normalize_pack_manifest(document, manifest_path)


def load_pack_profile_document(
    pack_id: str,
    profile_id: str,
    *,
    packs_root: str | Path | None = None,
) -> RawProfile:
    manifest = load_pack_manifest(pack_id, packs_root=packs_root)
    entry = next((profile for profile in manifest["profiles"] if profile["id"] == profile_id), None)
    if entry is None:
        raise PackLoadError(
            Issue(
                severity="error",
                code="pack-profile-missing",
                message=f"Profile `{profile_id}` does not exist in pack `{pack_id}`.",
                path="profiles",
            )
        )

    origin = {
        "type": "pack",
        "profile_path": entry["path"],
        "profile_dir": str(Path(entry["path"]).parent),
        "profile_id": entry["id"],
        "profile_relative_path": entry["relative_path"],
        "pack": _pack_summary(manifest),
        "pack_profile": {
            "id": entry["id"],
            "name": entry["name"],
            "description": entry["description"],
            "family": entry["family"],
            "tags": entry["tags"],
        },
    }
    return load_profile_document(entry["path"], origin=origin)


def _normalize_pack_manifest(document: Mapping[str, Any], manifest_path: Path) -> dict[str, Any]:
    _reject_unknown_keys(document, PACK_TOP_LEVEL_KEYS, "pack")

    schema = document.get("schema")
    if not isinstance(schema, str) or schema.strip() != PACK_SCHEMA:
        raise PackLoadError(
            Issue(
                severity="error",
                code="unsupported-pack-schema",
                message=f"`schema` must be `{PACK_SCHEMA}` in a 2.x pack manifest.",
                path="schema",
            )
        )

    raw_pack = document.get("pack")
    if not isinstance(raw_pack, Mapping):
        raise PackLoadError(
            Issue(
                severity="error",
                code="missing-pack-table",
                message="Pack manifests require a `[pack]` table.",
                path="pack",
            )
        )
    _reject_unknown_keys(raw_pack, PACK_METADATA_KEYS, "pack")

    pack_id = _require_identifier(raw_pack.get("id"), "pack.id")
    name = _require_non_empty_string(raw_pack.get("name"), "pack.name")
    description = _optional_string(raw_pack.get("description"))
    family = _optional_string(raw_pack.get("family"))
    tags = _normalize_tags(raw_pack.get("tags"), "pack.tags")
    author = _optional_string(raw_pack.get("author"))
    source = _optional_string(raw_pack.get("source")) or "builtin-local"

    expected_dir = manifest_path.parent.name
    if pack_id != expected_dir:
        raise PackLoadError(
            Issue(
                severity="error",
                code="pack-id-directory-mismatch",
                message=f"`pack.id` `{pack_id}` must match directory `{expected_dir}`.",
                path="pack.id",
            )
        )

    profiles = _normalize_pack_profiles(document.get("profiles"), manifest_path.parent)
    assets = _normalize_assets(document.get("assets"), manifest_path.parent)
    recommendations = _normalize_recommendations(document.get("recommendations"))

    return {
        "schema": PACK_SCHEMA,
        "id": pack_id,
        "name": name,
        "description": description,
        "family": family,
        "tags": tags,
        "author": author,
        "source": source,
        "root": str(manifest_path.parent.resolve()),
        "manifest_path": str(manifest_path.resolve()),
        "profiles": profiles,
        "assets": assets,
        "recommendations": recommendations,
    }


def _normalize_pack_profiles(raw_profiles: Any, pack_root: Path) -> list[dict[str, Any]]:
    if not isinstance(raw_profiles, list) or not raw_profiles:
        raise PackLoadError(
            Issue(
                severity="error",
                code="missing-pack-profiles",
                message="Pack manifests require at least one `[[profiles]]` entry.",
                path="profiles",
            )
        )

    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(raw_profiles):
        path_prefix = f"profiles[{index}]"
        if not isinstance(entry, Mapping):
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="invalid-pack-profile-entry",
                    message=f"`{path_prefix}` must be a table.",
                    path=path_prefix,
                )
            )

        _reject_unknown_keys(entry, PACK_PROFILE_KEYS, path_prefix)
        profile_id = _require_identifier(entry.get("id"), f"{path_prefix}.id")
        if profile_id in seen_ids:
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="duplicate-pack-profile-id",
                    message=f"Duplicate pack profile id `{profile_id}` in pack manifest.",
                    path=f"{path_prefix}.id",
                )
            )
        seen_ids.add(profile_id)

        relative_path = _require_non_empty_string(entry.get("file"), f"{path_prefix}.file")
        profile_path = _resolve_relative_path(relative_path, pack_root, f"{path_prefix}.file")
        if profile_path.suffix.lower() != ".toml":
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="invalid-pack-profile-extension",
                    message=f"`{path_prefix}.file` must point to a TOML profile.",
                    path=f"{path_prefix}.file",
                )
            )
        if not profile_path.is_file():
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="missing-pack-profile-file",
                    message=f"Referenced pack profile does not exist: {profile_path}",
                    path=f"{path_prefix}.file",
                )
            )

        normalized.append(
            {
                "id": profile_id,
                "name": _optional_string(entry.get("name")) or profile_id,
                "description": _optional_string(entry.get("description")),
                "family": _optional_string(entry.get("family")),
                "tags": _normalize_tags(entry.get("tags"), f"{path_prefix}.tags", allow_missing=True),
                "relative_path": relative_path,
                "path": str(profile_path),
            }
        )

    return sorted(normalized, key=lambda entry: entry["id"])


def _normalize_assets(raw_assets: Any, pack_root: Path) -> dict[str, str]:
    if raw_assets is None:
        return {}
    if not isinstance(raw_assets, Mapping):
        raise PackLoadError(
            Issue(
                severity="error",
                code="invalid-pack-assets",
                message="`[assets]` must be a table when provided.",
                path="assets",
            )
        )

    normalized: dict[str, str] = {}
    for key in sorted(raw_assets):
        value = raw_assets[key]
        if not isinstance(key, str) or not key.strip():
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="invalid-pack-asset-key",
                    message="Pack asset keys must be non-empty strings.",
                    path="assets",
                )
            )
        if not isinstance(value, str) or not value.strip():
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="invalid-pack-asset-path",
                    message=f"`assets.{key}` must be a non-empty relative path string.",
                    path=f"assets.{key}",
                )
            )

        asset_path = _resolve_relative_path(value, pack_root, f"assets.{key}")
        if not asset_path.exists():
            raise PackLoadError(
                Issue(
                    severity="error",
                    code="missing-pack-asset",
                    message=f"Referenced pack asset does not exist: {asset_path}",
                    path=f"assets.{key}",
                )
            )
        normalized[key.strip()] = str(asset_path)

    return normalized


def _normalize_recommendations(raw_recommendations: Any) -> dict[str, Any]:
    if raw_recommendations is None:
        return {}
    if not isinstance(raw_recommendations, Mapping):
        raise PackLoadError(
            Issue(
                severity="error",
                code="invalid-pack-recommendations",
                message="`[recommendations]` must be a table when provided.",
                path="recommendations",
            )
        )
    return _mapping_to_plain_dict(raw_recommendations)


def _pack_summary(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": manifest["id"],
        "name": manifest["name"],
        "description": manifest["description"],
        "family": manifest["family"],
        "tags": manifest["tags"],
        "author": manifest["author"],
        "source": manifest["source"],
        "manifest_path": manifest["manifest_path"],
        "root": manifest["root"],
        "assets": manifest["assets"],
        "recommendations": manifest["recommendations"],
        "profile_count": len(manifest["profiles"]),
    }


def _coerce_packs_root(packs_root: str | Path | None) -> Path:
    return (Path(packs_root).expanduser() if packs_root is not None else DEFAULT_PACKS_ROOT).resolve()


def _reject_unknown_keys(mapping: Mapping[str, Any], allowed: set[str], path: str) -> None:
    unknown = sorted(key for key in mapping if key not in allowed)
    if unknown:
        raise PackLoadError(
            Issue(
                severity="error",
                code="unknown-pack-key",
                message=f"Unsupported keys under `{path}`: {', '.join(unknown)}.",
                path=path,
            )
        )


def _require_identifier(value: Any, path: str) -> str:
    normalized = _require_non_empty_string(value, path).lower()
    if PACK_ID_RE.match(normalized) is None:
        raise PackLoadError(
            Issue(
                severity="error",
                code="invalid-pack-identifier",
                message=f"`{path}` must match `^[a-z0-9][a-z0-9-]{{1,63}}$`.",
                path=path,
            )
        )
    return normalized


def _require_non_empty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackLoadError(
            Issue(
                severity="error",
                code="missing-pack-string",
                message=f"`{path}` is required and must be a non-empty string.",
                path=path,
            )
        )
    return value.strip()


def _optional_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def _normalize_tags(value: Any, path: str, *, allow_missing: bool = False) -> list[str]:
    if value is None and allow_missing:
        return []
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise PackLoadError(
            Issue(
                severity="error",
                code="invalid-pack-tags",
                message=f"`{path}` must be a list of non-empty strings.",
                path=path,
            )
        )
    return sorted({item.strip() for item in value})


def _resolve_relative_path(relative_path: str, root: Path, path: str) -> Path:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise PackLoadError(
            Issue(
                severity="error",
                code="pack-path-escape",
                message=f"`{path}` must stay within pack root {root.resolve()}.",
                path=path,
            )
        ) from exc
    return candidate


def _mapping_to_plain_dict(value: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key in sorted(value):
        item = value[key]
        if isinstance(item, Mapping):
            normalized[str(key)] = _mapping_to_plain_dict(item)
        elif isinstance(item, list):
            normalized[str(key)] = [
                _mapping_to_plain_dict(entry) if isinstance(entry, Mapping) else entry for entry in item
            ]
        else:
            normalized[str(key)] = item
    return normalized
