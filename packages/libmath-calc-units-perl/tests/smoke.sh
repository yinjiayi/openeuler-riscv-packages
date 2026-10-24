#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Calc-Units
rpm -q --whatprovides 'perl(Math::Calc::Units)'
rpm -qf -- /usr/bin/ucalc
perl -MMath::Calc::Units=equal,convert -e '
  die "unexpected version\n" unless $Math::Calc::Units::VERSION eq "1.07";
  die "unit equality failed\n" unless equal("60 sec", "1 min");
  die "unit conversion failed\n" unless convert("60 sec", "min") eq "1 min";
'
test "$(ucalc -c '60 sec' 'min')" = '1 min'
