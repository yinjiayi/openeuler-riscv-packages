#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- macchanger
installed_version=$(rpm -q --qf '%{VERSION}' macchanger)
macchanger --version | grep -F "${installed_version}"
