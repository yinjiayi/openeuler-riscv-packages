#!/usr/bin/bash
set -euo pipefail
exec python3 /usr/libexec/stagit-tests/installed-check.py --bindir /usr/bin
