#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- abduco
installed_version=$(rpm -q --qf '%{VERSION}' abduco)
abduco -v | grep -F "abduco-${installed_version}"
