#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Peek
rpm -q --whatprovides 'perl(Data::Peek)'
perl -MB -MData::Peek -e '
  die "wrong installed version\n" unless $Data::Peek::VERSION eq "0.54";
  die "installed DPeek is not XS\n"
    unless B::svref_2object(Data::Peek->can("DPeek"))->XSUB;
  my $peek = Data::Peek::DPeek("sample");
  die "installed XS peek failed\n"
    if $peek =~ /^Your perl did not/ || $peek !~ /sample/;
  my $display = Data::Peek::DDisplay("ab");
  die "installed XS display failed\n" unless $display =~ /ab/;
'
