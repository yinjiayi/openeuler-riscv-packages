#!/usr/bin/env bash
# Copyright 2026 openEuler package contributors.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C LANG=C
work=$(mktemp -d /tmp/gsl-lite-installed-smoke.XXXXXXXX)
python3 /usr/libexec/gsl-lite/qa/run-installed.py --prefix /usr --work-dir "$work/run"
