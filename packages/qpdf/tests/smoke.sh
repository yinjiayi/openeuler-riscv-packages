#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- qpdf
qpdf --version | grep -F 'qpdf version 12.3.2'

smoke_dir=$(mktemp -d)
trap 'rm -r -- "$smoke_dir"' EXIT
qpdf --empty "$smoke_dir/empty.pdf"
test "$(qpdf --show-npages "$smoke_dir/empty.pdf")" = 0

# --empty deliberately creates a zero-page skeleton, not a valid PDF.
# Check a separate one-page fixture from upstream's npages test instead.
fixture_b64="$(dirname -- "${BASH_SOURCE[0]}")/minimal-one-page.pdf.b64"
base64 --decode < "$fixture_b64" > "$smoke_dir/one-page.pdf"
test "$(qpdf --show-npages "$smoke_dir/one-page.pdf")" = 1
qpdf --check "$smoke_dir/one-page.pdf"
qpdf --empty --pages "$smoke_dir/one-page.pdf" 1 -- "$smoke_dir/copied.pdf"
test "$(qpdf --show-npages "$smoke_dir/copied.pdf")" = 1
qpdf --check "$smoke_dir/copied.pdf"
