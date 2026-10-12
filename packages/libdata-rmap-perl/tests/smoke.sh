#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Rmap
rpm -q --whatprovides 'perl(Data::Rmap)'
perl -MData::Rmap=rmap -e '
  die "unexpected Data::Rmap version\n" unless $Data::Rmap::VERSION eq "0.65";
  my $values = ["a", ["b"]];
  rmap { $_ = uc($_) } $values;
  die "recursive map mismatch\n"
    unless $values->[0] eq "A" && $values->[1][0] eq "B";
'
