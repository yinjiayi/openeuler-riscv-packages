#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-sexpdata
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import importlib.metadata
import os
import sexpdata
assert importlib.metadata.version('sexpdata') == '1.0.2'
assert sexpdata.__version__ == '1.0.2'
path = os.path.realpath(sexpdata.__file__)
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert path.endswith('/site-packages/sexpdata.py'), path
print(path)
PY
)
test_file=/usr/share/python-sexpdata/tests/test_sexpdata.py
for path in "$module_path" "$test_file"; do
  test -f "$path"
  test "$(rpm -qf --qf '%{NAME}\n' -- "$path")" = python3-sexpdata
done
# Copy only the complete original RPM-owned test, never a source library.
cp -- "$test_file" ./test_sexpdata.py
cmp -- "$test_file" ./test_sexpdata.py
test ! -e ./sexpdata.py
# Complete original current-workflow unit suite plus installed-module doctests.
python3 -m pytest --doctest-modules "$module_path" test_sexpdata.py
