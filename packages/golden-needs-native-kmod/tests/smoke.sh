#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

echo 'This test requires a native RISC-V kernel and must never run under QEMU user mode.' >&2
exit 86
