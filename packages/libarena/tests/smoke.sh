#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT
library=/usr/lib64/libarena.so.0.0.3
driver=/usr/libexec/libarena/api-smoke
test -f "$library"
test -x "$driver"
test -f /usr/lib64/libarena.a
test -f /usr/lib64/libarena.la
for header in arena pool proto rbits util align; do
    test -f "/usr/include/arena/$header.h"
done
cd /usr/share/licenses/libarena/source-notices
test "$(wc -l < SHA256SUMS)" -eq 33
sha256sum -c SHA256SUMS
grep -F 'output file without restriction.' /usr/share/licenses/libarena/LicenseRef-dh-make-output.txt
cd /
sha256sum -c /usr/share/libarena-tests/SHA256SUMS
for elf in "$library" "$driver"; do
    readelf -h "$elf" | grep -E 'Class:[[:space:]]+ELF64[[:space:]]*$'
    readelf -h "$elf" | grep -E 'Machine:[[:space:]]+RISC-V[[:space:]]*$'
done
readelf -d "$driver" | grep -E '\(NEEDED\).*\[libarena\.so\.0\]'
trace="$(mktemp)"
out="$(mktemp)"; err="$(mktemp)"; expected="$(mktemp)"
trap 'rm -f "$trace" "$out" "$err" "$expected"' EXIT
cat > "$expected" <<'LIBARENA_EXPECTED_EOF'
case 1 arena-aligned-reallocation PASS
case 2 arena-mark-reset PASS
case 3 pool-bucket-reallocation PASS
case 4 layered-prototype-ownership PASS
case 5 exact-string-binary-format PASS
case 6 zero-size-reallocation PASS
libarena API 6/6 PASS
LIBARENA_EXPECTED_EOF
if "$driver" >"$out" 2>"$err"; then
    :
else
    status=$?
    cat "$out" "$err" >&2
    sha256sum "$out" "$err" >&2
    exit "$status"
fi
cat "$out"
cat "$err" >&2
test ! -s "$err"
cmp "$expected" "$out"
if LD_DEBUG=bindings "$driver" >"$out" 2>"$trace"; then
    :
else
    status=$?
    cat "$out" "$trace" >&2
    sha256sum "$out" "$trace" >&2
    exit "$status"
fi
echo 'BEGIN libarena installed raw loader trace'
cat "$trace"
echo 'END libarena installed raw loader trace'
sha256sum "$trace"
cmp "$expected" "$out"
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
for symbol in arena_open arena_malloc arena_realloc pool_open pool_get pool_realloc; do
    verify_binding "$symbol"
done
echo 'libarena six installed fixed-input API cases and six strict same-file bindings PASS'
