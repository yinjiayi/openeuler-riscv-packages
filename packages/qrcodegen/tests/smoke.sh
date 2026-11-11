#!/bin/bash
set -euo pipefail
run_installed_demos() {
    root=$1
    qa="$root/usr/share/qrcodegen/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=c99 -I"$root/usr/include/qrcodegen" "$qa/c-demo.c" "$root/usr/lib64/libqrcodegen.a" -o "$temp/c-demo"
    g++ -O2 -g -UNDEBUG -std=c++11 -I"$root/usr/include/qrcodegen" "$qa/cpp-demo.cpp" "$root/usr/lib64/libqrcodegencpp.a" -o "$temp/cpp-demo"
    "$temp/c-demo" > "$temp/c.out"
    "$temp/cpp-demo" > "$temp/cpp.out"
    cmp "$qa/c-demo.expected" "$temp/c.out"
    cmp "$qa/cpp-demo.expected" "$temp/cpp.out"
    rm -f "$temp/c-demo" "$temp/cpp-demo" "$temp/c.out" "$temp/cpp.out"
    rmdir "$temp"
    echo 'PASS qrcodegen complete original C/C++ demos against installed static archives'
}
run_installed_demos ''
