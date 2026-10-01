#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libmatheval
test -e /usr/lib64/libmatheval.so.1
