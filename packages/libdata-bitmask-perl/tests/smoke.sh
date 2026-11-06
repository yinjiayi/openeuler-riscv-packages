#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-BitMask
rpm -q --whatprovides 'perl(Data::BitMask)'
perl -e '
  use Data::BitMask;
  die "unexpected Data::BitMask version\n"
    unless $Data::BitMask::VERSION eq "1.00";
  my $mask = Data::BitMask->new(A => 1, B => 2, C => 4);
  die "named mask mismatch\n" unless $mask->build_mask("A|C") == 5;
'
