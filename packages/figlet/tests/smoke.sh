#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- figlet
test "$(figlet -I1)" = 2.2.5
test "$(figlet -I2)" = /usr/share/figlet
test -f /usr/share/figlet/standard.flf
test -n "$(figlet -f standard RISCV)"
test -n "$(figlet -f small openEuler)"
