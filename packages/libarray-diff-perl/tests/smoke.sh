#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Array-Diff
rpm -q --whatprovides 'perl(Array::Diff)'
perl -MArray::Diff -e '
  die "unexpected Array::Diff version\n" unless $Array::Diff::VERSION eq "0.09";
  my $diff = Array::Diff->diff([qw(a b c)], [qw(b c d)]);
  die "added values mismatch\n" unless join(",", @{$diff->added}) eq "d";
  die "deleted values mismatch\n" unless join(",", @{$diff->deleted}) eq "a";
  die "difference count mismatch\n" unless $diff->count == 2;
'
