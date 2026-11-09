#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
perl -MTime::Clock -e '
  my $clock = Time::Clock->new;
  $clock->parse("23:59:59.999999999");
  $clock->add(nanoseconds => 1);
  die "clock did not wrap at midnight\n" unless $clock->as_string eq "00:00:00";
  print "ok - midnight wraps at nanosecond precision\n";
'
