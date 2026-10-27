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
export LC_ALL=C LANG=C PATH=/usr/bin:/bin NO_COLOR=1
unset LD_LIBRARY_PATH LD_PRELOAD
work=$(mktemp -d /tmp/libtree-installed.XXXXXXXX)
finish() {
    status=$?
    trap - EXIT
    set +e
    for raw in "$work"/*; do
        test -f "$raw" || continue
        printf '\nLIBTREE_SMOKE_RAW_BEGIN %s\n' "${raw##*/}" || status=1
        sha256sum "$raw" || status=1
        cat "$raw" || status=1
        printf '\nLIBTREE_SMOKE_RAW_END %s\n' "${raw##*/}" || status=1
    done
    exit "$status"
}
trap finish EXIT
binary=$(command -v libtree)
test "$binary" -ef /usr/bin/libtree
readlink -f "$binary" > "$work/binary-realpath"
sha256sum /usr/bin/libtree > "$work/binary-before.sha256"
sha256sum /usr/libexec/libtree/regressions.py > "$work/helper-before.sha256"
(cd /; sha256sum -c /usr/share/libtree-tests/SHA256SUMS) > "$work/manifest.stdout" 2> "$work/manifest.stderr"
test ! -s "$work/manifest.stderr"
(cd /usr/share/licenses/libtree/source-notices; sha256sum -c SHA256SUMS) > "$work/notices.stdout" 2> "$work/notices.stderr"
test ! -s "$work/notices.stderr"
test "$(find /usr/share/licenses/libtree/source-notices -type f -name '*.notice' | wc -l)" -eq 24
test "$(wc -l < /usr/share/licenses/libtree/source-notices/SHA256SUMS)" -eq 24
readelf -h "$binary" > "$work/elf-header.stdout" 2> "$work/elf-header.stderr"
readelf -d "$binary" > "$work/elf-dynamic.stdout" 2> "$work/elf-dynamic.stderr"
test ! -s "$work/elf-header.stderr" && test ! -s "$work/elf-dynamic.stderr"
grep -Eq 'Class:[[:space:]]+ELF64' "$work/elf-header.stdout"
grep -Eq 'Machine:[[:space:]]+RISC-V' "$work/elf-header.stdout"
grep -Fq 'Shared library: [libc.so.6]' "$work/elf-dynamic.stdout"
if grep -Eq '\((RPATH|RUNPATH)\)' "$work/elf-dynamic.stdout"; then exit 1; else test "$?" -eq 1; fi
python3 /usr/libexec/libtree/regressions.py "$binary" > "$work/regressions.stdout" 2> "$work/regressions.stderr" || { status=$?; cat "$work/regressions.stdout" "$work/regressions.stderr"; exit "$status"; }
test ! -s "$work/regressions.stderr"
grep -E '^ok [1-6] - |^libtree-cli: 6 groups passed$' "$work/regressions.stdout" > "$work/groups.txt"
cmp /usr/share/libtree-tests/expected-groups.txt "$work/groups.txt"
sha256sum /usr/bin/libtree > "$work/binary-after.sha256"
cmp "$work/binary-before.sha256" "$work/binary-after.sha256"
sha256sum /usr/libexec/libtree/regressions.py > "$work/helper-after.sha256"
cmp "$work/helper-before.sha256" "$work/helper-after.sha256"
printf 'libtree installed strict CLI smoke: PASS\n'
