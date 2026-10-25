#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Sort
rpm -q --whatprovides 'perl(File::Sort)'
test_dir="$(mktemp -d)"
trap 'rm -f -- "$test_dir/input" "$test_dir/output"; rmdir -- "$test_dir"' EXIT
printf '3\n1\n2\n' > "$test_dir/input"
perl -MFile::Sort=sort_file -e '
  die "unexpected File::Sort version\n" unless $File::Sort::VERSION eq "1.01";
  sort_file({ I => $ARGV[0], o => $ARGV[1], n => 1 });
' "$test_dir/input" "$test_dir/output"
printf '1\n2\n3\n' | cmp -s - "$test_dir/output"
