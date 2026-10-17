#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-pylev
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import importlib.metadata
import os
import pylev
assert importlib.metadata.version('pylev') == '1.4.0'
assert pylev.__version__ == (1, 4, 0)
path = os.path.realpath(pylev.__file__)
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert path.endswith('/site-packages/pylev/__init__.py'), path
print(path)
PY
)
test_file=/usr/share/python-pylev/tests/tests.py
for path in "$module_path" "$test_file"; do
  test -f "$path"
  test "$(rpm -qf --qf '%{NAME}\n' -- "$path")" = python3-pylev
done
test "$(sha256sum -- "$test_file" | cut -d ' ' -f 1)" = c5b78b0597aec0780a28547b690dd2f7d9fe2cc9a65c6d9f463dca8f9e9a6386
# Only the original test is copied; imports must resolve to the installed RPM.
cp -- "$test_file" ./tests.py
cmp -- "$test_file" ./tests.py
test ! -e ./pylev
python3 tests.py
