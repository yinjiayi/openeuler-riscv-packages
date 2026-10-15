#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH
rpm -q libcstl libcstl-devel
rpm -V libcstl libcstl-devel
test -s /usr/share/licenses/libcstl/COPYING.LESSER
test -s /usr/share/licenses/libcstl/AUTHORS
library=$(readlink -f /usr/lib64/libcstl.so.2)
test -s "$library"
test "$(rpm -qf --qf '%{NAME}' "$library")" = libcstl
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd /usr/share/libcstl/tests
sha256sum -c SHA256SUMS
gcc -O2 -UNDEBUG verify-containers.c -lcstl -o "$work/shared"
ldd "$work/shared" | tee "$work/ldd.txt"
linked=$(awk '$1 == "libcstl.so.2" && $2 == "=>" {print $3}' "$work/ldd.txt")
test -n "$linked"
test "$(readlink -f "$linked")" = "$library"
"$work/shared"
gcc -O2 -UNDEBUG verify-containers.c /usr/lib64/libcstl.a -o "$work/static"
"$work/static"
