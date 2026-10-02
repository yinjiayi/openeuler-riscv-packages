#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Sorting
rpm -q --whatprovides 'perl(Data::Sorting)'
perl -MData::Sorting=sorted_array -e '
  die "unexpected Data::Sorting version\n"
    unless $Data::Sorting::VERSION eq "0.9";
  my @numbers = (10, 2, 1);
  my @sorted = sorted_array(@numbers, -compare => "numeric");
  die "numeric multi-key sorting failed\n"
    unless join(",", @sorted) eq "1,2,10";
'
