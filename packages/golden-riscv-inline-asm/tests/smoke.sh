#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

golden-inline | grep -E '^[0-9]+$'
rpm -q --qf '%{ARCH}\n' golden-riscv-inline-asm | grep -Fx riscv64
