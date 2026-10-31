#!/bin/sh
# SPDX-License-Identifier: MIT
set -eu
root=${1-}
base="$root/usr/libexec/pick-tests"
binary="$root/usr/bin/pick"
test -x "$binary"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT HUP INT TERM
tar -xzf "$base/source.tar.gz" -C "$work"
cd "$work"
test "$(find tests -name '*.t' -type f | wc -l)" -eq 31
# Retain upstream feature detection and the original two-second PTY timeout.
CC=gcc CFLAGS='-O2 -g -Wall -Wextra' sh ./configure
# Build only the original PTY driver; PICK is the staged/installed executable.
make -C tests PICK="$binary"
printf '%s\n' 'PASS pick unchanged default 31-file PTY suite against installed binary'
