#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
unset LD_PRELOAD LD_AUDIT LD_DEBUG_OUTPUT
export LD_LIBRARY_PATH=/usr/lib64
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
tests=/usr/libexec/libucontext-tests
cd "$tests"
sha256sum -c SHA256SUMS
test -r /usr/include/libucontext/libucontext.h
test -r /usr/include/libucontext/bits.h
test -r /usr/lib64/pkgconfig/libucontext.pc
for library in libucontext.so.1 libucontext_posix.so.1 libucontext.a libucontext_posix.a; do
    test -r "/usr/lib64/$library"
done
test "$(readlink /usr/lib64/libucontext.so)" = libucontext.so.1
test "$(readlink /usr/lib64/libucontext_posix.so)" = libucontext_posix.so.1

# Check original test programs and actual loader bindings, not libc-only ABI
# calls. This is functional validation, with no timing/performance claim.
for variant in test_libucontext test_libucontext_posix test_libucontext_bare_posixabi; do
    LD_DEBUG=bindings "$tests/$variant" > "$work/$variant.out" 2> "$work/$variant.bindings"
    grep -F 'looks like all arguments are passed correctly' "$work/$variant.out"
    grep -F 'returned from initial swapcontext' "$work/$variant.out"
    grep -F 'done = 1' "$work/$variant.out"
    if [ "$variant" = test_libucontext ]; then
        for symbol in libucontext_getcontext libucontext_makecontext libucontext_swapcontext libucontext_setcontext; do
            grep -E "binding file .*test_libucontext.* to /usr/lib64/libucontext[.]so[.]1 .*symbol .$symbol." "$work/$variant.bindings"
        done
    else
        for symbol in getcontext makecontext swapcontext setcontext; do
            grep -E "binding file .*${variant}.* to /usr/lib64/libucontext(_posix)?[.]so[.]1 .*symbol .$symbol." "$work/$variant.bindings"
        done
    fi
done

# Preserve original link-order behavior above; additionally exercise the same
# POSIX ELF with the packaged signal-mask implementation explicitly selected.
LD_PRELOAD=/usr/lib64/libucontext_posix.so.1 LD_DEBUG=bindings \
    "$tests/test_libucontext_posix" > "$work/posix-preload.out" 2> "$work/posix-preload.bindings"
grep -F 'looks like all arguments are passed correctly' "$work/posix-preload.out"
grep -F 'returned from initial swapcontext' "$work/posix-preload.out"
grep -F 'done = 1' "$work/posix-preload.out"
for symbol in getcontext swapcontext setcontext; do
    grep -E "binding file .*test_libucontext_posix.* to /usr/lib64/libucontext_posix[.]so[.]1 .*symbol .$symbol." "$work/posix-preload.bindings"
done
printf '%s\n' 'libucontext: three original variants and explicit POSIX binding passed'
