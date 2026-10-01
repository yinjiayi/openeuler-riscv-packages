#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Diff-XS
rpm -q --whatprovides 'perl(Algorithm::Diff::XS)'
perl -MAlgorithm::Diff::XS=LCS -e '
  my @common = LCS([qw(a b c)], [qw(b c d)]);
  die "XS longest-common-subsequence mismatch\n"
    unless join(",", @common) eq "b,c";
'
