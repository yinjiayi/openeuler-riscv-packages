#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Touch
rpm -q --whatprovides 'perl(File::Touch)'
test_file="$(mktemp)"
trap 'rm -f -- "$test_file"' EXIT
perl -MFile::Touch -e '
  die "unexpected File::Touch version\n"
    unless $File::Touch::VERSION eq "0.12";
  my $toucher = File::Touch->new(mtime => 1399156463);
  die "touch failed\n" unless $toucher->touch($ARGV[0]) == 1;
  die "mtime mismatch\n" unless (stat($ARGV[0]))[9] == 1399156463;
' "$test_file"
