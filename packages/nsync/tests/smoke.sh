#!/bin/bash
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C LANG=C
exec python3 /usr/share/nsync-tests/run-qa.py --prefix /usr
