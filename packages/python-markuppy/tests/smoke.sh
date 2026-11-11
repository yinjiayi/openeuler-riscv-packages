#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$(rpm -q --qf '%{VERSION}' python-markuppy)" = 1.18
rpm -V python-markuppy
unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONOPTIMIZE
export PYTHONDONTWRITEBYTECODE=1
cd /tmp
exec python3 -I -B /usr/share/python-markuppy/verify.py \
    /usr/share/python-markuppy /usr/lib/python3.11/site-packages installed
