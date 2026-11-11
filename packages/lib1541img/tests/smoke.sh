#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q lib1541img lib1541img-devel
rpm -V lib1541img lib1541img-devel
test "$(pkg-config --modversion 1541img)" = 1.1.0
test "$(pkg-config --variable=libdir 1541img)" = /usr/lib64
test "$(pkg-config --variable=includedir 1541img)" = /usr/include
test -f /usr/share/licenses/lib1541img/LICENSE.txt
test -f /usr/share/licenses/lib1541img/LICENSE-zimk
test -s /usr/share/doc/1541img/README.md
test -s /usr/share/doc/1541img/CHANGES.txt
cmp /usr/share/doc/1541img/LICENSE.txt /usr/share/licenses/lib1541img/LICENSE.txt
rpm -qf /usr/share/doc/1541img/README.md /usr/share/doc/1541img/CHANGES.txt \
    /usr/share/doc/1541img/LICENSE.txt
library=$(readlink -f /usr/lib64/lib1541img.so)
test "$library" = /usr/lib64/lib1541img.so.1.1.0
rpm -qf "$library"
work_dir=$(mktemp -d)
trap 'rm -r -- "$work_dir"' EXIT
unset CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH LIBRARY_PATH LD_LIBRARY_PATH PKG_CONFIG_PATH PKG_CONFIG_LIBDIR PKG_CONFIG_SYSROOT_DIR
cd "$work_dir"
gcc -std=c11 -Wall -Wextra /usr/share/lib1541img/verify-1541img.c \
    $(pkg-config --cflags --libs 1541img) -o consumer
ldd ./consumer | tee linked.txt
linked=$(awk '$1 == "lib1541img.so.1" && $2 == "=>" {print $3}' linked.txt)
test -n "$linked"
test "$(readlink -f "$linked")" = "$library"
rpm -qf "$(readlink -f "$linked")"
./consumer
