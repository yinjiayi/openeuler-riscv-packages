#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nmail
nmail --version | grep -F -- 'nmail 5.14.12'
nmail --help >/dev/null
