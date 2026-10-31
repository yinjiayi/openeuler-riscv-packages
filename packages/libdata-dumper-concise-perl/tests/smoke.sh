#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Dumper-Concise
rpm -q --whatprovides 'perl(Data::Dumper::Concise)'
rpm -q --whatprovides 'perl(Devel::Dwarn)'
perl -MData::Dumper::Concise -MDevel::ArgNames -e '
  die "unexpected version\n" unless $Data::Dumper::Concise::VERSION eq "2.023";
  my $s = Dumper({ sample => 1 });
  die "dump missing key\n" unless index($s, "sample") >= 0;
'
