#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Round
rpm -q --whatprovides 'perl(Math::Round)'
perl -MMath::Round=round,round_even,nearest -e '
  die "unexpected Math::Round version\n" unless $Math::Round::VERSION eq "0.08";
  die "round mismatch\n" unless round(2.5) == 3;
  die "even tie mismatch\n" unless round_even(2.5) == 2;
  die "nearest multiple mismatch\n" unless nearest(10, 26) == 30;
'
