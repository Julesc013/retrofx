# v2/packs

Purpose:

- home of curated pack metadata, family definitions, pack manifests, style catalogs, and pack-local assets

Implemented now:

- `retrofx.pack/v2alpha1` local pack manifests
- built-in curated packs under stable directories such as `crt-core/` and `modern-minimal/`
- pack-local profile discovery for dev-only resolve, compile, and plan entrypoints
- pack metadata, recommendations, and optional asset references exposed through the dev pipeline

Do implement here later:

- richer family defaults and inheritance hooks
- preview metadata consumers
- local pack install and distribution helpers once the 2.x runtime exists

Do not implement here:

- runtime apply behavior
- planner orchestration
- hidden executable logic inside packs

Current rule:

- packs are local-only and dev-facing in this stage
- pack manifests organize discovery and metadata; they do not apply anything themselves
- the working product line remains 1.x
