#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxdgdirs
test -f /usr/include/xdgdirs.h
test -f /usr/lib/libXDGdirs.a
