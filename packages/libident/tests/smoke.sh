#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -r /usr/include/ident.h
test -r /usr/lib64/libident.a
test -r /usr/lib64/libident.so.0
test -r /usr/share/man/man3/ident.3.gz
test -r /usr/share/licenses/libident/COPYING
test -r /usr/share/licenses/libident/AUTHORS
test -r /usr/share/licenses/libident/COPYING.GPL2
test -r /usr/share/licenses/libident/license-notices/admin/install-sh
test -r /usr/share/licenses/libident/license-notices/api-smoke.c
work_dir=$(mktemp -d)
trap 'rm -rf -- "$work_dir"' EXIT
(
    cd /usr/share/licenses/libident/license-notices
    sha256sum -c SHA256SUMS
)
(
    cd /usr/libexec/libident-tests
    sha256sum -c SHA256SUMS
)
LD_DEBUG=bindings /usr/libexec/libident-tests/api-smoke \
    > "$work_dir/output" 2> "$work_dir/bindings"
grep -Fx 'libident api-smoke: 6 cases passed; version 0.32' "$work_dir/output"
for symbol in id_parse id_query ident_free; do
    grep -Eq "binding file .*api-smoke.*libident[.]so[.]0.*${symbol}" "$work_dir/bindings"
done
printf '%s\n' 'libident installed shared-library API smoke passed (no server or timing claim)'
