#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- sysfsutils
test -x /usr/bin/systool
rpm -ql sysfsutils | grep -F '/libsysfs.so.2'

