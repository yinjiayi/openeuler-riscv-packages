#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libartnet libartnet-devel
rpm -V libartnet libartnet-devel
test "$(rpm -qf --qf '%{NAME}\n' /usr/lib64/libartnet.so.1.0.0)" = libartnet
test "$(rpm -qf --qf '%{NAME}\n' /usr/include/artnet/artnet.h)" = libartnet-devel
test "$(rpm -qf --qf '%{NAME}\n' /usr/lib64/pkgconfig/libartnet.pc)" = libartnet-devel
test "$(readlink /usr/lib64/libartnet.so.1)" = libartnet.so.1.0.0
test "$(readlink /usr/lib64/libartnet.so)" = libartnet.so.1.0.0
test -s /usr/lib64/libartnet.a
test -s /usr/share/licenses/libartnet/COPYING
bash /usr/share/libartnet/tests/run-contract.sh
