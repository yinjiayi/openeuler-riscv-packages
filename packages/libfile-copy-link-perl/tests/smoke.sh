#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Copy-Link
rpm -q --whatprovides 'perl(File::Copy::Link)'
rpm -q --whatprovides 'perl(File::Spec::Link)'
command -v copylink
test_dir="$(mktemp -d)"
trap 'rm -f -- "$test_dir/source" "$test_dir/link"; rmdir -- "$test_dir"' EXIT
printf 'copy-link-roundtrip\n' > "$test_dir/source"
ln -s source "$test_dir/link"
copylink "$test_dir/link"
test -f "$test_dir/link"
test ! -L "$test_dir/link"
cmp -s -- "$test_dir/source" "$test_dir/link"
