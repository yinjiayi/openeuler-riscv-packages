#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Combinatorics
rpm -q --whatprovides 'perl(Algorithm::Combinatorics)'
perl -MAlgorithm::Combinatorics=combinations -e '
  die "unexpected Algorithm::Combinatorics version\n"
    unless $Algorithm::Combinatorics::VERSION eq "0.27";
  my @pairs = combinations([1, 2, 3], 2);
  die "combination result mismatch\n"
    unless join(";", map { join(",", @$_) } @pairs) eq "1,2;1,3;2,3";
'
