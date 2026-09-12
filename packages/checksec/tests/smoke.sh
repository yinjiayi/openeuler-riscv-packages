#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- checksec
installed_version=$(rpm -q --qf '%{VERSION}' checksec)
checksec --version | grep -F "${installed_version}"
checksec --no-banner --output json file /usr/bin/bash | \
  python3 -c 'import json, sys; result = json.load(sys.stdin); assert isinstance(result, list) and len(result) == 1 and isinstance(result[0].get("checks"), dict)'
