#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdxfrw libdxfrw-devel
rpm -V libdxfrw libdxfrw-devel
bash /usr/share/libdxfrw/tests/run-contract.sh /
