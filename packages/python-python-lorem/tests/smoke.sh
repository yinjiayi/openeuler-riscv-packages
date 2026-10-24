#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-python-lorem
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import importlib.metadata
import os
import lorem
assert importlib.metadata.version('python-lorem') == '1.3.0.post3'
assert lorem.__version__ == '1.3.0.post3'
path = os.path.realpath(lorem.__file__)
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert path.endswith('/site-packages/lorem.py'), path
print(path)
PY
)
test_path="$(dirname "$module_path")/test_lorem.py"
config=/usr/share/python-python-lorem/tests/.coveragerc
for path in "$module_path" "$test_path" "$config"; do
  test -f "$path"
  test "$(rpm -qf --qf '%{NAME}\n' -- "$path")" = python3-python-lorem
done
# Only unmodified RPM-owned tests/config, never the source library.
cp -- "$test_path" ./test_lorem.py
cp -- "$config" ./.coveragerc
cmp -- "$test_path" ./test_lorem.py
cmp -- "$config" ./.coveragerc
test ! -e ./lorem.py
python3 -m coverage run test_lorem.py
