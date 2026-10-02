#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Set-Tiny
rpm -q --whatprovides 'perl(Set::Tiny)'
perl -MSet::Tiny=set -e '
  die "wrong installed version\n" unless $Set::Tiny::VERSION eq "0.06";
  my $left = set(qw(a b c));
  my $right = set(qw(c d));
  die "membership failed\n" unless $left->contains(qw(a c)) && !$left->contains("d");
  die "union failed\n" unless $left->union($right)->as_string eq "(a b c d)";
  die "intersection failed\n" unless $left->intersection($right)->as_string eq "(c)";
  die "difference failed\n" unless $left->difference($right)->as_string eq "(a b)";
'
