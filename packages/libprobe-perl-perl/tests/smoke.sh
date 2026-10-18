#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Probe-Perl
perl -MProbe::Perl -MConfig -e '
  die "unexpected Probe::Perl version\n"
    unless $Probe::Perl::VERSION eq "0.03";
  my $probe = Probe::Perl->new;
  die "Perl configuration mismatch\n"
    unless $probe->config("version") eq $Config{version};
  my $exe = $probe->find_perl_interpreter;
  die "Perl interpreter unavailable\n" unless defined($exe) && -x $exe;
  die "Perl identity mismatch\n" unless $probe->perl_is_same($exe);
'
