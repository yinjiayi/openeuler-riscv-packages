#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nudoku
installed_version=$(rpm -q --qf '%{VERSION}' nudoku)
nudoku -v | grep -F "${installed_version}"
