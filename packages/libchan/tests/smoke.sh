#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libchan libchan-devel
rpm -V libchan libchan-devel
test "$(rpm -qf --qf '%{NAME}\n' /usr/lib64/libchan.so.0.0.0)" = libchan
test "$(rpm -qf --qf '%{NAME}\n' /usr/include/chan/chan.h)" = libchan-devel
test "$(rpm -qf --qf '%{NAME}\n' /usr/include/chan/queue.h)" = libchan-devel
test "$(readlink /usr/lib64/libchan.so.0)" = libchan.so.0.0.0
test "$(readlink /usr/lib64/libchan.so)" = libchan.so.0.0.0
test -s /usr/lib64/libchan.a
test -s /usr/share/licenses/libchan/LICENSE
bash /usr/share/libchan/tests/run-original-tests.sh
