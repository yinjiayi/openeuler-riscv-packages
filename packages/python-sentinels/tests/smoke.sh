#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-sentinels
cd /tmp
python3 -I - <<'PY'
import copy
import importlib.metadata
import pickle
from sentinels import NOTHING, Sentinel, __version__
from sentinels import _sentinel_unpickler

assert __version__ == importlib.metadata.version('sentinels') == '1.1.1'
assert NOTHING is Sentinel('NOTHING')
assert repr(NOTHING) == '<NOTHING>'
assert NOTHING != None and NOTHING != 'NOTHING' and NOTHING != 2
assert copy.copy(NOTHING) is NOTHING
assert copy.deepcopy(NOTHING) is NOTHING
for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
    assert pickle.loads(pickle.dumps(NOTHING, protocol=protocol)) is NOTHING
other = Sentinel('openEuler-sentinels-smoke')
assert other is _sentinel_unpickler('openEuler-sentinels-smoke', obj_id=123)
assert other is not NOTHING
assert pickle.loads(pickle.dumps(other)) is other
print('installed sentinels version, singleton identity, copy, and pickle semantics passed')
PY
