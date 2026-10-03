#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Measure
rpm -q --whatprovides 'perl(Class::Measure)'
rpm -q --whatprovides 'perl(Class::Measure::Length)'
perl -MClass::Measure::Length=length -e '
  die "wrong installed version\n" unless $Class::Measure::Length::VERSION eq "0.10";
  my $inches = length(12, "inches");
  die "foot conversion failed\n" unless $inches->feet == 1;
  my $yards = $inches * 3;
  die "yard conversion failed\n" unless $yards->yards == 1;
  die "source object was modified\n" unless $inches->inches == 12;
'
