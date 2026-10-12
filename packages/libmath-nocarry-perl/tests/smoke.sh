#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-NoCarry
rpm -q --whatprovides 'perl(Math::NoCarry)'
perl -MMath::NoCarry=add,subtract,multiply -e '
  die "unexpected Math::NoCarry version\n" unless $Math::NoCarry::VERSION eq "1.117";
  my ($a, $b, $c, $d, $e, $f) = (1234, 5678, 12, 8, 2, 6);
  die "add mismatch\n" unless add($a, $b) == 6802;
  die "subtract mismatch\n" unless subtract($c, $d) == 14;
  die "multiply mismatch\n" unless multiply($e, $f) == 2;
'
