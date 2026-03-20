#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="$ROOT_DIR/VERSION"

log() {
  printf '[release-package] %s\n' "$*"
}

die() {
  printf '[release-package][error] %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/release-package.sh [--ref <git-ref>] [--out-dir <dir>]

Default behavior packages the current tracked working tree into deterministic
source archives under state/releases/<version>/.

Options:
  --ref <git-ref>   Package the files from a committed git ref instead of the working tree.
  --out-dir <dir>   Write archives into the given directory.
USAGE
}

read_version() {
  local version=""
  [[ -f "$VERSION_FILE" ]] || die "VERSION file not found"
  IFS= read -r version <"$VERSION_FILE" || true
  version="${version%$'\r'}"
  [[ -n "$version" ]] || die "VERSION file is empty"
  printf '%s' "$version"
}

collect_worktree_file_list() {
  git -C "$ROOT_DIR" ls-files -z
}

collect_ref_file_list() {
  local ref="$1"
  git -C "$ROOT_DIR" ls-tree -r --name-only -z "$ref"
}

write_tarball() {
  local list_file="$1"
  local prefix="$2"
  local epoch="$3"
  local out_path="$4"

  tar \
    --directory="$ROOT_DIR" \
    --null \
    --files-from="$list_file" \
    --transform="s|^|$prefix/|" \
    --sort=name \
    --mtime="@$epoch" \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    -cf - | gzip -n >"$out_path"
}

write_zip_from_worktree() {
  local list_file="$1"
  local prefix="$2"
  local epoch="$3"
  local out_path="$4"

  python3 - "$ROOT_DIR" "$list_file" "$prefix" "$epoch" "$out_path" <<'PY'
import os
import stat
import sys
import time
import zipfile

root_dir, list_path, prefix, epoch_s, out_path = sys.argv[1:]
epoch = int(epoch_s)
dt = time.gmtime(epoch)[:6]

with open(list_path, "rb") as fh:
    names = [item.decode("utf-8") for item in fh.read().split(b"\0") if item]

names.sort()

with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for rel_path in names:
        full_path = os.path.join(root_dir, rel_path)
        st = os.stat(full_path)
        info = zipfile.ZipInfo(f"{prefix}/{rel_path}", dt)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (stat.S_IMODE(st.st_mode) | stat.S_IFREG) << 16
        with open(full_path, "rb") as source:
            zf.writestr(info, source.read())
PY
}

write_zip_from_ref() {
  local ref="$1"
  local prefix="$2"
  local out_path="$3"

  git -C "$ROOT_DIR" archive --format=zip --prefix="$prefix/" -o "$out_path" "$ref"
}

write_checksums() {
  local out_path="$1"
  sha256sum "$(basename "$out_path")" >"$(basename "$out_path").sha256"
}

main() {
  local version=""
  local ref=""
  local out_dir=""
  local epoch=""
  local prefix=""
  local tar_path=""
  local zip_path=""
  local tmp_list=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --ref)
        [[ $# -ge 2 ]] || die "--ref requires a git ref"
        ref="$2"
        shift 2
        ;;
      --out-dir)
        [[ $# -ge 2 ]] || die "--out-dir requires a directory"
        out_dir="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        die "unknown option: $1"
        ;;
    esac
  done

  version="$(read_version)"
  prefix="retrofx-$version"
  if [[ -z "$out_dir" ]]; then
    out_dir="$ROOT_DIR/state/releases/$version"
  fi
  mkdir -p "$out_dir"

  if [[ -n "$ref" ]]; then
    git -C "$ROOT_DIR" rev-parse --verify "$ref^{commit}" >/dev/null 2>&1 || die "git ref not found: $ref"
    epoch="$(git -C "$ROOT_DIR" log -1 --format=%ct "$ref")"
  else
    epoch="$(git -C "$ROOT_DIR" log -1 --format=%ct HEAD)"
  fi

  tar_path="$out_dir/$prefix-src.tar.gz"
  zip_path="$out_dir/$prefix-src.zip"
  tmp_list="$(mktemp)"

  if [[ -n "$ref" ]]; then
    collect_ref_file_list "$ref" >"$tmp_list"
  else
    collect_worktree_file_list >"$tmp_list"
  fi

  write_tarball "$tmp_list" "$prefix" "$epoch" "$tar_path"
  if [[ -n "$ref" ]]; then
    write_zip_from_ref "$ref" "$prefix" "$zip_path"
  else
    write_zip_from_worktree "$tmp_list" "$prefix" "$epoch" "$zip_path"
  fi

  (
    cd "$out_dir"
    write_checksums "$tar_path"
    write_checksums "$zip_path"
  )

  rm -f "$tmp_list"

  log "version: $version"
  if [[ -n "$ref" ]]; then
    log "source: git ref $ref"
  else
    log "source: tracked working tree"
  fi
  log "wrote $tar_path"
  log "wrote $zip_path"
}

main "$@"
