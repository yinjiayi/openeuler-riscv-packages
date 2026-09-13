#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- recutils recutils-libs recutils-devel recutils-bash-builtins
recsel --version | grep -F 'recsel (GNU recutils) 1.9'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
recfile="$smoke_dir/packages.rec"
cat >"$recfile" <<'EOF'
%rec: Package
%type: Count int

Name: compiler
Arch: riscv64
Count: 2

Name: emulator
Arch: x86_64
Count: 1
EOF

test "$(recsel -e 'Count > 1' -P Name "$recfile")" = compiler
recfix --check "$recfile"

printf 'Name,Arch\nrunner,riscv64\n' | csv2rec >"$smoke_dir/from-csv.rec"
rec2csv "$smoke_dir/from-csv.rec" >"$smoke_dir/roundtrip.csv"
test "$(sed -n '2p' "$smoke_dir/roundtrip.csv")" = '"runner","riscv64"'

cat >"$smoke_dir/rec-smoke.c" <<'EOF'
#include <rec.h>

int main(void) {
    rec_db_t database = rec_db_new();
    if (database == NULL) {
        return 1;
    }
    rec_db_destroy(database);
    return 0;
}
EOF
cc "$smoke_dir/rec-smoke.c" -o "$smoke_dir/rec-smoke" -lrec
"$smoke_dir/rec-smoke"

libdir=$(rpm --eval '%{_libdir}')
enable -f "$libdir/readrec.so" readrec
enable -f "$libdir/testrec.so" testrec
help readrec >/dev/null
test "$(type -t '[%')" = builtin

printf 'Name: compiler\nCount: 2\n\n' >"$smoke_dir/builtin.rec"
Name=
Count=
readrec <"$smoke_dir/builtin.rec"
test "$Name" = compiler
test "$Count" = 2
command '[%' 'Name = "compiler"' '%]'
if command '[%' 'Name = "emulator"' '%]'; then
    echo 'testrec unexpectedly matched a different record' >&2
    exit 1
fi
