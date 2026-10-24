#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Trigger
rpm -q --whatprovides 'perl(Class::Trigger)'
perl -MClass::Trigger -e '
  die "wrong installed version\n" unless $Class::Trigger::VERSION eq "0.15";
  { package OEEvent; use Class::Trigger qw(fire); sub new { bless {}, shift } }
  my $count = 0;
  OEEvent->add_trigger(fire => sub { $count += $_[1] });
  my $event = OEEvent->new;
  $event->call_trigger("fire", 3);
  die "installed trigger dispatch failed\n" unless $count == 3;
'
