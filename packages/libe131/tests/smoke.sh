#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_LIBRARY_PATH LD_AUDIT LD_DEBUG LD_DEBUG_OUTPUT LD_BIND_NOW LIBRARY_PATH CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH GCC_EXEC_PREFIX COMPILER_PATH CFLAGS CPPFLAGS LDFLAGS
data=/usr/share/libe131-tests
library=/usr/lib64/libe131.so.1.0.4
license=/usr/share/licenses/libe131
if [ ! -d "$license" ]; then license=/usr/share/licenses/libe131-1.4.0; fi
test -s "$library" && test -s /usr/lib64/libe131.a && test -s /usr/include/e131.h
for notice in LICENSE GPL-2.0.txt GPL-3.0.txt Shelby-Merrick-E131.h.notice Shelby-Merrick-E131.cpp.notice; do test -s "$license/$notice"; done
test "$(wc -l < "$license/source-notices/SHA256SUMS")" -eq 23
test "$(find "$license/source-notices" -type f -name '*.notice' | wc -l)" -eq 23
(cd "$license/source-notices"; sha256sum -c SHA256SUMS)
(cd /; sha256sum -c "$data/SHA256SUMS")
printf '%s  %s\n' edaef632cbb643e4e7a221717a6c441a4c1a7c918e6e4d56debc3d8739b233f6 "$license/GPL-2.0.txt" | sha256sum -c -
printf '%s  %s\n' 3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986 "$license/GPL-3.0.txt" | sha256sum -c -
work=$(mktemp -d)
cleanup() {
    status=$?
    trap - EXIT
    for raw in negative.stdout negative.stderr negative.status link.stdout link.stderr library.nm library.elf library.dynamic consumer.elf consumer.dynamic normal.stdout normal.stderr loader.stdout loader.stderr bindings.tsv objects.before objects.after; do
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
sha256sum "$library" /usr/lib64/libe131.a /usr/include/e131.h > objects.before
symbols='e131_pkt_init e131_pkt_validate e131_get_option e131_set_option e131_multicast_dest e131_dest_str e131_pkt_discard e131_pkt_dump e131_strerror'
if gcc -O2 -std=gnu11 -Wall -Wextra -Werror -UNDEBUG -I/usr/include "$data/api-smoke.c" -o "$work/negative" > negative.stdout 2> negative.stderr; then
    printf '%s\n' 0 > negative.status
    echo 'unexpected missing-library link success' >&2
    exit 1
else
    status=$?
    printf '%s\n' "$status" > negative.status
fi
test "$status" -ne 0 && test ! -e "$work/negative" && test ! -s negative.stdout
for symbol in $symbols; do grep -E "undefined reference to .*${symbol}" negative.stderr > /dev/null; done
if gcc -O2 -std=gnu11 -Wall -Wextra -Werror -UNDEBUG -I/usr/include "$data/api-smoke.c" -L/usr/lib64 -le131 -o "$work/consumer" > link.stdout 2> link.stderr; then :; else
    status=$?; exit "$status"
fi
test ! -s link.stderr
nm -D --defined-only "$library" > library.nm
for symbol in $symbols; do grep -E " [Tt] ${symbol}$" library.nm > /dev/null; done
readelf -h "$library" > library.elf
readelf -d "$library" > library.dynamic
readelf -h "$work/consumer" > consumer.elf
readelf -d "$work/consumer" > consumer.dynamic
for header in library.elf consumer.elf; do
    grep -E 'Class:[[:space:]]+ELF64' "$header" > /dev/null
    grep -E 'Machine:[[:space:]]+RISC-V' "$header" > /dev/null
done
grep -E '\(SONAME\).*\[libe131\.so\.1\]' library.dynamic > /dev/null
grep -E '\(NEEDED\).*\[libe131\.so\.1\]' consumer.dynamic > /dev/null
if grep -E '\((RPATH|RUNPATH)\)' consumer.dynamic; then exit 1; fi
if "$work/consumer" > normal.stdout 2> normal.stderr; then :; else status=$?; exit "$status"; fi
cmp "$data/expected.stdout" normal.stdout
test ! -s normal.stderr
if LD_DEBUG=bindings LD_BIND_NOW=1 "$work/consumer" > loader.stdout 2> loader.stderr; then :; else
    status=$?; cat loader.stderr >&2; exit "$status"
fi
cmp "$data/expected.stdout" loader.stdout
gawk '
BEGIN { quote=sprintf("%c",39); rx="binding file (/[^[]+) \\[[0-9]+\\] to (/[^[]+) \\[[0-9]+\\]: normal symbol `([A-Za-z_][A-Za-z_0-9]*)" quote }
match($0,rx,m) { print m[1] "\t" m[2] "\t" m[3] }
' loader.stderr > bindings.tsv
tab=$(printf '\t')
for symbol in $symbols; do
    count=0
    while IFS="$tab" read -r caller target name extra; do
        test -z "${extra:-}"
        if [ "$name" = "$symbol" ]; then
            test "$caller" -ef "$work/consumer"
            test "$target" -ef "$library"
            count=$((count+1))
        fi
    done < bindings.tsv
    test "$count" -eq 1
done
sha256sum "$library" /usr/lib64/libe131.a /usr/include/e131.h > objects.after
cmp objects.before objects.after
sha256sum "$work/consumer"
cat normal.stdout
echo 'installed libe131 ELF and nine same-file shared bindings PASS'
