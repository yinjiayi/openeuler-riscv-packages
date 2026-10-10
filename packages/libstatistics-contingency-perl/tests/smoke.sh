#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Statistics-Contingency
rpm -q --whatprovides 'perl(Statistics::Contingency)'
perl -MStatistics::Contingency -e '
  die "unexpected Statistics::Contingency version\n"
    unless $Statistics::Contingency::VERSION eq "0.09";
  my $table = Statistics::Contingency->new(categories => [qw(sports finance)]);
  $table->set_entries(2, 3, 5, 19);
  die "precision mismatch\n"
    unless abs($table->micro_precision - 2/5) < 1e-12;
  die "recall mismatch\n"
    unless abs($table->micro_recall - 2/7) < 1e-12;
  die "accuracy mismatch\n"
    unless abs($table->micro_accuracy - 21/29) < 1e-12;
'
