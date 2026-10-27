#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libsquish.so.0.0
driver=/usr/libexec/libsquish-tests/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/include/squish.h
test -f /usr/lib64/libsquish.a
cd /usr/share/licenses/libsquish/license-notices
test "$(wc -l < SHA256SUMS)" -eq 54
sha256sum -c SHA256SUMS
cd /usr/libexec/libsquish-tests
sha256sum -c SHA256SUMS
trace="$(mktemp)"
symbols="$(mktemp)"
trap 'rm -f "$trace" "$symbols"' EXIT
# nm/c++filt inspect the installed ELF without executing that object.
nm --dynamic --defined-only --format=posix "$library" > "$symbols"
if LD_DEBUG=bindings "$driver" 2>"$trace"; then
    :
else
    status=$?
    cat "$trace" >&2
    sha256sum "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libsquish installed raw loader trace'
cat "$trace"
echo 'END libsquish installed raw loader trace'
sha256sum "$trace"
verify_binding() {
    local expected=$1 symbol kind remainder decoded count=0 selected=
    while read -r symbol kind remainder; do
        [[ $kind == T ]] || continue
        decoded=$(c++filt "$symbol")
        if [[ $decoded == "$expected" ]]; then
            selected=$symbol
            count=$((count+1))
        fi
    done < "$symbols"
    [[ $count -eq 1 ]] || { printf 'expected one installed definition: %s; found %s\n' "$expected" "$count" >&2; return 1; }
    local line caller target observed found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}; target=${BASH_REMATCH[2]}; observed=${BASH_REMATCH[3]}
            [[ $observed == "$selected" ]] || continue
            [[ $caller == /* && $caller -ef $driver ]] || continue
            if [[ $target != /* || ! $target -ef $library ]]; then
                printf 'binding %s FAIL target=%s\n' "$selected" "$target" >&2
                return 1
            fi
            printf 'binding %s PASS target=%s same installed file\n' "$selected" "$target"
            found=true
        fi
    done < "$trace"
    [[ $found == true ]] || { printf 'missing exact driver binding: %s\n' "$selected" >&2; return 1; }
}
verify_binding 'squish::GetStorageRequirements(int, int, int)'
verify_binding 'squish::CompressMasked(unsigned char const*, int, void*, int, float*)'
verify_binding 'squish::Decompress(unsigned char*, void const*, int)'
verify_binding 'squish::CompressImage(unsigned char const*, int, int, int, void*, int, float*)'
verify_binding 'squish::DecompressImage(unsigned char*, int, int, int, void const*, int)'
verify_binding 'squish::ComputeMSE(unsigned char const*, int, int, int, unsigned char const*, int, double&, double&)'
echo 'libsquish six installed API cases and six strict same-file bindings PASS'
