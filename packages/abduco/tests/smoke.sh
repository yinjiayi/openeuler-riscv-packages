#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- abduco
abduco -v | grep -F 'abduco-0.6'
