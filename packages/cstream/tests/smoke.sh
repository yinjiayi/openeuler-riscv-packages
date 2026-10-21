#!/usr/bin/bash
set -euo pipefail
test -x /usr/bin/cstream
test -x /usr/libexec/cstream-tests/installed-check.py
exec /usr/bin/python3 /usr/libexec/cstream-tests/installed-check.py --binary /usr/bin/cstream
