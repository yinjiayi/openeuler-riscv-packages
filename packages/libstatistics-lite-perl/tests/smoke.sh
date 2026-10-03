#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Statistics-Lite
rpm -q --whatprovides 'perl(Statistics::Lite)'
perl -MStatistics::Lite=:all -e '
  die "unexpected Statistics::Lite version\n"
    unless $Statistics::Lite::VERSION eq "3.62";
  die "mean mismatch\n" unless mean(1, 2, 3) == 2;
  die "median mismatch\n" unless median(3, 1, 2) == 2;
  die "mode mismatch\n" unless mode(1, 1, 2) == 1;
  die "variance mismatch\n" unless variance(1, 2, 3) == 1;
  my %frequencies = frequencies(1, 1, 2);
  die "frequency mismatch\n"
    unless $frequencies{1} == 2 && $frequencies{2} == 1;
'
