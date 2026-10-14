#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH LD_PRELOAD LIBRARY_PATH CPATH CPLUS_INCLUDE_PATH PKG_CONFIG_PATH PKG_CONFIG_LIBDIR
[[ $(rpm -q --qf '%{VERSION}\n' libbinio) == 1.5 ]]
[[ $(rpm -q --qf '%{VERSION}\n' libbinio-devel) == 1.5 ]]
rpm -V libbinio libbinio-devel
[[ $(pkg-config --modversion libbinio) == 1.5 ]]
includedir=$(pkg-config --variable=includedir libbinio)
libdir=$(pkg-config --variable=libdir libbinio)
[[ $includedir == /usr/include && $libdir == /usr/lib64 ]]
for file in "$includedir/libbinio/binio.h" "$includedir/libbinio/binstr.h" "$includedir/libbinio/binwrap.h" "$includedir/libbinio/binfile.h" "$libdir/pkgconfig/libbinio.pc" /usr/share/libbinio/verify-binio.cpp; do
  [[ -f $file && ! -L $file ]]
  [[ $(rpm -qf --qf '%{NAME}\n' "$file") == libbinio-devel ]]
done
library=$(readlink -f "$libdir/libbinio.so")
[[ $library == /usr/lib64/libbinio.so.1.0.0 && -f $library && ! -L $library ]]
[[ $(rpm -qf --qf '%{NAME}\n' "$library") == libbinio ]]
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
g++ -O2 -I"$includedir/libbinio" /usr/share/libbinio/verify-binio.cpp -L"$libdir" -lbinio -lm -o "$run_dir/verify"
ldd "$run_dir/verify"
ldd "$run_dir/verify" | grep -F "libbinio.so.1 => /usr/lib64/libbinio.so.1"
(cd "$run_dir" && ./verify)
