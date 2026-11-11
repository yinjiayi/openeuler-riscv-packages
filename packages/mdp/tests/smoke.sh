#!/usr/bin/bash
set -euo pipefail
test -x /usr/bin/mdp
test -x /usr/libexec/mdp-tests/installed-check.py
exec /usr/bin/python3 /usr/libexec/mdp-tests/installed-check.py --installed
