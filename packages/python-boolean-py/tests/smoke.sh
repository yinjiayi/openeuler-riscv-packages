#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-boolean-py
cd /tmp
python3 - <<'PY'
import importlib.metadata
from pathlib import Path
import sysconfig
import boolean

assert importlib.metadata.version("boolean.py") == "5.0"
installed = Path(boolean.__file__).resolve()
assert installed.is_relative_to(Path(sysconfig.get_path("purelib")).resolve())
algebra = boolean.BooleanAlgebra()
first = algebra.parse("apple and (oranges or banana) and not banana", simplify=False)
second = algebra.parse("(oranges | banana) and not banana & apple", simplify=True)
assert first != second
assert first.simplify() == second
assert algebra.parse("a | (a & b)", simplify=True) == algebra.parse("a")
assert algebra.parse("~(a & b)", simplify=True) == algebra.parse("~a | ~b", simplify=True)
print("boolean.py 5.0 installed-package API smoke passed")
PY
