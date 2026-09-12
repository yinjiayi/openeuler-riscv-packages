#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- 6tunnel
installed_version=$(rpm -q --qf '%{VERSION}' 6tunnel)
6tunnel -V | grep -F "$installed_version"
test -x /usr/bin/6tunnel
test -r /usr/share/man/man1/6tunnel.1.gz
