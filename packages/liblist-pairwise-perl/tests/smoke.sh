#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Pairwise
rpm -q --whatprovides 'perl(List::Pairwise)'
perl -MList::Pairwise=mapp,pair -e '
  die "unexpected List::Pairwise version\n"
    unless $List::Pairwise::VERSION eq "1.03";
  my @sums = mapp { $a + $b } (1, 2, 3, 4);
  die "pairwise map mismatch\n" unless join(",", @sums) eq "3,7";
  my @pairs = pair(a => 1, b => 2);
  die "pair grouping mismatch\n" unless @pairs == 2;
'
