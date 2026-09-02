#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- pcre2 pcre2-devel
printf 'riscv64\n' | pcre2grep '^riscv[0-9]+$' | grep -Fx riscv64
pcre2-config --version | grep -Fx 10.48
