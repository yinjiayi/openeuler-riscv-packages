#!/usr/bin/env bash
# SPDX-License-Identifier: ISC
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libroxml.so.0.0.0
driver=/usr/libexec/libroxml/api-smoke
test -f "$library" && test -x "$driver"
for file in /usr/lib64/libroxml.a /usr/lib64/libroxml.la /usr/include/roxml.h /usr/lib64/pkgconfig/libroxml.pc; do test -f "$file"; done
test -x /usr/bin/roxml && test -x /usr/bin/rocat
cd /usr/share/licenses/libroxml/source-notices
test "$(wc -l < SHA256SUMS)" -eq 82
sha256sum -c SHA256SUMS
cd /
sha256sum -c /usr/share/libroxml-tests/SHA256SUMS
for elf in "$library" "$driver" /usr/bin/roxml /usr/bin/rocat; do
    readelf -h "$elf" | grep -E 'Class:[[:space:]]+ELF64[[:space:]]*$'
    readelf -h "$elf" | grep -E 'Machine:[[:space:]]+RISC-V[[:space:]]*$'
done
readelf -d "$driver" | grep -E '\(NEEDED\).*\[libroxml\.so\.0\]'
work="$(mktemp -d)"
trap 'rm -f "$work/expected" "$work/out" "$work/err" "$work/trace"; rmdir "$work"' EXIT
cd "$work"
cat >expected <<'EXPECTED'
ok 1 parse-navigation
ok 2 content-attribute
ok 3 xpath-ownership
ok 4 edit-serialize
ok 5 file-roundtrip
ok 6 null-boundaries
libroxml API: 6/6 passed
EXPECTED
if "$driver" >out 2>err; then :; else
    status=$?; cat out err >&2; sha256sum out err >&2; exit "$status"
fi
cat out; cat err >&2
test ! -s err
cmp expected out
if LD_DEBUG=bindings "$driver" >out 2>trace; then :; else
    status=$?; cat out trace >&2; sha256sum out trace >&2; exit "$status"
fi
echo 'BEGIN libroxml installed raw loader trace'
cat trace
echo 'END libroxml installed raw loader trace'
sha256sum trace
cmp expected out
verify_binding() {
    local expected=$1 line caller target observed found=false
    local binding_re="^[[:space:]]*[0-9]+:[[:space:]]+binding file ([^[:space:]]+) \\[[0-9]+\\] to ([^[:space:]]+) \\[[0-9]+\\]: normal symbol \`([^']+)'$"
    while IFS= read -r line; do
        if [[ $line =~ $binding_re ]]; then
            caller=${BASH_REMATCH[1]}; target=${BASH_REMATCH[2]}; observed=${BASH_REMATCH[3]}
            [[ $observed == "$expected" ]] || continue
            [[ $caller == /* && $caller -ef $driver ]] || continue
            if [[ $target != /* || ! $target -ef $library ]]; then
                printf 'binding %s FAIL target=%s\n' "$expected" "$target" >&2; return 1
            fi
            printf 'binding %s PASS target=%s same installed file\n' "$expected" "$target"
            found=true
        fi
    done < trace
    [[ $found == true ]] || { printf 'missing exact driver binding: %s\n' "$expected" >&2; return 1; }
}
for symbol in roxml_load_buf roxml_get_chld roxml_get_name roxml_get_content roxml_xpath roxml_close; do verify_binding "$symbol"; done
echo 'libroxml six installed API cases and six strict same-file bindings PASS'
