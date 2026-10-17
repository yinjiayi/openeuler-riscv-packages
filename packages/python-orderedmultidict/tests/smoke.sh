#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-orderedmultidict
test "$(rpm -q --qf '%{VERSION}-%{RELEASE}\n' python-orderedmultidict)" = '1.0.2-1'
rpm -V -- python-orderedmultidict
unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONOPTIMIZE
export PYTHONDONTWRITEBYTECODE=1
cd /tmp
python3 -I /usr/share/python-orderedmultidict/verify-installed.py /usr/share/python-orderedmultidict /usr/lib/python3.11/site-packages installed
