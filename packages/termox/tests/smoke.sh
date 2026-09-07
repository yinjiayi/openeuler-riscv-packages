#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- termox
test -f /usr/include/ox/ox.hpp
test -f /usr/lib64/libTermOx.a
