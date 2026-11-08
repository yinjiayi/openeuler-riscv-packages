#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Bezier
rpm -q --whatprovides 'perl(Math::Bezier)'
perl -MMath::Bezier -e '
  die "unexpected version\n" unless $Math::Bezier::VERSION eq "0.01";
  my $curve = Math::Bezier->new(0, 0, 10, 20, 30, -20, 40, 0);
  my ($x, $y) = $curve->point(0.5);
  die "unexpected midpoint\n" unless abs($x - 20) < 1e-9 && abs($y) < 1e-9;
  my $points = $curve->curve();
  die "unexpected curve length\n" unless @$points == 40;
'
