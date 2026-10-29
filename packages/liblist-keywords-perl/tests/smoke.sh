#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Keywords
rpm -q --whatprovides 'perl(List::Keywords)'
perl -e '
  use List::Keywords "first";
  die "unexpected List::Keywords version\n"
    unless $List::Keywords::VERSION eq "0.11";
  my @values = (1, 2, 3, 4);
  my $first = first { $_ > 2 } @values;
  die "keyword result mismatch\n" unless $first == 3;
'
