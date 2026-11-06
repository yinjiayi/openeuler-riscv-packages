#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-VecStat
rpm -q --whatprovides 'perl(Math::VecStat)'
perl -MMath::VecStat=min,max,sum,average,median,vecprod -e '
  die "unexpected version\n" unless $Math::VecStat::VERSION eq "0.08";
  die "minimum mismatch\n" unless scalar(min(3, 1, 2)) == 1;
  die "maximum mismatch\n" unless scalar(max(3, 1, 2)) == 3;
  die "sum mismatch\n" unless scalar(sum(3, 1, 2)) == 6;
  die "average mismatch\n" unless average(3, 1, 2) == 2;
  die "median mismatch\n" unless median(3, 1, 2)->[0] == 2;
  die "vector product mismatch\n" unless join(q{,}, @{vecprod(2, [3, 1, 2])}) eq "6,2,4";
'
