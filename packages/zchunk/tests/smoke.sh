#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
set -euo pipefail
qa=/usr/share/zchunk-tests
(cd "$qa" && sha256sum -c SHA256SUMS)
python3 - <<'PY_NOTICES'
import base64,hashlib,json
from pathlib import Path
p=Path('/usr/share/licenses/zchunk/source-notices');original=json.loads((p/'original-manifest.json').read_text());assert len(original)==166
for name,row in original.items():
    b=(p/(name+'.notice')).read_bytes()
    if row['encoding']=='base64':
        value=json.loads(b);assert value['encoding']=='base64' and value['original_Git_mode']==row['Git_mode'];b=base64.b64decode(value['data'],validate=True)
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],name
PY_NOTICES
work=$(mktemp -d /tmp/zchunk-smoke.XXXXXX)
exec python3 "$qa/run-qa.py" --output "$work/results"
