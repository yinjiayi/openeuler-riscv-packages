#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nudoku
nudoku -v | grep -F '8.0.1'

