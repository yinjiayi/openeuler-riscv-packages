#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Truncate
rpm -q --whatprovides 'perl(String::Truncate)'
perl -MString::Truncate=elide,trunc -e '
  die "unexpected String::Truncate version\n"
    unless $String::Truncate::VERSION eq "1.100603";
  die "right elision mismatch\n"
    unless elide("this is your brain", 16) eq "this is your ...";
  die "plain truncation mismatch\n"
    unless trunc("this is your brain", 16) eq "this is your bra";
  die "ends elision mismatch\n"
    unless elide("this is your brain", 16, { truncate => "ends" })
      eq "... is your b...";
'
