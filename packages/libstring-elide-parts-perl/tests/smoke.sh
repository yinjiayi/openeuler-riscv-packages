#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Elide-Parts
rpm -q --whatprovides 'perl(String::Elide::Parts)'
perl -MString::Elide::Parts=elide -e '
  die "unexpected String::Elide::Parts version\n"
    unless $String::Elide::Parts::VERSION eq "0.07";
  die "right elision mismatch\n"
    unless elide("1234567890", 5) eq "123..";
  die "middle elision mismatch\n"
    unless elide("1234567890", 6, { truncate => "middle" }) eq "12..90";
  die "marker elision mismatch\n"
    unless elide("1234567890", 5, { marker => "---" }) eq "12---";
'
