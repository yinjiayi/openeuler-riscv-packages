#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- qpdf
qpdf --version | grep -F 'qpdf version 12.3.2'

smoke_dir=$(mktemp -d)
trap 'rm -r -- "$smoke_dir"' EXIT
qpdf --empty "$smoke_dir/empty.pdf"
test "$(qpdf --show-npages "$smoke_dir/empty.pdf")" = 0
qpdf --check "$smoke_dir/empty.pdf"
