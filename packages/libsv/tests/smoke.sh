#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH LD_PRELOAD CPATH C_INCLUDE_PATH LIBRARY_PATH
rpm -q -- libsv libsv-devel
rpm -V libsv libsv-devel
[[ $(pkg-config --modversion libsv) == 1.0.0 ]]
includedir=$(pkg-config --variable=includedir libsv)
libdir=$(pkg-config --variable=libdir libsv)
[[ $includedir == /usr/include && $libdir == /usr/lib64 ]]
for file in "$includedir/sv/semver.h" "$libdir/pkgconfig/libsv.pc" \
    /usr/share/libsv/tests/SHA256SUMS /usr/share/libsv/tests/*.c; do
    [[ -f $file && ! -L $file ]]
    [[ $(rpm -qf --qf '%{NAME}\n' "$file") == libsv-devel ]]
done
(cd /usr/share/libsv/tests && sha256sum -c SHA256SUMS)
library=$(readlink -f "$libdir/libsv.so.1")
[[ -f $library && $(rpm -qf --qf '%{NAME}\n' "$library") == libsv ]]
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
for name in version comp match range semvers utils usage; do
    gcc -O2 -UNDEBUG -std=c99 -I"$includedir/sv" \
        /usr/share/libsv/tests/$name.c $(pkg-config --cflags --libs libsv) \
        -o "$run_dir/$name"
    ldd "$run_dir/$name"
    linked=$(ldd "$run_dir/$name" | awk '$1 == "libsv.so.1" && $2 == "=>" {print $3}')
    [[ $linked == /* && $(readlink -f "$linked") == "$library" ]]
    (cd "$run_dir" && ./$name)
    echo "PASS original-installed $name"
done
