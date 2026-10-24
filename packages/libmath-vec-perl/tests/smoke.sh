#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Vec
rpm -q --whatprovides 'perl(Math::Vec)'
perl -MMath::Vec -e '
  die "unexpected version\n" unless $Math::Vec::VERSION eq "1.01";
  my $a = Math::Vec->new(3, 4, 0);
  die "length mismatch\n" unless abs($a) == 5;
  my $b = Math::Vec->new(0, 1, 0);
  die "dot mismatch\n" unless $a->Dot($b) == 4;
  my @cross = $a->Cross($b);
  die "cross mismatch\n" unless join(",", @cross) eq "0,0,3";
'
