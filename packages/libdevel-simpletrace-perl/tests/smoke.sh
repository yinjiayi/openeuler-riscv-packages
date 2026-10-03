#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Devel-SimpleTrace
rpm -q --whatprovides 'perl(Devel::SimpleTrace)'
perl -MDevel::SimpleTrace -e '
  die "wrong installed version\n" unless $Devel::SimpleTrace::VERSION eq "0.08";
  die "warning hook inactive\n" unless ref($SIG{"__WARN__"}) eq "CODE";
  die "exception hook inactive\n" unless ref($SIG{"__DIE__"}) eq "CODE";
  sub first { second() }
  sub second { die "simpletrace-probe\n" }
  eval { first() };
  die "missing trace marker\n" unless $@ =~ /simpletrace-probe/;
  die "missing nested caller\n" unless $@ =~ /main::second/ && $@ =~ /main::first/;
  print "installed exception stack trace OK\n";
'
