#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Pond
rpm -q --whatprovides 'perl(Data::Pond)'
perl -MB -MData::Pond=pond_read_datum,pond_write_datum -e '
  die "wrong installed version\n" unless $Data::Pond::VERSION eq "0.006";
  die "installed XS backend did not load\n"
    unless B::svref_2object(\&pond_read_datum)->XSUB;
  my $datum = pond_read_datum(q({answer=>[42,"ok"]}));
  die "installed parser failed\n"
    unless $datum->{answer}[0] eq "42" && $datum->{answer}[1] eq "ok";
  die "installed writer failed\n"
    unless pond_read_datum(pond_write_datum($datum))->{answer}[1] eq "ok";
'
