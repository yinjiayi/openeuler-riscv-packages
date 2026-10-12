#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Rotation-Cycle
rpm -q --whatprovides 'perl(List::Rotation::Cycle)'
perl -MList::Rotation::Cycle -e '
  die "unexpected version\n" unless $List::Rotation::Cycle::VERSION eq "1.009";
  my $cycle = List::Rotation::Cycle->new(qw(a b c));
  my $observed = join q{,}, map { $cycle->next } 1..4;
  die "cycle mismatch\n" unless $observed eq q{a,b,c,a};
'
