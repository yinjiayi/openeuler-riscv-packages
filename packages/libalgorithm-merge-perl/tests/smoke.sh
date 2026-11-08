#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Merge
rpm -q --whatprovides 'perl(Algorithm::Merge)'
perl -MAlgorithm::Merge=merge -e '
  die "unexpected Algorithm::Merge version\n"
    unless $Algorithm::Merge::VERSION eq "0.08";
  my @ancestor = qw(a b c);
  my @left = qw(a b);
  my @right = qw(a b c);
  my @merged = merge(\@ancestor, \@left, \@right);
  die "three-way merge mismatch\n"
    unless join(",", @merged) eq "a,b";
'
