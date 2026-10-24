#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Copy-Recursive-Reduced
rpm -q --whatprovides 'perl(File::Copy::Recursive::Reduced)'
source_file="$(mktemp)"
target_file="$(mktemp)"
trap 'rm -f -- "$source_file" "$target_file"' EXIT
printf 'copy-roundtrip\n' > "$source_file"
perl -MFile::Copy::Recursive::Reduced=fcopy -e '
  die "unexpected File::Copy::Recursive::Reduced version\n"
    unless $File::Copy::Recursive::Reduced::VERSION eq "0.008";
  fcopy($ARGV[0], $ARGV[1]) or die "fcopy failed: $!\n";
' "$source_file" "$target_file"
cmp -s -- "$source_file" "$target_file"
