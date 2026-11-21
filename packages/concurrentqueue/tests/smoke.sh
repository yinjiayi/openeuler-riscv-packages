#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
out=$(mktemp -d /tmp/concurrentqueue-installed-XXXXXX)
python3 /usr/share/concurrentqueue-tests/run-qa.py --prefix /usr --phase installed --output "$out/evidence"
