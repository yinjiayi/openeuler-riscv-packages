#!/bin/bash
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
prefix=/usr
qa=/usr/share/libclaw
if [[ ${1:-} == --staged && $# == 2 ]]; then
    prefix="$2/usr"
    qa="$prefix/share/libclaw"
elif [[ $# != 0 ]]; then
    echo 'usage: run-tests.sh [--staged BUILDROOT]' >&2
    exit 2
fi
[[ $prefix == /* && $qa == /* ]]
if [[ $# == 0 ]]; then rpm -V libclaw libclaw-tests; fi
(cd "$qa/original" && sha256sum -c "$qa/SHA256SUMS")
mapfile -t archives < <(find "$prefix/share/doc/libclaw1/example" -maxdepth 1 -type f -name '*.tar.gz' | sort)
[[ ${#archives[@]} == 21 ]]
for archive in "${archives[@]}"; do test -s "$archive"; done
test -s "$prefix/share/doc/libclaw1/html/index.html"
test -s "$prefix/share/locale/fr/LC_MESSAGES/libclaw.mo"
for module in application configuration_file dynamic_library graphic logger net tween; do
    test -s "$prefix/lib64/libclaw_${module}.a"
    [[ -n $(ar t "$prefix/lib64/libclaw_${module}.a") ]]
done
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
# Run the ORIGINAL complete default installed-example compile suite unchanged.
# It prints failures but returns success; retain it and validate its summary.
bash "$qa/original/check-examples.sh" "$prefix" 2>&1 | tee "$work/original.log"
[[ $(grep -Fxc '21 pass, 0 fail.' "$work/original.log") == 1 ]]
[[ $(grep -c '\[PASS\]' "$work/original.log") == 21 ]]
if grep -q '\[FAIL\]' "$work/original.log"; then exit 1; fi
cmake -S "$qa" -B "$work/consumer" -DCMAKE_PREFIX_PATH="$prefix" \
    -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="${CXXFLAGS:-} -UNDEBUG"
cmake --build "$work/consumer" --parallel 2
"$work/consumer/consumer"
echo 'libclaw: original21 installed-example compiles and separate downstream consumer passed'
