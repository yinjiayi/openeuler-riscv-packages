#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Miscellany
rpm -q --whatprovides 'perl(Data::Miscellany)'
perl -MData::Miscellany=set_push,trim,is_deeply -e '
  die "unexpected Data::Miscellany version\n"
    unless $Data::Miscellany::VERSION eq "1.100850";
  my @values = (1, 2);
  set_push @values, 2, 3;
  die "set_push mismatch\n" unless is_deeply(\@values, [1, 2, 3]);
  die "trim mismatch\n" unless trim("  value  ") eq "value";
'
