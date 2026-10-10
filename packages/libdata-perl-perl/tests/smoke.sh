#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Perl
rpm -q --whatprovides 'perl(Data::Perl::Collection::Array)'
perl -MData::Perl -e '
  die "unexpected Data::Perl version\n"
    unless $Data::Perl::VERSION eq "0.002011";
  my $string = string("foo");
  $string->append("bar");
  die "installed string wrapper failed\n" unless $$string eq "foobar";
  my $array = array(1, 2, 3);
  die "installed array wrapper failed\n" unless $array->count == 3;
  my $number = number(5);
  die "installed number wrapper failed\n" unless $number->add(7) == 12;
'
