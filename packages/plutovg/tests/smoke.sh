#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
out=$(mktemp -d /tmp/plutovg-installed-XXXXXX)
python3 /usr/share/plutovg-tests/run-qa.py --prefix /usr --phase installed --output "$out/evidence" --font-contract /usr/share/plutovg-tests/font-input.json
