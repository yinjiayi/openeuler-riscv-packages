#!/bin/sh
set -eu
exec /usr/bin/python3 /usr/libexec/sfeed-tests/installed-check.py --bindir /usr/bin
