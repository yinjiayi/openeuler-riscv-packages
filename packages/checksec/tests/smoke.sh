#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- checksec
installed_version=$(rpm -q --qf '%{VERSION}' checksec)
checksec --version | grep -F "checksec v${installed_version}"
if checksec --help | grep -E -- '--(update|upgrade)'; then
  echo 'packaged checksec unexpectedly exposes its network self-update command' >&2
  exit 1
fi
checksec --format=json --file=/usr/bin/bash | jq -e 'type == "object"'
