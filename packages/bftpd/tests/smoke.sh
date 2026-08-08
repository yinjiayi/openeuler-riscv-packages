#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bftpd
bftpd -v | grep -F 'Bftpd version 6.7'
test -r /etc/bftpd.conf
