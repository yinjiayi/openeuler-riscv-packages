#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT LIBRARY_PATH CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH GCC_EXEC_PREFIX COMPILER_PATH CFLAGS CPPFLAGS LDFLAGS
archive=/usr/lib64/libbf.a
data=/usr/share/libbf-tests
license=/usr/share/licenses/libbf
if [ ! -d "$license" ]; then license=/usr/share/licenses/libbf-2025.06.03; fi
test -s "$archive" && test -s /usr/include/libbf.h
test -s "$license/MIT.notice" && test -s "$license/Apache-2.0.txt"
printf '%s  %s\n' cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 "$license/Apache-2.0.txt" | sha256sum -c -
test "$(wc -l < "$license/source-notices/SHA256SUMS")" -eq 25
set -- "$license"/source-notices/*.notice
test "$#" -eq 25
(cd "$license/source-notices"; sha256sum -c SHA256SUMS)
(cd /; sha256sum -c "$data/SHA256SUMS")
work=$(mktemp -d)
cleanup() {
    status=$?
    trap - EXIT
    # Emit complete evidence, then its digest, on success and every failure.
    for raw in negative.stdout negative.stderr negative.status link.trace link.stderr consumer.map archive.nm consumer.nm consumer.elf consumer.dynamic consumer.stdout consumer.stderr archive.before archive.after; do
        if test -f "$work/$raw"; then
            printf '\nraw %s\n' "$raw"
            cat "$work/$raw"
            sha256sum "$work/$raw"
        fi
    done
    rm -rf "$work"
    exit "$status"
}
trap cleanup EXIT
cd "$work"
sha256sum "$archive" > archive.before
symbols='bf_context_init bf_atof bf_add bf_div bfdec_add bf_sqrtrem'
# Missing-library negative control must fail at link, not unrelated compilation.
if gcc -O2 -Wall -Wextra -Werror -UNDEBUG -I/usr/include "$data/api-smoke.c" -lm -o "$work/negative" > negative.stdout 2> negative.stderr; then
    printf '%s\n' 0 > negative.status
    echo 'unexpected missing-library link success' >&2
    exit 1
else
    status=$?
    printf '%s\n' "$status" > negative.status
fi
test "$status" -ne 0 && test ! -e "$work/negative"
test ! -s negative.stdout
for symbol in $symbols; do
    grep -E "undefined reference to .*${symbol}" negative.stderr > /dev/null
done
if gcc -O2 -Wall -Wextra -Werror -UNDEBUG -I/usr/include "$data/api-smoke.c" -L/usr/lib64 -lbf -lm -Wl,-t,-Map,"$work/consumer.map" -o "$work/consumer" > link.trace 2> link.stderr; then :; else
    status=$?; exit "$status"
fi
test ! -s link.stderr
trace_count=0
while IFS= read -r line; do
    case "$line" in
        /*libbf.a) test -f "$line" && test "$line" -ef "$archive"; trace_count=$((trace_count+1));;
    esac
done < link.trace
test "$trace_count" -eq 1
map_count=0
while IFS= read -r line; do
    case "$line" in
        'LOAD '/*libbf.a) object=${line#LOAD }; test -f "$object" && test "$object" -ef "$archive"; map_count=$((map_count+1));;
    esac
done < consumer.map
test "$map_count" -eq 1
nm -g --defined-only "$archive" > archive.nm
nm -g --defined-only "$work/consumer" > consumer.nm
for symbol in $symbols; do
    grep -E " [Tt] ${symbol}$" archive.nm > /dev/null
    grep -E " [Tt] ${symbol}$" consumer.nm > /dev/null
    grep -E "^[[:space:]]+0x[[:xdigit:]]+[[:space:]]+${symbol}$" consumer.map > /dev/null
done
readelf -h "$work/consumer" > consumer.elf
grep -E 'Class:[[:space:]]+ELF64' consumer.elf > /dev/null
grep -E 'Machine:[[:space:]]+RISC-V' consumer.elf > /dev/null
readelf -d "$work/consumer" > consumer.dynamic
if grep -E '\(NEEDED\).*libbf' consumer.dynamic; then exit 1; fi
if "$work/consumer" > consumer.stdout 2> consumer.stderr; then :; else
    status=$?; exit "$status"
fi
cmp "$data/expected.stdout" consumer.stdout
test ! -s consumer.stderr
sha256sum "$archive" > archive.after
cmp archive.before archive.after
sha256sum "$work/consumer"
echo 'installed exact static archive and six symbols PASS'
