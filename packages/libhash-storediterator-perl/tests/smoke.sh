#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-StoredIterator
rpm -q --whatprovides 'perl(Hash::StoredIterator)'
perl -MHash::StoredIterator=:all -e '
  die "unexpected Hash::StoredIterator version\n"
    unless $Hash::StoredIterator::VERSION eq "0.008";
  my %hash = (alpha => 1, beta => 2);
  my @keys = sort { $a cmp $b } hkeys %hash;
  die "independent hash keys mismatch\n"
    unless join(",", @keys) eq "alpha,beta";
'
