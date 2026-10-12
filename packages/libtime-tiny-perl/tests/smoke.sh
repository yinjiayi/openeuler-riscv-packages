#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Time-Tiny
rpm -q --whatprovides 'perl(Time::Tiny)'
perl -MTime::Tiny -e '
  die "wrong installed version\n" unless $Time::Tiny::VERSION eq "1.08";
  my $time = Time::Tiny->new(hour => 1, minute => 2, second => 3);
  die "string conversion changed\n" unless "$time" eq "01:02:03";
  my $roundtrip = Time::Tiny->from_string($time->as_string);
  die "roundtrip hour changed\n" unless $roundtrip->hour == 1;
  die "roundtrip minute changed\n" unless $roundtrip->minute == 2;
  die "roundtrip second changed\n" unless $roundtrip->second == 3;
'
