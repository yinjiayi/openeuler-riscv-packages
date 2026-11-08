#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Trim
rpm -q --whatprovides 'perl(String::Trim)'
perl -MString::Trim -e '
  die "unexpected String::Trim version\n"
    unless $String::Trim::VERSION eq "0.005";
  my $value = "  hello  ";
  die "trim result mismatch\n" unless trim($value) eq "hello";
  my @values = (" a ", " b ");
  my $trimmed = trim(\@values);
  die "array trim result mismatch\n"
    unless join(",", @$trimmed) eq "a,b";
'
