#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
perl -MTime::Progress -e '
  my $progress = Time::Progress->new(min => 0, max => 10);
  die "incorrect percentage\n" unless $progress->report("%p", 5) eq " 50.0%";
  die "incorrect meter\n" unless $progress->report("%10b", 5) eq "#####.....";
  print "ok - staged progress reports exact half completion\n";
'
