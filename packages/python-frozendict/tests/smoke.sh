#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-frozendict
python3 - <<'PY'
from importlib.metadata import version
from pathlib import Path
import pickle
import subprocess
import frozendict

assert version("frozendict") == frozendict.__version__ == "2.4.7"
module = Path(frozendict.__file__).resolve()
assert module.is_relative_to(Path("/usr/lib64/python3.11/site-packages"))
owner = subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(module)], text=True)
assert owner == "python3-frozendict"
assert module.with_name("py.typed").is_file()
assert module.with_name("__init__.pyi").is_file()
fd = frozendict.frozendict(a=1, b=2)
assert fd["a"] == 1 and len(fd) == 2
assert fd.set("a", 3)["a"] == 3 and fd["a"] == 1
assert fd.delete("b") == {"a": 1}
assert pickle.loads(pickle.dumps(fd)) == fd
assert hash(fd) == hash(frozendict.frozendict(b=2, a=1))
assert frozendict.deepfreeze({"a": [1, 2]}) == frozendict.frozendict(a=(1, 2))
try:
    fd["a"] = 9
except TypeError:
    pass
else:
    raise AssertionError("frozendict unexpectedly mutable")
print("frozendict installed implementation:", "C" if frozendict.c_ext else "Python")
PY
