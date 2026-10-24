#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Munkres
rpm -q --whatprovides 'perl(Algorithm::Munkres)'
perl -MAlgorithm::Munkres -e '
  die "unexpected Algorithm::Munkres version\n"
    unless $Algorithm::Munkres::VERSION eq "0.08";
  my @matrix = ([2, 4, 7], [3, 9, 5], [8, 2, 9]);
  my @assigned;
  assign(\@matrix, \@assigned);
  die "assignment result mismatch\n"
    unless join(",", @assigned) eq "0,2,1";
'
