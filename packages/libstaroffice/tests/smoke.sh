#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libstaroffice
command -v sdc2csv >/dev/null
test -f /usr/include/libstaroffice/libstaroffice.hxx
test -e /usr/lib64/libstaroffice-0.0.so.0
