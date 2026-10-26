#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT LIBRARY_PATH CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH COMPILER_PATH GCC_EXEC_PREFIX LD_RUN_PATH
qa=/usr/share/libjodycode-tests
license=/usr/share/licenses/libjodycode
library=/usr/lib64/libjodycode.so.4.2.0
test -f "$library" && test -f /usr/lib64/libjodycode.a && test -f /usr/include/libjodycode.h
test /usr/lib64/libjodycode.so.4 -ef "$library" && test /usr/lib64/libjodycode.so -ef "$library"
(cd /; sha256sum -c "$qa/SHA256SUMS")
(cd "$license/license-notices"; sha256sum -c SHA256SUMS)
test "$(wc -l < "$license/license-notices/SHA256SUMS")" -eq 81
printf '%s  %s\n' 808f9d8a8ca0768c508a7dd79f60bd0b340194a9e021232e7687ad9829e1917b "$license/LICENSE.txt" | sha256sum -c -
printf '%s  %s\n' cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 "$license/Apache-2.0.txt" | sha256sum -c -
grep -F 'public-domain' "$license/Public-Domain.notice"
work=$(mktemp -d)
cleanup() {
    status=$?; trap - EXIT
    for raw in negative.stdout negative.stderr negative.status link.stdout link.stderr elf-library elf-consumer dynamic-library dynamic-consumer api.stdout api.stderr debug.stdout loader.trace bindings.tsv bound-symbols; do
        if test -f "$work/$raw"; then printf '\nraw %s\n' "$raw"; cat "$work/$raw"; sha256sum "$work/$raw"; fi
    done
    rm -rf "$work"; exit "$status"
}
trap cleanup EXIT
cd "$work"
sha256sum "$library" > library.before
if /usr/bin/gcc -std=gnu11 -O2 -UNDEBUG -I/usr/include "$qa/api-smoke.c" -o "$work/no-library" > negative.stdout 2> negative.stderr; then
    printf '%s\n' 0 > negative.status; exit 1
else status=$?; printf '%s\n' "$status" > negative.status; fi
test "$status" -ne 0 && test ! -e "$work/no-library"
for symbol in jc_block_hash jc_numeric_strcmp jc_str_init jc_make_relative_link_name jc_fread jc_strtol; do
    grep -E "undefined reference to.*${symbol}" negative.stderr
done
if /usr/bin/gcc -std=gnu11 -O2 -UNDEBUG -I/usr/include "$qa/api-smoke.c" -L/usr/lib64 -ljodycode -o "$work/consumer" > link.stdout 2> link.stderr; then :; else status=$?; cat link.stdout link.stderr; exit "$status"; fi
readelf -h "$library" > elf-library
readelf -h "$work/consumer" > elf-consumer
for header in elf-library elf-consumer; do
    grep -E 'Class:[[:space:]]+ELF64[[:space:]]*$' "$header"
    grep -E 'Machine:[[:space:]]+RISC-V[[:space:]]*$' "$header"
done
readelf -d "$library" > dynamic-library
readelf -d "$work/consumer" > dynamic-consumer
grep -E '\(SONAME\).*\[libjodycode\.so\.4\]' dynamic-library
grep -E '\(NEEDED\).*\[libjodycode\.so\.4\]' dynamic-consumer
if grep -E '\((RPATH|RUNPATH)\)' dynamic-consumer; then exit 1; fi
if "$work/consumer" > api.stdout 2> api.stderr; then :; else status=$?; cat api.stdout api.stderr; exit "$status"; fi
cat api.stdout; cmp "$qa/expected.stdout" api.stdout; test ! -s api.stderr
if LD_DEBUG=bindings "$work/consumer" > debug.stdout 2> loader.trace; then :; else status=$?; cat debug.stdout loader.trace; exit "$status"; fi
cmp "$qa/expected.stdout" debug.stdout
cat > parse-bindings.awk <<'AWK'
BEGIN { n=split("jc_block_hash jc_numeric_strcmp jc_str_init jc_make_relative_link_name jc_fread jc_strtol", names, " "); for(i=1;i<=n;i++) wanted[names[i]]=1 }
/^[[:space:]]*[0-9]+:[[:space:]]+binding file [^[:space:]]+ \[[0-9]+\] to [^[:space:]]+ \[[0-9]+\]: normal symbol [`'][^`']+'$/ {
    line=$0; sub(/^[[:space:]]*[0-9]+:[[:space:]]+/, "", line)
    n=split(line,f,/[[:space:]]+/); if(n!=10) next
    symbol=f[10]; sub(/^[`']/,"",symbol); sub(/'$/,"",symbol)
    if(wanted[symbol]) printf "%s\t%s\t%s\n",f[3],f[6],symbol
}
AWK
gawk -f parse-bindings.awk loader.trace > bindings.tsv
: > bound-symbols
while IFS=$'\t' read -r caller target symbol; do
    if [[ "$caller" != /* || ! "$caller" -ef "$work/consumer" ]]; then continue; fi
    [[ "$target" == /* && "$target" -ef "$library" ]] || { printf 'wrong installed binding %s -> %s\n' "$symbol" "$target" >&2; exit 1; }
    printf '%s\n' "$symbol" >> bound-symbols
    printf 'binding %s PASS same installed file canonical=%s\n' "$symbol" "$(readlink -f "$target")"
    sha256sum "$target"
done < bindings.tsv
for symbol in jc_block_hash jc_numeric_strcmp jc_str_init jc_make_relative_link_name jc_fread jc_strtol; do grep -Fx "$symbol" bound-symbols; done
sha256sum "$library" > library.after; cmp library.before library.after
printf 'installed library canonical=%s\n' "$(readlink -f "$library")"
printf '%s\n' 'libjodycode installed six strict cases and six same-file function bindings PASS'
