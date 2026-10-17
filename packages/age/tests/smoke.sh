#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- age
for command in age age-keygen age-inspect age-plugin-batchpass; do
    test -x "/usr/bin/${command}"
    "${command}" --version | grep -Fx 'v1.3.1'
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

printf 'openEuler riscv64 age smoke\n' >"$smoke_dir/plaintext"
age-keygen -o "$smoke_dir/identity" 2>"$smoke_dir/keygen.log"
recipient=$(age-keygen -y "$smoke_dir/identity")
test -n "$recipient"
age -r "$recipient" -o "$smoke_dir/ciphertext" "$smoke_dir/plaintext"
age -d -i "$smoke_dir/identity" -o "$smoke_dir/decrypted" "$smoke_dir/ciphertext"
cmp "$smoke_dir/plaintext" "$smoke_dir/decrypted"
age-inspect --json "$smoke_dir/ciphertext" | grep -F 'age-encryption.org/v1'
