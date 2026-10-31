#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Date-Leapyear
rpm -q --whatprovides 'perl(Date::Leapyear)'
perl -MDate::Leapyear -e '
  die "wrong installed version\n" unless $Date::Leapyear::VERSION eq "1.72";
  for my $case ([1900, 0], [2000, 1], [2004, 1], [2100, 0], [2400, 1]) {
    die "wrong leap result for $case->[0]\n"
      unless isleap($case->[0]) == $case->[1];
  }
'
