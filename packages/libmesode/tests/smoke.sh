#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libmesode.so.0.0.0
driver=/usr/libexec/libmesode-tests/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/include/mesode.h
test -f /usr/lib64/libmesode.a
test -f /usr/lib64/pkgconfig/libmesode.pc
cd /usr/share/licenses/libmesode/license-notices
test "$(wc -l < SHA256SUMS)" -eq 83
sha256sum -c SHA256SUMS
cd /usr/libexec/libmesode-tests
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
echo 'BEGIN libmesode installed raw loader trace'
cat "$trace"
echo 'END libmesode installed raw loader trace'
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
for symbol in xmpp_stanza_new_from_string xmpp_stanza_to_text xmpp_stanza_copy xmpp_jid_new xmpp_base64_decode_bin xmpp_sha1; do
    verify_binding "$symbol"
done
echo 'libmesode six installed API cases and six strict same-file bindings PASS'
