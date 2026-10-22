#!/bin/bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
root=
if [ "${1:-}" = --staged ]; then
    [ "$#" -eq 2 ]
    root=$2
    [ -n "$root" ] && [ -d "$root/usr/lib64" ]
elif [ "$#" -ne 0 ]; then
    exit 2
fi
data="$root/usr/share/liquid-dsp/tests"
programs="$root/usr/libexec/liquid-dsp"
lib="$root/usr/lib64/libliquid.so.1.8.3"
test -f "$lib"
readelf -d "$lib" | grep -E 'SONAME.*\[libliquid\.so\.1\]'
readelf -d "$lib" | grep -E 'NEEDED.*\[libfftw3f\.so\.3\]'
test -f "$root/usr/share/liquid-dsp/corresponding-source/fftw-3.3.10-3.oe2403sp3.src.rpm"
printf '%s  %s\n' \
    f0ebf856e2a01df5c04e421e4e98e2cc0ab05ddac8d1ac69111effba7dbde195 \
    "$root/usr/share/liquid-dsp/corresponding-source/fftw-3.3.10-3.oe2403sp3.src.rpm" | sha256sum -c -
if [ -z "$root" ]; then
    rpm -V liquid-dsp liquid-dsp-devel liquid-dsp-tests
fi
work=$(mktemp -d "${TMPDIR:-/tmp}/liquid-installed-qa.XXXXXXXX")
printf 'Installed QA raw output directory: %s\n' "$work"
export LD_LIBRARY_PATH="$root/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
python3 "$data/run-originals.py" --programs "$programs" --data "$data" --output "$work/originals"
export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig:$root/usr/share/pkgconfig"
if [ -n "$root" ]; then
    export PKG_CONFIG_SYSROOT_DIR="$root"
fi
test "$(pkg-config --modversion liquid-dsp)" = 1.8.3
gcc -std=c11 -Wall -Wextra -Werror "$data/consumer.c" \
    $(pkg-config --cflags --libs liquid-dsp) -lm -o "$work/consumer-pkgconfig"
"$work/consumer-pkgconfig"
cmake -S "$data" -B "$work/cmake" -Dliquid_DIR="$root/usr/lib64/cmake/liquid"
cmake --build "$work/cmake"
"$work/cmake/consumer"
printf 'liquid-dsp: installed originals 191 + 1349, FFTW/SONAME/source, PC and CMake consumers passed\n'
