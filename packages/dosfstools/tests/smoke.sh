#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dosfstools
mkfs.fat --version 2>&1 | grep -F 'dosfstools 4.2'
fsck.fat -V 2>&1 | grep -F 'dosfstools 4.2'
test -x /usr/sbin/mkfs.fat
test -x /usr/sbin/fsck.fat
