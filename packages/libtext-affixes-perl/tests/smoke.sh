#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Text-Affixes
perl -MText::Affixes -e '
  die "unexpected version\n" unless $Text::Affixes::VERSION eq "0.09";
  my $prefixes = get_prefixes({ min => 2, max => 2 }, "Hello, hello");
  die "prefix counts mismatch\n"
    unless $prefixes->{2}->{He} == 1 && $prefixes->{2}->{he} == 1;
  my $suffixes = get_suffixes({ min => 2, max => 2 }, "Hello, hello");
  die "suffix counts mismatch\n" unless $suffixes->{2}->{lo} == 2;
'
