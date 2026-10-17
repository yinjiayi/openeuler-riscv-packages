#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Number-Delta
rpm -q --whatprovides 'perl(Test::Number::Delta)'
perl -MTest::Number::Delta -e '
  die "unexpected Test::Number::Delta version\n"
    unless $Test::Number::Delta::VERSION eq "1.06";
  Test::Builder->new->plan(tests => 2);
  delta_within(1, 1.0001, 0.001, "installed absolute tolerance")
    or die "delta_within failed\n";
  delta_not_within(1, 1.1, 0.001, "installed inequality tolerance")
    or die "delta_not_within failed\n";
'
