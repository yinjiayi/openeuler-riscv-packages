#!/usr/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy at https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. Full text ships with the package.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_LIBRARY_PATH LD_PRELOAD
work=$(mktemp -d /tmp/sipcalc-installed.XXXXXXXX)
finish() {
    status=$?
    trap - EXIT
    set +e
    for raw in "$work"/*; do
        test -f "$raw" || continue
        printf '\nSIPCALC_SMOKE_RAW_BEGIN %s\n' "${raw##*/}" || status=1
        sha256sum "$raw" || status=1
        cat "$raw" || status=1
        printf '\nSIPCALC_SMOKE_RAW_END %s\n' "${raw##*/}" || status=1
    done
    exit "$status"
}
trap finish EXIT
binary=$(command -v sipcalc)
test "$binary" -ef /usr/bin/sipcalc
readlink -f "$binary" > "$work/binary-realpath"
sha256sum /usr/bin/sipcalc > "$work/binary-before.sha256"
(cd /; sha256sum -c /usr/share/sipcalc-tests/SHA256SUMS) > "$work/installed-manifest.stdout" 2> "$work/installed-manifest.stderr"
test ! -s "$work/installed-manifest.stderr"
(cd /usr/share/licenses/sipcalc/source-notices; sha256sum -c SHA256SUMS) > "$work/notice-check.stdout" 2> "$work/notice-check.stderr"
test ! -s "$work/notice-check.stderr"
test "$(find /usr/share/licenses/sipcalc/source-notices -type f -name '*.notice' | wc -l)" -eq 32
test "$(wc -l < /usr/share/licenses/sipcalc/source-notices/SHA256SUMS)" -eq 32
readelf -h /usr/bin/sipcalc > "$work/elf-header.stdout" 2> "$work/elf-header.stderr"
readelf -d /usr/bin/sipcalc > "$work/elf-dynamic.stdout" 2> "$work/elf-dynamic.stderr"
test ! -s "$work/elf-header.stderr" && test ! -s "$work/elf-dynamic.stderr"
grep -Eq 'Class:[[:space:]]+ELF64' "$work/elf-header.stdout"
grep -Eq 'Machine:[[:space:]]+RISC-V' "$work/elf-header.stdout"
grep -Fq 'Shared library: [libc.so.6]' "$work/elf-dynamic.stdout"
if grep -Eq '\((RPATH|RUNPATH)\)' "$work/elf-dynamic.stdout"; then exit 1; else test "$?" -eq 1; fi
bash /usr/libexec/sipcalc/run-regressions.sh "$binary" /usr/bin/sipcalc /usr/share/sipcalc-tests/expected-version.txt > "$work/regressions.stdout" 2> "$work/regressions.stderr" || { status=$?; cat "$work/regressions.stdout" "$work/regressions.stderr"; exit "$status"; }
test ! -s "$work/regressions.stderr"
gawk '/^sipcalc case0[1-6] .*: PASS$/{n++} END{exit(n!=6)}' "$work/regressions.stdout"
test "$(grep -c '^sipcalc strict CLI: 6 cases PASS$' "$work/regressions.stdout")" -eq 1
sha256sum /usr/bin/sipcalc > "$work/binary-after.sha256"
cmp "$work/binary-before.sha256" "$work/binary-after.sha256"
printf 'sipcalc installed strict CLI smoke: PASS\n'
