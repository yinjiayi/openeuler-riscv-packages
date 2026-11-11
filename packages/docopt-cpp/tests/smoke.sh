#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
set -euo pipefail
qa=/usr/share/docopt-cpp-tests
(cd "$qa" && sha256sum -c SHA256SUMS)
work=$(mktemp -d /tmp/docopt-cpp-smoke.XXXXXX)
exec python3 "$qa/run-qa.py" --root / --output "$work/results"
