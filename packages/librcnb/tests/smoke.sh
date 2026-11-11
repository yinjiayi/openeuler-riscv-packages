#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH LD_PRELOAD CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH LIBRARY_PATH PYTHONPATH PYTHONHOME
export LC_ALL=C.UTF-8
[[ $(locale charmap) == UTF-8 ]]
rpm -q -- librcnb librcnb-devel librcnb-tools
rpm -V librcnb librcnb-devel librcnb-tools
up=/usr/share/librcnb/upstream-originals
qa=/usr/share/librcnb/tests/qa.py
[[ -f $qa && $(rpm -qf --qf '%{NAME}\n' "$qa") == librcnb-devel ]]
[[ $(rpm -qf --qf '%{NAME}\n' /usr/bin/rcnb) == librcnb-tools ]]
for p in "$up"/examples/* /usr/include/rcnb/* "$up"/LICENSE; do
    [[ -f $p && ! -L $p && $(rpm -qf --qf '%{NAME}\n' "$p") == librcnb-devel ]]
done
(cd "$up/examples" && sha256sum -c ../EXAMPLE-SHA256SUMS)
lib=$(readlink -f /usr/lib64/librcnb.so.1)
[[ -f $lib && $(rpm -qf --qf '%{NAME}\n' "$lib") == librcnb ]]
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
gcc -O2 -UNDEBUG -I/usr/include "$up/examples/c-example1.c" -L/usr/lib64 -lrcnb -o "$run_dir/example1"
linked=$(ldd "$run_dir/example1" | awk '$1 == "librcnb.so.1" && $2 == "=>" {print $3}')
[[ $linked == /* && $(readlink -f "$linked") == "$lib" ]]
"$run_dir/example1"
python3 "$up/examples/python3-example.py" > "$run_dir/python-example.txt"
grep -Fx 'The Quick Brown RC Jumps Over the NB Dog. 😄' "$run_dir/python-example.txt"
python3 "$qa" "$lib"
cd "$run_dir"
echo "The Quick Brown RC Jumps Over the NB Dog." > in.txt
rcnb -e in.txt out.rcnb
rcnb -d out.rcnb out.txt
cmp in.txt out.txt
printf AB > two.txt
rcnb -e two.txt two.rcnb
rcnb -d two.rcnb two-out.txt
cmp two.txt two-out.txt
echo 'PASS original-installed-appveyor-vector and exact-two-byte CLI regression'
