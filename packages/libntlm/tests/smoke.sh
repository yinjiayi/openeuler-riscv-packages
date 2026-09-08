#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libntlm libntlm-devel
pkg-config --modversion libntlm | grep -Fx '1.8'
test -f /usr/include/ntlm.h
test -f /usr/lib64/pkgconfig/libntlm.pc
