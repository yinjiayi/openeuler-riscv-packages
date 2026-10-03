#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Devel-OverloadInfo
rpm -q --whatprovides 'perl(Devel::OverloadInfo)'
perl -MDevel::OverloadInfo=is_overloaded,overload_op_info -MScalar::Util=refaddr -MSub::Util -e '
  die "wrong installed version\n" unless $Devel::OverloadInfo::VERSION eq "0.008";
  die "Sub::Util branch inactive\n" unless refaddr(\&Devel::OverloadInfo::subname) == refaddr(\&Sub::Util::subname);
  package Local::Overloaded;
  use overload q{""} => sub { q{overloaded} };
  package main;
  die "overload not detected\n" unless is_overloaded(q{Local::Overloaded});
  my $info = overload_op_info(q{Local::Overloaded}, q{""});
  die "wrong declaring class\n" unless $info->{class} eq q{Local::Overloaded};
  print "installed overload introspection and Sub::Util branch OK\n";
'
