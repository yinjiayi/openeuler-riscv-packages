#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libstatgrab statgrab saidar
test "$(rpm -q --qf '%{VERSION}' libstatgrab)" = '0.92.1'
test -x /usr/bin/statgrab
test -x /usr/bin/saidar
test -x /usr/bin/statgrab-make-mrtg-config
test -x /usr/bin/statgrab-make-mrtg-index
test -s /usr/include/statgrab.h
test "$(pkg-config --modversion libstatgrab)" = '0.92.1'

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/smoke.c" <<'EOF'
#include <statgrab.h>

int main(void) {
    const sg_cpu_stats *stats;
    size_t count = 0;

    if (sg_init(0) != 0)
        return 1;
    stats = sg_get_cpu_stats(&count);
    if (stats == NULL || count == 0)
        return 2;
    sg_shutdown();
    return 0;
}
EOF
${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" $(pkg-config --cflags --libs libstatgrab) -o "$tmpdir/smoke"
"$tmpdir/smoke"

set +e
statgrab_version=$(statgrab -h 2>&1)
statgrab_status=$?
saidar_version=$(saidar -v 2>&1)
saidar_status=$?
set -e
test "$statgrab_status" -eq 1
test "$saidar_status" -eq 1
grep -F 'Version 0.92.1' <<<"$statgrab_version"
grep -F 'version 0.92.1' <<<"$saidar_version"
