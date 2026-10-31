#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 yinjiayi
set -euo pipefail
# An optional staged root is only used by %check; empty means installed RPMs.
root="${1:-}"
libdir="${2:-/usr/lib64}"
qa="$root/usr/share/liblogging/qa"
test -d "$qa"
(cd "$qa" && sha256sum --check SHA256SUMS)
if test -z "$root"; then
  rpm -V liblogging liblogging-devel liblogging-tests
fi
test -s "$root$libdir/liblogging-stdlog.a"
test -s "$root$libdir/liblogging-rfc3195.a"
ar t "$root$libdir/liblogging-stdlog.a"
ar t "$root$libdir/liblogging-rfc3195.a"
qa_tmp="$(mktemp -d)"
trap 'rm -rf -- "$qa_tmp"' EXIT
cc="${CC:-cc}"
shared_flags=("-L$root$libdir" -llogging-stdlog)
if test -n "$root"; then
  shared_flags=("-L$root$libdir" "-Wl,-rpath,$root$libdir" -llogging-stdlog)
fi
"$cc" -O2 -Wall -Wextra -I"$root/usr/include/liblogging" \
  "$qa/tester.c" -o "$qa_tmp/tester-shared" "${shared_flags[@]}"
# The original pc file has no Libs.private for journal support; retain that
# file unchanged and provide libsystemd explicitly for the static consumer.
read -r -a journal_libs <<< "$(pkg-config --libs libsystemd)"
"$cc" -O2 -Wall -Wextra -I"$root/usr/include/liblogging" \
  "$qa/tester.c" "$root$libdir/liblogging-stdlog.a" \
  -o "$qa_tmp/tester-static" "${journal_libs[@]}"
for linkage in shared static; do
  "$qa_tmp/tester-$linkage" "file:$qa_tmp/$linkage.log"
  test -s "$qa_tmp/$linkage.log"
  grep -q 'tester: Test' "$qa_tmp/$linkage.log"
  "$qa_tmp/tester-$linkage" -p "file:$qa_tmp/$linkage-pid.log"
  test -s "$qa_tmp/$linkage-pid.log"
  grep -Eq 'tester\[[0-9]+\]: Test' "$qa_tmp/$linkage-pid.log"
done
printf '%s\n' 'Original liblogging tester replayed: shared/static, default/PID'
