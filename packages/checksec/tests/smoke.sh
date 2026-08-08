#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- checksec
installed_version=$(rpm -q --qf '%{VERSION}' checksec)
checksec --version | grep -F "${installed_version}"
