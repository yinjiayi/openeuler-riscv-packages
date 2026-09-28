#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- figlet
# Upstream -I1 reports the integer version, not the dotted release.
test "$(figlet -I1)" = 20205
test "$(figlet -I2)" = /usr/share/figlet
test -f /usr/share/figlet/standard.flf
test -n "$(figlet -f standard RISCV)"
test -n "$(figlet -f small openEuler)"
