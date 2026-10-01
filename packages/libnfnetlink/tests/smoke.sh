#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libnfnetlink
test -e /usr/lib64/libnfnetlink.so.0
