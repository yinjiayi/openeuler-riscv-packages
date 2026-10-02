#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-BaseCnv
rpm -q --whatprovides 'perl(Math::BaseCnv)'
rpm -qf -- /usr/bin/cnv
perl -MMath::BaseCnv=cnv -e '
  die "unexpected module version\n" unless $Math::BaseCnv::VERSION eq "1.14";
  die "unexpected conversion\n" unless cnv(127, 10, 16) eq "7F";
'
test "$(/usr/bin/cnv 127 10 16)" = 7F
