#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Devel-FindPerl
rpm -q --whatprovides 'perl(Devel::FindPerl)'
perl -T -MDevel::FindPerl=find_perl_interpreter,perl_is_same -MScalar::Util=tainted -e '
  die "wrong installed version\n" unless $Devel::FindPerl::VERSION eq "0.016";
  my $path = find_perl_interpreter();
  die "interpreter not executable\n" unless -x $path;
  die "interpreter configuration differs\n" unless perl_is_same($path);
  die "tainted interpreter path\n" if tainted($path);
  print "installed taint-mode interpreter identity OK\n";
'
