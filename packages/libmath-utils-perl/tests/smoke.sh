#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Utils
rpm -q --whatprovides 'perl(Math::Utils)'
perl -MMath::Utils=gcd,lcm,sign,log2 -e '
  die "unexpected Math::Utils version\n" unless $Math::Utils::VERSION eq "1.14";
  die "gcd mismatch\n" unless gcd(12, 18) == 6;
  die "lcm mismatch\n" unless lcm(12, 18) == 36;
  die "sign mismatch\n" unless sign(-3) == -1;
  die "log2 mismatch\n" unless log2(8) == 3;
'
