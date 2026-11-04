#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libsimple.so.1.8
driver=/usr/libexec/libsimple-tests/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/lib64/libsimple.a
test -f /usr/include/libsimple.h
test -f /usr/include/libsimple-arg.h
cd /usr/share/licenses/libsimple/license-notices
test "$(wc -l < SHA256SUMS)" -eq 1353
sha256sum -c SHA256SUMS
cd /usr/libexec/libsimple-tests
sha256sum -c SHA256SUMS
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
echo 'BEGIN libsimple installed raw loader trace'
cat "$trace"
echo 'END libsimple installed raw loader trace'
sha256sum "$trace"
verify_binding() {
    local expected=$1 line caller target observed found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}; target=${BASH_REMATCH[2]}; observed=${BASH_REMATCH[3]}
            [[ $observed == "$expected" ]] || continue
            [[ $caller == /* && $caller -ef $driver ]] || continue
            if [[ $target != /* || ! $target -ef $library ]]; then
                printf 'binding %s FAIL target=%s\n' "$expected" "$target" >&2
                return 1
            fi
            printf 'binding %s PASS target=%s same installed file\n' "$expected" "$target"
            found=true
        fi
    done < "$trace"
    [[ $found == true ]] || { printf 'missing exact driver binding: %s\n' "$expected" >&2; return 1; }
}
for symbol in libsimple_memdup libsimple_strtoi libsimple_strstarts libsimple_memcasecmp libsimple_memmem libsimple_strtotimespec; do
    verify_binding "$symbol"
done
echo 'libsimple six installed API cases and six strict same-file bindings PASS'
