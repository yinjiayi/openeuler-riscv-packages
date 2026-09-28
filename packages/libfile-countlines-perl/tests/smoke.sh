#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-CountLines
rpm -q --whatprovides 'perl(File::CountLines)'
test_file="$(mktemp)"
trap 'rm -f -- "$test_file"' EXIT
printf 'alpha\nbeta\n' > "$test_file"
perl -MFile::CountLines=count_lines -e '
  die "unexpected File::CountLines version\n" unless $File::CountLines::VERSION eq "0.0.3";
  die "line-break count failed\n" unless count_lines($ARGV[0]) == 2;
' "$test_file"
