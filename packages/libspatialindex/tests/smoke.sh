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
if LD_DEBUG=bindings "$driver" > "$work_dir/stdout" 2> "$work_dir/bindings"; then
    :
else
    driver_status=$?
    cat "$work_dir/stdout"
    cat "$work_dir/bindings" >&2
    exit "$driver_status"
fi
cat "$work_dir/stdout"
# Retain complete loader evidence in the existing smoke.log before assertions.
cat "$work_dir/bindings"
test "$(grep -c '^api .*: PASS$' "$work_dir/stdout")" -eq 6

verify_installed_binding() {
    local trace=$1 expected_driver=$2 expected_library=$3 symbol=$4
    local line caller target observed_symbol found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}
            target=${BASH_REMATCH[2]}
            observed_symbol=${BASH_REMATCH[3]}
            [[ $observed_symbol == "$symbol" ]] || continue
            [[ $caller == /* && $caller -ef $expected_driver ]] || continue
            if [[ $target != /* || ! $target -ef $expected_library ]]; then
                printf 'binding %s: FAIL (target %s is not installed %s)\n' "$symbol" "$target" "$expected_library" >&2
                return 1
            fi
            printf 'binding %s: PASS (target %s is same file as %s)\n' "$symbol" "$target" "$expected_library"
            found=true
        fi
    done < "$trace"
    if [[ $found != true ]]; then
        printf 'binding %s: FAIL (no exact installed-driver symbol binding)\n' "$symbol" >&2
        return 1
    fi
}
for symbol in SIDX_Version Index_Create Index_InsertData Index_Intersects_count; do
    verify_installed_binding "$work_dir/bindings" "$driver" /usr/lib64/libspatialindex_c.so.8 "$symbol"
done
