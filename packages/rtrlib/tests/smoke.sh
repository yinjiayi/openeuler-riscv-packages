#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- rtrlib
test -x /usr/bin/rtrclient
test -x /usr/bin/rpki-rov
test -f /usr/include/rtrlib/rtrlib.h
test -f /usr/lib64/librtr.so.0.8.0
test -f /usr/lib64/pkgconfig/rtrlib.pc
