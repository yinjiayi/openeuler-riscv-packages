#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nasm
installed_version=$(rpm -q --qf '%{VERSION}' nasm)
nasm --version | grep -F "NASM version $installed_version"
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf '%s\n' 'bits 64' 'mov eax, 0x12345678' 'ret' >"$smoke_dir/smoke.asm"
nasm -f bin -o "$smoke_dir/smoke.bin" "$smoke_dir/smoke.asm"
test "$(od -An -tx1 "$smoke_dir/smoke.bin" | tr -d ' \n')" = 'b878563412c3'
ndisasm -b 64 "$smoke_dir/smoke.bin" | grep -F 'mov eax,0x12345678'
