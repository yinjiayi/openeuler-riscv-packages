#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bftpd
installed_version=$(rpm -q --qf '%{VERSION}' bftpd)
bftpd -v | grep -F "Bftpd version ${installed_version}"
test -r /etc/bftpd.conf
