#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Time-Piece-MySQL
rpm -q --whatprovides 'perl(Time::Piece::MySQL)'
perl -MTime::Piece::MySQL -e '
  die "wrong installed version\n" unless $Time::Piece::MySQL::VERSION eq "0.06";
  my $date = Time::Piece->from_mysql_date("2012-02-11");
  die "date round trip failed\n" unless $date->mysql_date eq "2012-02-11";
  my $datetime = Time::Piece->from_mysql_datetime("2012-02-11 05:45:37");
  die "datetime round trip failed\n" unless $datetime->mysql_datetime eq "2012-02-11 05:45:37";
  my $stamp = Time::Piece->from_mysql_timestamp("120211054537");
  die "timestamp round trip failed\n" unless $stamp->mysql_timestamp eq "20120211054537";
  print "installed MySQL date/time conversions OK\n";
'
