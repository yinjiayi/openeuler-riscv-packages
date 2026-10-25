#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-Diff
perl -MAlgorithm::Diff=LCS,diff -MAlgorithm::DiffOld -e '
  die "unexpected Algorithm::Diff version\n"
    unless $Algorithm::Diff::VERSION eq "1.201";
  my @left = qw(a b c);
  my @right = qw(a x c);
  die "LCS mismatch\n" unless join(",", LCS(\@left, \@right)) eq "a,c";
  my @changes = diff(\@left, \@right);
  die "edit difference mismatch\n" unless @changes == 1;
  die "legacy comparison interface mismatch\n"
    unless join(",", Algorithm::DiffOld::LCS(
      \@left, \@right, sub { $_[0] eq $_[1] })) eq "a,c";
'
