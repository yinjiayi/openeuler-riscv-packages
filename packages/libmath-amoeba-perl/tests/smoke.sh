#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Amoeba
rpm -q --whatprovides 'perl(Math::Amoeba)'
perl -MMath::Amoeba=MinimiseND -e '
  die "unexpected version\n" unless $Math::Amoeba::VERSION eq "0.05";
  my $objective = sub { my ($x, $y) = @_; return ($x - 2)**2 + ($y + 3)**2 };
  my ($point, $cost) = MinimiseND([0, 0], [1, 1], $objective, 1e-7, 10000);
  die "bad minimum cost: $cost\n" unless $cost < 1e-5;
  die "bad minimum point\n" unless abs($point->[0] - 2) < 0.01 && abs($point->[1] + 3) < 0.01;
'
