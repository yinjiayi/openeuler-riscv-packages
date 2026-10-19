#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- pick pick-tests
exec sh /usr/libexec/pick-tests/replay.sh ''
