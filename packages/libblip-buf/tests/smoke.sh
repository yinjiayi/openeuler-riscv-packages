#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libblip-buf
manifest=$(rpm -ql -- libblip-buf | grep '/source-notices/SHA256SUMS$')
case "$manifest" in
    /usr/share/licenses/libblip-buf/source-notices/SHA256SUMS|/usr/share/licenses/libblip-buf-1.1.1/source-notices/SHA256SUMS) ;;
    *) exit 1;;
esac
test "$(wc -l < "$manifest")" -eq 8
(cd "$(dirname "$manifest")" && sha256sum -c SHA256SUMS)
bash /usr/share/libblip-buf-tests/run-qa.sh ''
