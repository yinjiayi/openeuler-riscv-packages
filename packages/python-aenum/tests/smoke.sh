#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-aenum python3-pyparsing
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
module_path=$(python3 - <<'PY'
import os
import aenum
path = os.path.realpath(aenum.__file__)
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert '/site-packages/aenum/' in path, path
print(path)
PY
)
test "$(rpm -qf --qf '%{NAME}\n' -- "$module_path")" = python3-aenum
# Full unmodified installed default, not a loader/discovery substitute.
python3 -m aenum.test
