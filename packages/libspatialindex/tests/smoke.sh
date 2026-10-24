#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libspatialindex
driver=/usr/libexec/libspatialindex-tests/api-smoke
test -x "$driver"
(cd /usr/libexec/libspatialindex-tests; sha256sum -c SHA256SUMS)
license_root=/usr/share/licenses/libspatialindex
if [[ ! -d "$license_root/license-notices" ]]; then
    license_root=/usr/share/licenses/libspatialindex-2.1.0
fi
test -d "$license_root/license-notices"
(cd "$license_root/license-notices"; sha256sum -c SHA256SUMS)
test "$(wc -l < "$license_root/license-notices/SHA256SUMS")" -eq 325
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
LD_DEBUG=bindings "$driver" > "$work_dir/stdout" 2> "$work_dir/bindings"
cat "$work_dir/stdout"
test "$(grep -c '^api .*: PASS$' "$work_dir/stdout")" -eq 6
for symbol in SIDX_Version Index_Create Index_InsertData Index_Intersects_count; do
    grep -E "binding file .*api-smoke.* to /usr/lib64/libspatialindex_c\\.so\\.8[^ ]*.*normal symbol .$symbol." "$work_dir/bindings"
done
