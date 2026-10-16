#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Fibonacci
rpm -q --whatprovides 'perl(Math::Fibonacci)'
perl -MMath::Fibonacci=term,series,decompose,isfibonacci -e '
  die "unexpected version\n" unless $Math::Fibonacci::VERSION eq "1.5";
  die "term mismatch\n" unless term(10) == 55;
  die "series mismatch\n" unless join(q{,}, series(7)) eq "1,1,2,3,5,8,13";
  die "decomposition mismatch\n" unless join(q{,}, decompose(100)) eq "89,8,3";
  die "membership mismatch\n" unless isfibonacci(55) == 10;
'
