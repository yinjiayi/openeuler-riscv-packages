#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-littleutils
python3 - <<'PY'
from importlib.metadata import version
from littleutils import HelpfulErrorDict, only, group_by_key_func, strip_required_prefix
assert version("littleutils") == "0.2.4"
assert only(iter([7])) == 7
assert HelpfulErrorDict({"a": 3})["a"] == 3
assert group_by_key_func(["a", "bb", "c"], len) == {1: ["a", "c"], 2: ["bb"]}
assert strip_required_prefix("openeuler-riscv", "openeuler-") == "riscv"
PY
