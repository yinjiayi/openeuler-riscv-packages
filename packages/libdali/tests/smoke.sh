#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libdali.so.1.8.1
driver=/usr/libexec/libdali/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/lib64/libdali.a
test -f /usr/include/libdali.h
test -f /usr/lib64/pkgconfig/dali.pc
cd /usr/share/licenses/libdali/license-notices
test "$(wc -l < SHA256SUMS)" -eq 38
sha256sum -c SHA256SUMS
cd /
sha256sum -c /usr/share/libdali-tests/SHA256SUMS
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
echo 'BEGIN libdali installed raw loader trace'
cat "$trace"
echo 'END libdali installed raw loader trace'
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
for symbol in dl_md2doy dl_time2dltime dl_dltime2isotimestr dl_splitstreamid dl_strparse dl_handlereply; do
    verify_binding "$symbol"
done
echo 'libdali six installed offline API cases and six strict same-file bindings PASS'
