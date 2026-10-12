#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Vector-Real
rpm -q --whatprovides 'perl(Math::Vector::Real)'
rpm -q --whatprovides 'perl(Math::Vector::Real::Test)'
perl -MMath::Vector::Real -MMath::Vector::Real::Test -e '
  die "unexpected version\n" unless $Math::Vector::Real::VERSION eq "0.18";
  my $x = V(3, 4, 0);
  my $y = V(0, 1, 0);
  die "norm mismatch\n" unless abs($x) == 5;
  die "dot mismatch\n" unless $x * $y == 4;
  die "cross mismatch\n" unless $x x $y == [0, 0, 3];
'
