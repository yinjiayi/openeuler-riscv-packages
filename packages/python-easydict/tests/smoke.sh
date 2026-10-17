#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-easydict
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import importlib.metadata
import os
import easydict
assert importlib.metadata.version('easydict') == '1.13'
path = os.path.realpath(easydict.__file__)
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert '/site-packages/easydict/' in path, path
print(path)
PY
)
test -f "$module_path"
test "$(rpm -qf --qf '%{NAME}\n' -- "$module_path")" = python3-easydict
# Complete unchanged original script against RPM-owned installed bytes.
python3 "$module_path" -v
# Complete original doctests, now with an explicit nonzero failure exit.
python3 -m doctest -v "$module_path"
