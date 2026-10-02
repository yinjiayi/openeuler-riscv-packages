#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Cartesian-Product
rpm -q --whatprovides 'perl(Math::Cartesian::Product)'
perl -MMath::Cartesian::Product -e '
  die "unexpected Math::Cartesian::Product version\n"
    unless $Math::Cartesian::Product::VERSION eq "1.009";
  my @pairs = cartesian { 1 } [qw(a b)], [1, 2];
  die "Cartesian product count mismatch\n" unless @pairs == 4;
  die "Cartesian product contents mismatch\n"
    unless join(",", map { join "", @$_ } @pairs) eq "a1,a2,b1,b2";
'
