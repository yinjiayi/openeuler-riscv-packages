#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- liblogging
test -e /usr/lib64/liblogging-stdlog.so.1
test -e /usr/lib64/liblogging-rfc3195.so.0
