#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- help2man
help2man --version | head -n1 | grep -F 'GNU help2man 1.49.3'
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '%s\n' '#!/bin/sh' 'case "$1" in --version) echo "demo 1.0";; --help) echo "Usage: demo";; esac' >"$d/demo"
chmod +x "$d/demo"
help2man --no-info --name='demo utility' "$d/demo" >"$d/demo.1"
grep -F 'demo utility' "$d/demo.1"
