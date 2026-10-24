#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-grapheme
scratch=$(mktemp -d)
trap 'rmdir "$scratch" 2>/dev/null || true' EXIT
unset PYTHONPATH
cd "$scratch"
python3 - <<'PY'
import importlib.metadata
import pathlib
import subprocess
import grapheme

assert importlib.metadata.version("grapheme") == "0.6.0"
assert grapheme.UNICODE_VERSION == "13.0.0"
path = pathlib.Path(grapheme.__file__).resolve()
assert path.is_absolute() and str(path).startswith("/usr/")
assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(path)], text=True) == "python3-grapheme"
for filename in ("tests/test_mod.py", "tests/benchmark.py", "unicode-data/GraphemeBreakTest.txt", "unicode-data/GraphemeBreakProperty.txt", "unicode-data/emoji-data.txt", "unicode-data/read_property_file.py", "upstream-travis.yml"):
    source = pathlib.Path("/usr/share/python-grapheme/tests") / filename
    assert source.is_file() and not source.is_symlink()
    assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(source)], text=True) == "python3-grapheme"
PY
cp -a /usr/share/python-grapheme/tests/tests /usr/share/python-grapheme/tests/unicode-data .
cmp tests/test_mod.py /usr/share/python-grapheme/tests/tests/test_mod.py
cmp unicode-data/GraphemeBreakTest.txt /usr/share/python-grapheme/tests/unicode-data/GraphemeBreakTest.txt
test ! -e grapheme
python3 -m pytest
python3 -m coverage run --source=grapheme -m pytest
# Leave test and coverage output in the isolated CI scratch directory for diagnostics.
