#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bzip3 bzip3-devel
installed_version=$(rpm -q --qf '%{VERSION}' bzip3)
bzip3 -V | grep -F "$installed_version"
test -r /usr/include/libbz3.h
test -r /usr/lib64/libbzip3.so.0
tmpdir=$(mktemp -d)
sample="$tmpdir/sample"
compressed="$tmpdir/compressed.bz3"
restored="$tmpdir/restored"
trap 'rm -f -- "$sample" "$compressed" "$restored"; rmdir -- "$tmpdir"' EXIT
printf 'openEuler RVA23 bzip3 smoke\n' > "$sample"
bzip3 -e "$sample" "$compressed"
bzip3 -d "$compressed" "$restored"
cmp "$sample" "$restored"
