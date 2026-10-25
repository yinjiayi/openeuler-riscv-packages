#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Time-Period
rpm -q --whatprovides 'perl(Time::Period)'
perl -MTime::Period -MPOSIX -e '
  die "wrong installed version\n" unless $Time::Period::VERSION eq "1.25";
  my $saturday = POSIX::mktime(0, 0, 0, 1, 0, 111);
  die "weekday match failed\n" unless inPeriod($saturday, "wd {sa}") == 1;
  die "weekday exclusion failed\n" unless inPeriod($saturday + 86400, "wd {sa}") == 0;
  die "year match failed\n" unless inPeriod($saturday, "yr {2011}") == 1;
  die "invalid period accepted\n" unless inPeriod($saturday, "wd {") == -1;
'
