#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Hexdumper
rpm -q --whatprovides 'perl(Data::Hexdumper)'
perl -MData::Hexdumper=hexdump -e '
  die "wrong installed version\n" unless $Data::Hexdumper::VERSION eq "3.0001";
  my $dump = hexdump(data => "AB", output_format => "%C %d");
  die "installed hexdump output mismatch\n" unless $dump eq "41 A\n42 B\n";
'
