#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Record
rpm -q --whatprovides 'perl(Data::Record)'
perl -e '
  use Data::Record;
  die "unexpected Data::Record version\n"
    unless $Data::Record::VERSION eq "0.02";
  my @records = Data::Record->new({ split => "," })->records("a,b");
  die "record splitting mismatch\n"
    unless @records == 2 && $records[0] eq "a" && $records[1] eq "b";
'
