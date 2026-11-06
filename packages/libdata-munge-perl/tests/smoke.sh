#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Munge
rpm -q --whatprovides 'perl(Data::Munge)'
perl -MData::Munge=trim,list2re -e '
  die "unexpected Data::Munge version\n" unless $Data::Munge::VERSION eq "0.111";
  die "trim mismatch\n" unless trim("  abc  ") eq "abc";
  my $pattern = list2re("ab", "a");
  die "alternation mismatch\n" unless "ab" =~ /^$pattern$/;
'
