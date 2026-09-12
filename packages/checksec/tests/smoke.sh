#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- checksec
installed_version=$(rpm -q --qf '%{VERSION}' checksec)
checksec --version | grep -F "${installed_version}"
checksec --no-banner --output json file /usr/bin/bash | \
  jq -e 'type == "array" and length == 1 and (.[0].checks | type == "object")'
