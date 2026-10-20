#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Dirify
rpm -q --whatprovides 'perl(String::Dirify)'
perl -MString::Dirify -e '
  die "unexpected version\n" unless $String::Dirify::VERSION eq "1.03";
  my $dirifier = String::Dirify->new;
  die "default separator mismatch\n"
    unless $dirifier->dirify("A B C") eq "a_b_c";
  die "custom separator mismatch\n"
    unless $dirifier->dirify("A B C", "-") eq "a-b-c";
  die "HTML conversion mismatch\n"
    unless $dirifier->dirify("<b>Hello</b> World") eq "hello_world";
'
