#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -f /usr/lib64/libudfread.so.3.0.0
test -f /usr/lib64/libudfread.a
test -f /usr/include/udfread/udfread.h
cd /usr/share/licenses/libudfread/license-notices
sha256sum -c SHA256SUMS
cd /usr/libexec/libudfread-tests
sha256sum -c SHA256SUMS
driver=/usr/libexec/libudfread-tests/api-smoke
test -x "$driver"
trace="$(mktemp)"
trap 'rm -f "$trace"' EXIT
if LD_DEBUG=bindings "$driver" /usr/libexec/libudfread-tests/fixture.udf 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libudfread installed raw loader trace'
cat "$trace"
echo 'END libudfread installed raw loader trace'
sha256sum "$trace"
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
for symbol in udfread_get_version udfread_open udfread_opendir udfread_file_open udfread_file_read udfread_file_seek; do
    verify_installed_binding "$trace" "$driver" /usr/lib64/libudfread.so.3.0.0 "$symbol"
done
echo 'libudfread installed API replay and six library bindings PASS'
