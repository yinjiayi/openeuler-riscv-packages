#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-GUID
rpm -q --whatprovides 'perl(Data::GUID)'
perl -MData::GUID -e '
  die "unexpected Data::GUID version\n"
    unless $Data::GUID::VERSION eq "0.051";
  my $guid = Data::GUID->new;
  my $string = $guid->as_string;
  die "invalid GUID string\n"
    unless $string =~ Data::GUID->string_guid_regex;
  my $copy = Data::GUID->from_string($string);
  die "GUID round-trip mismatch\n"
    unless $copy->as_string eq $string;
'
