#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Combinatorics
rpm -q --whatprovides 'perl(Math::Combinatorics)'
perl -MMath::Combinatorics -e '
  die "unexpected version\n" unless $Math::Combinatorics::VERSION eq "0.09";
  my $iterator = Math::Combinatorics->new(data => [qw(a b c d)], count => 2);
  my $count = 0;
  $count++ while $iterator->next_combination;
  die "expected six combinations, got $count\n" unless $count == 6;
'
