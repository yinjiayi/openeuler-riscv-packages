#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- bitwise
installed_version=$(rpm -q --qf '%{VERSION}' bitwise)
bitwise --version | grep -F "${installed_version}"
