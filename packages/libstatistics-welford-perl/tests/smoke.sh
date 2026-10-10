#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Statistics-Welford
rpm -q --whatprovides 'perl(Statistics::Welford)'
perl -MStatistics::Welford -e '
  die "unexpected Statistics::Welford version\n"
    unless $Statistics::Welford::VERSION eq "0.02";
  my $statistics = Statistics::Welford->new;
  $statistics->add($_) for (1, 2, 3);
  die "count mismatch\n" unless $statistics->n == 3;
  die "extrema mismatch\n"
    unless $statistics->min == 1 && $statistics->max == 3;
  die "mean mismatch\n" unless $statistics->mean == 2;
  die "variance mismatch\n" unless abs($statistics->variance - 1) < 1e-12;
  die "standard deviation mismatch\n"
    unless abs($statistics->standard_deviation - 1) < 1e-12;
'
