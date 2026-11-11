#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH LD_PRELOAD
export LC_ALL=C
rpm -q libcs50 libcs50-devel
rpm -V libcs50 libcs50-devel
library=$(readlink -f /usr/lib64/libcs50.so.11)
[[ $library == /usr/lib64/libcs50.so.11.0.4 ]]
rpm -qf "$library" /usr/lib64/libcs50.a /usr/include/cs50.h
(cd /usr/share/libcs50/tests && sha256sum -c SHA256SUMS)
for name in get_char get_double get_float get_int get_long get_long_long get_string; do
    test -s "/usr/share/man/man3/$name.3.gz"
    gzip -t "/usr/share/man/man3/$name.3.gz"
done
test -s /usr/share/licenses/libcs50/LICENSE
test -s /usr/share/licenses/libcs50/COPYING.BSD-3-Clause
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
printf '#include <cs50.h>\nint main(void) { return get_int(0) == 42 ? 0 : 1; }\n' > "$work/consumer.c"
gcc -std=c11 -Wall -Wextra -pedantic "$work/consumer.c" -lcs50 -o "$work/consumer"
ldd "$work/consumer" > "$work/ldd.txt"
cat "$work/ldd.txt"
linked=$(awk '$1 == "libcs50.so.11" { print $3 }' "$work/ldd.txt")
[[ -n $linked && $(readlink -f "$linked") == "$library" ]]
rpm -qf "$linked"
printf '42\n' | timeout 15 "$work/consumer"
bash /usr/share/libcs50/tests/run-tests.sh /usr/include /usr/lib64 /usr/share/libcs50/tests installed
