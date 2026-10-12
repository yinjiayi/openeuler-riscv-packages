#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Set-Scalar
rpm -q --whatprovides 'perl(Set::Scalar)'
module_file="$(perl -MSet::Scalar -e 'print $INC{"Set/Scalar.pm"}')"
test -n "$module_file"
rpm -qf -- "$module_file"

perl -MSet::Scalar -e '
  die "unexpected version\n" unless $Set::Scalar::VERSION eq "1.29";
  my $left = Set::Scalar->new(qw(alpha beta));
  my $right = Set::Scalar->new(qw(beta gamma));
  die "membership failed\n" unless $left->has("alpha") && !$left->has("gamma");
  my $union = $left->union($right);
  die "union failed\n"
    unless $union->size == 3 && $union->has("alpha")
      && $union->has("beta") && $union->has("gamma");
  my $intersection = $left->intersection($right);
  die "intersection failed\n"
    unless $intersection->size == 1 && $intersection->has("beta");
  my $difference = $left->difference($right);
  die "difference failed\n"
    unless $difference->size == 1 && $difference->has("alpha");
  die "source set mutated\n" unless $left->size == 2 && $right->size == 2;
'
