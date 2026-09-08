#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dragonbox
installed_version=$(rpm -q --qf '%{VERSION}' dragonbox)
test -r "/usr/include/dragonbox-${installed_version}/dragonbox/dragonbox.h"
test -r /usr/lib64/libdragonbox_to_chars.a
