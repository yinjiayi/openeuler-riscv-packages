#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-addict
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
unset PYTHONPATH
module_path=$(python3 - <<'PY'
import os
import addict
path = os.path.realpath(addict.__file__)
assert addict.__version__ == '2.4.0', addict.__version__
assert path.startswith(('/usr/lib/python3', '/usr/lib64/python3')), path
assert '/site-packages/addict/' in path, path
print(path)
PY
)
module_dir=$(dirname -- "$module_path")
test_file=/usr/share/python-addict/tests/test_addict.py
for path in "$module_path" "$module_dir/addict.py" "$test_file"; do
  test -f "$path"
  test "$(rpm -qf --qf '%{NAME}\n' -- "$path")" = python3-addict
done
# Copy only the unmodified RPM-owned test, never the library, to fresh scratch.
cp -- "$test_file" ./test_addict.py
cmp -- "$test_file" ./test_addict.py
# Original defaults collect both concrete classes and import installed code.
python3 -m pytest
python3 -m unittest -v test_addict
