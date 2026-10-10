#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-crccheck
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cd "$smoke_dir"
unset PYTHONPATH PYTHONHOME
module_path=$(python3 -c 'import crccheck; print(crccheck.__file__)')
case "$module_path" in
  /usr/lib/python3*/site-packages/crccheck/__init__.py) ;;
  *) printf 'Unexpected module path: %s\n' "$module_path" >&2; exit 1 ;;
esac
test "$(rpm -qf --qf '%{NAME}' -- "$module_path")" = python3-crccheck
python3 - <<'PY'
from importlib.metadata import version
from crccheck.crc import Crc32IsoHdlc, Crc16Xmodem
assert version('crccheck') == '1.3.1'
assert Crc32IsoHdlc.calc(b'123456789') == 0xCBF43926
assert Crc16Xmodem.calc(b'123456789') == 0x31C3
PY
printf '123456789' > vector
test "$(python3 -m crccheck Crc32IsoHdlc -H vector)" = 0xCBF43926
# Copy only original tests/config, never the source module: imports resolve to RPM.
cp -a /usr/share/python-crccheck/tests .
cp /usr/share/python-crccheck/.coveragerc .
export COVERAGE_FILE="$smoke_dir/.coverage-installed"
# Coverage defaults exclude site-packages; explicitly measure the RPM-owned tree.
python3 -m coverage run --branch --source="${module_path%/__init__.py}" -m unittest discover
python3 -m coverage report
python3 -m coverage html
