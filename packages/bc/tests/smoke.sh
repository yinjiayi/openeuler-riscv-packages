#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bc
bc --version | grep -F 'bc 1.08.2'
dc --version | grep -Fx 'dc 1.5.2 (GNU bc 1.08.2)'
printf '6 * 7\n' | bc | grep -qx '42'
printf '6 7 * p\n' | dc | grep -qx '42'
printf 'scale=6; 22 / 7\n' | bc | grep -qx '3.142857'
