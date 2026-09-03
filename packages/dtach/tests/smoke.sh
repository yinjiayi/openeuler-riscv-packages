#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- dtach
installed_version=$(rpm -q --qf '%{VERSION}' dtach)
dtach --version | grep -F "dtach - version ${installed_version}"
dtach --help >/dev/null
