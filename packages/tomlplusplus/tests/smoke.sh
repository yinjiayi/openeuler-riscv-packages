#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler supplementary packaging contributors.
set -euo pipefail
qa=/usr/share/tomlplusplus-tests
license=/usr/share/licenses/tomlplusplus
if test ! -d "$license/source-notices"; then
    license=/usr/share/licenses/tomlplusplus-3.4.0
fi
test -d "$license/source-notices"
(cd "$license/source-notices" && sha256sum -c SHA256SUMS)
test "$(wc -l < "$license/source-notices/SHA256SUMS")" -eq 212
test -f "$license/LICENSE"
test -f "$license/Apache-2.0.txt"
test -f "$license/foreign-notices.txt"
echo '2743e3fe04c63ad491c3b5069ca901ec0d9bae3ad5ed99486252442281251309  '"$license/foreign-notices.txt" | sha256sum -c -
exec "$qa/run-qa.sh" /usr
