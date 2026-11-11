#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
test -f /usr/lib64/libtpl.so.0.0.0
test -f /usr/lib64/libtpl.a
test -f /usr/include/tpl.h
cd /usr/share/licenses/libtpl/license-notices
sha256sum -c SHA256SUMS
cd /usr/libexec/libtpl-tests
sha256sum -c SHA256SUMS
driver=/usr/libexec/libtpl-tests/api-smoke
test -x "$driver"
trace="$(mktemp)"
trap 'rm -f "$trace"' EXIT
if LD_DEBUG=bindings "$driver" 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libtpl installed raw loader trace'
cat "$trace"
echo 'END libtpl installed raw loader trace'
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
for symbol in tpl_map tpl_pack tpl_dump tpl_load tpl_unpack tpl_free; do
    verify_installed_binding "$trace" "$driver" /usr/lib64/libtpl.so.0.0.0 "$symbol"
done
echo 'libtpl installed API replay and six library bindings PASS'
