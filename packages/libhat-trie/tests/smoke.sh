#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT LIBRARY_PATH CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH PKG_CONFIG_PATH PKG_CONFIG_LIBDIR
qa=/usr/share/libhat-trie-tests
archive=/usr/lib64/libhat-trie.a
license=/usr/share/licenses/libhat-trie
test -f "$archive" && test -f /usr/lib64/libhat-trie.la
test "$(pkg-config --modversion hat-trie-0.1)" = 0.1.2
(cd /; sha256sum -c "$qa/SHA256SUMS")
(cd "$license/license-notices"; sha256sum -c SHA256SUMS)
test "$(wc -l < "$license/license-notices/SHA256SUMS")" -eq 27
printf '%s  %s\n' 20e50fe7aae3e56378ebf0417d9de904f55a0e61e4df315333e632a4d3555d95 "$license/LGPL-2.1.txt" | sha256sum -c -
printf '%s  %s\n' cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 "$license/Apache-2.0.txt" | sha256sum -c -
grep -F 'LGPL-2.1-only' "$license/SuperFastHash-attribution.notice"
work=$(mktemp -d)
cleanup() {
    status=$?
    trap - EXIT
    for raw in negative.stdout negative.stderr negative.status link.stdout link.stderr consumer.map elf-header elf-dynamic archive.nm consumer.nm api.stdout api.stderr; do
        if test -f "$work/$raw"; then printf '\nraw %s\n' "$raw"; cat "$work/$raw"; sha256sum "$work/$raw"; fi
    done
    rm -rf "$work"
    exit "$status"
}
trap cleanup EXIT
sha256sum "$archive" > "$work/archive.before"
read -r -a cflags <<< "$(pkg-config --cflags hat-trie-0.1)"
read -r -a libs <<< "$(pkg-config --libs hat-trie-0.1)"
# Negative control must fail at linking the actual missing library symbols,
# not merely at an unrelated compiler/header error; never execute its output.
if /usr/bin/gcc -std=c99 -O2 -UNDEBUG "${cflags[@]}" "$qa/api-smoke.c" -o "$work/no-library" > "$work/negative.stdout" 2> "$work/negative.stderr"; then
    printf '%s\n' 0 > "$work/negative.status"
    exit 1
else
    status=$?
    printf '%s\n' "$status" > "$work/negative.status"
fi
test "$status" -ne 0 && test ! -e "$work/no-library"
for symbol in hattrie_get hattrie_tryget hattrie_clear ahtable_clear ahtable_save ahtable_load; do
    grep -E "undefined reference to.*${symbol}" "$work/negative.stderr"
done
if /usr/bin/gcc -std=c99 -O2 -UNDEBUG "${cflags[@]}" "$qa/api-smoke.c" "${libs[@]}" -Wl,-t,-t "-Wl,-Map,$work/consumer.map" -o "$work/consumer" > "$work/link.stdout" 2> "$work/link.stderr"; then :; else status=$?; cat "$work/link.stdout" "$work/link.stderr"; exit "$status"; fi
cat "$work/link.stdout" "$work/link.stderr"
# Functional pkg-config linkage must select exactly the installed static archive.
trace_count=0
while IFS= read -r line; do
    candidate=
    case "$line" in
        /*libhat-trie.a) candidate="$line";;
        \(/*libhat-trie.a\)*) candidate="${line#(}"; candidate="${candidate%%)*}";;
    esac
    if test -n "$candidate"; then test -f "$candidate" && test "$candidate" -ef "$archive"; trace_count=$((trace_count+1)); fi
done < "$work/link.stdout"
test "$trace_count" -gt 0
map_count=0
while IFS= read -r line; do
    case "$line" in
        'LOAD '/*libhat-trie.a) candidate="${line#LOAD }"; test -f "$candidate" && test "$candidate" -ef "$archive"; map_count=$((map_count+1));;
    esac
done < "$work/consumer.map"
test "$map_count" -eq 1
if grep -F 'libhat-trie.so' "$work/link.stdout" "$work/consumer.map"; then exit 1; fi
readelf -h "$work/consumer" > "$work/elf-header"
grep -E 'Class:[[:space:]]+ELF64' "$work/elf-header"
grep -E 'Machine:[[:space:]]+RISC-V' "$work/elf-header"
readelf -d "$work/consumer" > "$work/elf-dynamic"
if grep -F 'libhat-trie.so' "$work/elf-dynamic"; then exit 1; fi
nm -g --defined-only "$archive" > "$work/archive.nm"
nm -g --defined-only "$work/consumer" > "$work/consumer.nm"
for symbol in hattrie_get hattrie_tryget hattrie_clear ahtable_clear ahtable_save ahtable_load; do
    grep -E "[[:space:]][Tt][[:space:]]${symbol}$" "$work/archive.nm"
    grep -E "[[:space:]][Tt][[:space:]]${symbol}$" "$work/consumer.nm"
done
if "$work/consumer" > "$work/api.stdout" 2> "$work/api.stderr"; then :; else status=$?; cat "$work/api.stdout" "$work/api.stderr"; exit "$status"; fi
cat "$work/api.stdout"
cmp "$qa/expected.stdout" "$work/api.stdout"
test ! -s "$work/api.stderr"
sha256sum "$archive" > "$work/archive.after"
cmp "$work/archive.before" "$work/archive.after"
sha256sum "$work/link.stdout" "$work/link.stderr" "$work/consumer.map" "$work/consumer" "$work/api.stdout" "$work/api.stderr"
printf '%s\n' 'libhat-trie installed static pkg-config consumer PASS'
