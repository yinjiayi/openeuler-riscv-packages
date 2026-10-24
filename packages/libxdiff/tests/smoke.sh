#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -r /usr/include/xdiff/xdiff.h
test -r /usr/include/xdiff/config.h
test -r /usr/lib64/libxdiff.a
test -r /usr/lib64/libxdiff.so.1
test -r /usr/lib64/pkgconfig/libxdiff.pc
test -r /usr/share/licenses/libxdiff/COPYING
test -r /usr/share/licenses/libxdiff/license-notices/xhistogram.c.notice
test -r /usr/share/licenses/libxdiff/license-notices/api-smoke.c
(
    cd /usr/share/licenses/libxdiff/license-notices
    sha256sum -c SHA256SUMS
)
(
    cd /usr/libexec/libxdiff-tests
    sha256sum -c SHA256SUMS
)
work_dir=$(mktemp -d)
trap 'rm -rf -- "$work_dir"' EXIT
LD_DEBUG=bindings /usr/libexec/libxdiff-tests/api-smoke \
    > "$work_dir/output" 2> "$work_dir/bindings"
grep -Fx 'libxdiff api-smoke: 6 cases passed; version 1.0' "$work_dir/output"
for symbol in xdl_diff xdl_merge xdl_mmfile_size xdl_mmfile_first; do
    grep -Eq "binding file .*api-smoke.*libxdiff[.]so[.]1.*${symbol}" "$work_dir/bindings"
done
printf '%s\n' 'libxdiff installed shared-library API smoke passed (no performance claim)'
