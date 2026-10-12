#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Time-Duration
rpm -q --whatprovides 'perl(Time::Duration)'
perl -MTime::Duration=duration,duration_exact,ago -e '
  die "wrong installed version\n" unless $Time::Duration::VERSION eq "1.21";
  die "rounded duration changed\n" unless duration(3661) eq "1 hour and 1 minute";
  die "exact duration changed\n" unless duration_exact(3661) eq "1 hour, 1 minute, and 1 second";
  die "relative duration changed\n" unless ago(3600) eq "1 hour ago";
  print "installed rounded, exact and relative duration output OK\n";
'
