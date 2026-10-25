#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-File-Tail
rpm -q --whatprovides 'perl(File::Tail)'
test_file="$(mktemp)"
trap 'rm -f -- "$test_file"' EXIT
printf 'file-tail-roundtrip\n' > "$test_file"
perl -MFile::Tail -e '
  die "unexpected File::Tail version\n"
    unless $File::Tail::VERSION eq "1.3";
  my $tail = File::Tail->new(name => $ARGV[0], tail => -1,
                             interval => 1, maxinterval => 2,
                             adjustafter => 2, errmode => "return");
  die "cannot open test file\n" unless $tail;
  my $line = $tail->read;
  die "unexpected tail contents\n" unless $line eq "file-tail-roundtrip\n";
' "$test_file"
