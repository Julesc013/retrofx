#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"

if [[ "${PYTHONPATH:-}" == "" ]]; then
  export PYTHONPATH="${repo_root}"
else
  export PYTHONPATH="${repo_root}:${PYTHONPATH}"
fi

cd "${repo_root}"
exec python3 -m unittest -v v2.tests.test_v2_core

