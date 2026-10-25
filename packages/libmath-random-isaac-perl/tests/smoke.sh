#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Random-ISAAC
rpm -q --whatprovides 'perl(Math::Random::ISAAC)'
perl -MMath::Random::ISAAC -e '
  die "unexpected version\n" unless $Math::Random::ISAAC::VERSION eq "1.004";
  die "pure-Perl backend not selected\n" unless $Math::Random::ISAAC::DRIVER eq "PP";
  my $a = Math::Random::ISAAC->new(1, 2, 3);
  my $b = Math::Random::ISAAC->new(1, 2, 3);
  for (1..8) {
    my $x = $a->irand();
    my $y = $b->irand();
    die "seeded sequence differs\n" unless $x == $y;
    die "integer outside 32-bit range\n" unless $x >= 0 && $x <= 4294967295;
  }
  my $fraction = $a->rand();
  die "fraction outside range\n" unless $fraction >= 0 && $fraction < 1;
'
