#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Trim-More
rpm -q --whatprovides 'perl(String::Trim::More)'
perl -MString::Trim::More=trim,trim_lines,ellipsis -e '
  die "unexpected String::Trim::More version\n"
    unless $String::Trim::More::VERSION eq "0.03";
  die "trim result mismatch\n" unless trim("  hello  ") eq "hello";
  die "per-line trim mismatch\n"
    unless trim_lines(" a \n b \n") eq "a\nb\n";
  die "ellipsis mismatch\n"
    unless ellipsis("12345678901", 10) eq "1234567...";
'
