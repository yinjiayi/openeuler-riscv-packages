#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Loops
perl -MAlgorithm::Loops=Filter,MapCar,NextPermuteNum -e '
  die "unexpected version\n" unless $Algorithm::Loops::VERSION eq "1.032";
  my @doubled = Filter { $_ *= 2 } (1, 2, 3, 4);
  die "Filter result mismatch\n" unless join(",", @doubled) eq "2,4,6,8";
  my @sum = MapCar { $_[0] + $_[1] } [1, 2], [4, 5];
  die "MapCar result mismatch\n" unless join(",", @sum) eq "5,7";
  my @permutation = (1, 2, 3);
  die "NextPermuteNum result mismatch\n"
    unless NextPermuteNum(@permutation)
       && join(",", @permutation) eq "1,3,2";
'
