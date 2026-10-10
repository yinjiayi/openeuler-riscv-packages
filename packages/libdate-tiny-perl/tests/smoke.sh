#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Date-Tiny
rpm -q --whatprovides 'perl(Date::Tiny)'
perl -MDate::Tiny -e '
  die "wrong installed version\n" unless $Date::Tiny::VERSION eq "1.07";
  my $date = Date::Tiny->new(year => 2006, month => 1, day => 31);
  die "string conversion changed\n" unless "$date" eq "2006-01-31";
  my $roundtrip = Date::Tiny->from_string($date->as_string);
  die "roundtrip year changed\n" unless $roundtrip->year == 2006;
  die "roundtrip month changed\n" unless $roundtrip->month == 1;
  die "roundtrip day changed\n" unless $roundtrip->day == 31;
'
