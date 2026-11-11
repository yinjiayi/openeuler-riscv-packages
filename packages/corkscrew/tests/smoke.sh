#!/usr/bin/bash
set -euo pipefail
test -x /usr/bin/corkscrew
test -x /usr/libexec/corkscrew-tests/installed-check.py
exec /usr/bin/python3 /usr/libexec/corkscrew-tests/installed-check.py
