#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- luau
command -v luau
luau --help | grep -F 'Usage:'
