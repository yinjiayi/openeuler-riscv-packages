#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-shortuuid
# Run the same entire original suite against the installed modules.
python3 -m unittest -v shortuuid.test_shortuuid
python3 - <<'PY'
from importlib.metadata import version
from uuid import UUID
import shortuuid

assert version('shortuuid') == '1.0.13'
# Preserve the release's stale import constant; do not falsify its value.
assert shortuuid.__version__ == '1.0.11'
value = UUID('3b1f8b40-222c-4a6e-b77e-779d5a94e21c')
assert shortuuid.encode(value) == 'CXc85b4rqinB7s5J52TRYb'
assert shortuuid.decode(shortuuid.encode(value)) == value
PY
test "$(shortuuid encode 3b1f8b40-222c-4a6e-b77e-779d5a94e21c)" = 'CXc85b4rqinB7s5J52TRYb'
test "$(shortuuid decode CXc85b4rqinB7s5J52TRYb)" = '3b1f8b40-222c-4a6e-b77e-779d5a94e21c'
