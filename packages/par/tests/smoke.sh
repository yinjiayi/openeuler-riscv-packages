#!/bin/sh
# SPDX-License-Identifier: MIT
set -eu
test -x /usr/bin/par
test -r /usr/share/licenses/par/par.doc
test -r /usr/libexec/par-tests/test-par
test -r /usr/libexec/par-tests/installed-check.py
exec /usr/bin/python3 /usr/libexec/par-tests/installed-check.py --binary /usr/bin/par --suite /usr/libexec/par-tests/test-par
