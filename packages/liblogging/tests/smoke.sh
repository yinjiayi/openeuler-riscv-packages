#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- liblogging
for soname in liblogging-stdlog.so.0 liblogging-rfc3195.so.0; do
  library="/usr/lib64/$soname"
  test -e "$library"
  test "$(rpm -qf --qf '%{NAME}' -- "$library")" = liblogging
done
