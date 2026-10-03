#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-MockTime
rpm -q --whatprovides 'perl(Test::MockTime)'
perl -MTest::MockTime=set_fixed_time,restore_time -e '
  die "unexpected version\n" unless $Test::MockTime::VERSION eq "0.17";
  set_fixed_time(1234567890);
  die "fixed time mismatch\n" unless time() == 1234567890;
  restore_time();
  die "time did not restore\n" if time() == 1234567890;
'
