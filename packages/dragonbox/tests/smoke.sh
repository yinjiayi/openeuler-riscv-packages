#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dragonbox
test -r /usr/include/dragonbox-1.1.3/dragonbox/dragonbox.h
test -r /usr/lib64/libdragonbox_to_chars.a

