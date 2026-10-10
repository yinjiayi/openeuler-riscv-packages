#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Statistics-TopK
rpm -q --whatprovides 'perl(Statistics::TopK)'
perl -MStatistics::TopK -e '
  die "unexpected Statistics::TopK version\n"
    unless $Statistics::TopK::VERSION eq "0.02";
  my $counter = Statistics::TopK->new(3);
  $counter->add($_) for (qw(a a a b b c));
  my %counts = $counter->counts;
  die "top-k counts mismatch\n"
    unless $counts{a} == 3 && $counts{b} == 2 && $counts{c} == 1;
  die "top-k keys mismatch\n"
    unless join(",", sort $counter->top) eq "a,b,c";
  die "invalid capacity accepted\n"
    if eval { Statistics::TopK->new(0); 1 };
'
