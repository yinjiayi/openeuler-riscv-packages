#!/usr/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors.
# Full license is installed in /usr/share/licenses/sfsexp/Apache-2.0.txt.
set -euo pipefail
cd /usr/share/licenses/sfsexp/source-notices
sha256sum -c SHA256SUMS
cd /usr/share/sfsexp-tests
sha256sum -c SHA256SUMS
exec python3 /usr/share/sfsexp-tests/run-qa.py installed /usr/share/sfsexp-tests
