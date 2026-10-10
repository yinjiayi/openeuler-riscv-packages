#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-dpath
python3 - <<'PY'
from importlib.metadata import version
from pathlib import Path
import dpath
from dpath.version import VERSION

assert version("dpath") == VERSION == "2.2.0"
assert Path(dpath.__file__).resolve().is_relative_to(Path("/usr/lib/python3.11/site-packages"))
assert Path(dpath.__file__).with_name("py.typed").is_file()
data = {"a": {"b": 1, "c": 2}}
assert dpath.get(data, "a/b") == 1
assert dpath.values(data, "a/*") == [1, 2]
assert dpath.set(data, "a/*", 3) == 2
assert data == {"a": {"b": 3, "c": 3}}
dpath.new(data, "a/d", 4)
assert dpath.get(data, "a/d") == 4
assert dpath.delete(data, "a/c") == 1
assert data == {"a": {"b": 3, "d": 4}}
destination = {"a": {"x": 1}}
dpath.merge(destination, {"a": {"y": 2}})
assert destination == {"a": {"x": 1, "y": 2}}
PY
