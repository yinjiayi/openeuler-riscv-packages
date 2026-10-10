#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-HexDump
rpm -q --whatprovides 'perl(Data::HexDump)'
perl -MData::HexDump -e '
  die "unexpected Data::HexDump version\n"
    unless $Data::HexDump::VERSION eq "0.04";
  my $dump = HexDump("A0");
  die "function dump mismatch\n"
    unless $dump =~ /00000000\s+41 30/ && $dump =~ /A0/;
  my $obj = Data::HexDump->new;
  $obj->data("B1");
  my $object_dump = $obj->dump;
  die "object dump mismatch\n"
    unless $object_dump =~ /00000000\s+42 31/ && $object_dump =~ /B1/;
'
