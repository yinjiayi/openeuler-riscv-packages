#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- units
units --version
test "$(units -t meter centimeter)" = "100"
