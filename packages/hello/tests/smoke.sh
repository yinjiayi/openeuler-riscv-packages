#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

test "$(hello)" = "Hello, world!"
hello --version | grep -F 'hello (GNU Hello) 2.12.3'
rpm -q --qf '%{ARCH}\n' hello | grep -Fx riscv64
