#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Escape
rpm -q --whatprovides 'perl(String::Escape)'
perl -MString::Escape=backslash,unbackslash -e '
  die "unexpected String::Escape version\n"
    unless $String::Escape::VERSION eq "2010.002";
  my $input = "\tA\n";
  die "backslash encoding mismatch\n"
    unless backslash($input) eq "\\tA\\n";
  die "backslash decoding mismatch\n"
    unless unbackslash(backslash($input)) eq $input;
'
