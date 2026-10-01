#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- m4
actual=$(
    printf '%s\n' \
        'changequote([,])dnl' \
        'define([TARGET], [riscv64-RVA23])dnl' \
        'TARGET' | m4
)
test "$actual" = "riscv64-RVA23"
