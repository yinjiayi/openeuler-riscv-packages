#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Test-Bits
rpm -q --whatprovides 'perl(Test::Bits)'
perl -MTest::Bits -MTest::More -e '
  die "unexpected version\n" unless $Test::Bits::VERSION eq "0.02";
  bits_is("AZ", [65, 90], "ASCII byte comparison");
  done_testing();
'
