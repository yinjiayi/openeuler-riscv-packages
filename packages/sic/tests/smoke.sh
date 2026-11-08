#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
test -x /usr/bin/sic
test -r /usr/share/sic/qa.py
python3 -I -B /usr/share/sic/qa.py /usr/bin/sic
