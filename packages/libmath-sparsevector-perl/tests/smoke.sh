#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-SparseVector
rpm -q --whatprovides 'perl(Math::SparseVector)'
perl -MMath::SparseVector -e '
  die "unexpected version\n" unless $Math::SparseVector::VERSION eq "0.04";
  my $left = Math::SparseVector->new;
  $left->set(2, 3);
  $left->set(9, 4);
  die "norm mismatch\n" unless $left->norm == 5;
  my $right = Math::SparseVector->new;
  $right->set(2, 2);
  $right->set(9, 1);
  die "dot mismatch\n" unless $left->dot($right) == 10;
  $left->free;
  die "free failed\n" unless $left->isnull;
'
