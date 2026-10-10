#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-boolean-py
cd /tmp
python3 - <<'PY'
import importlib.metadata
from pathlib import Path
import subprocess
import boolean

assert importlib.metadata.version("boolean.py") == "5.0"
installed = Path(boolean.__file__).resolve()
owner = subprocess.check_output(
    ["rpm", "-qf", "--queryformat", "%{NAME}\n", "--", str(installed)], text=True
).strip()
assert owner == "python3-boolean-py"
algebra = boolean.BooleanAlgebra()
first = algebra.parse("apple and (oranges or banana) and not banana", simplify=False)
second = algebra.parse("(oranges | banana) and not banana & apple", simplify=True)
assert first != second
assert first.simplify() == second
assert algebra.parse("a | (a & b)", simplify=True) == algebra.parse("a")
assert algebra.parse("~(a & b)").demorgan() == algebra.parse("~a | ~b")
print("boolean.py 5.0 installed-package API smoke passed")
PY
