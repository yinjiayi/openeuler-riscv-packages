#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libmodule
test -f /usr/include/module/module.h
test -f /usr/lib64/libmodule.so.5.0.2
