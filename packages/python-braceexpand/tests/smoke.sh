#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-braceexpand
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import os
import braceexpand
path = os.path.realpath(braceexpand.__file__)
assert braceexpand.__version__ == '0.1.7', braceexpand.__version__
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert '/site-packages/braceexpand/' in path, path
print(path)
PY
)
module_dir=$(dirname -- "$module_path")
test_file=/usr/share/python-braceexpand/tests/test_braceexpand.py
for path in "$module_path" "$module_dir/__init__.pyi" "$module_dir/py.typed" "$test_file"; do
  test -f "$path"
  test "$(rpm -qf --qf '%{NAME}\n' -- "$path")" = python3-braceexpand
done
# The original module-main preserves its doctest flags and failure exit.
python3 "$module_path"
# Exact original standalone unittest, importing the installed RPM-owned module.
python3 "$test_file"
