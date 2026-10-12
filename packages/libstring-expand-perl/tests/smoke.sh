#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Expand
rpm -q --whatprovides 'perl(String::Expand)'
perl -MString::Expand=expand_string,expand_strings -e '
  die "unexpected String::Expand version\n"
    unless $String::Expand::VERSION eq "0.04";
  die "single string expansion mismatch\n"
    unless expand_string("hello \$WHO", { WHO => "RISC-V" }) eq "hello RISC-V";
  my %values = ( NAME => "RISC-V", MESSAGE => "hello \$NAME" );
  expand_strings(\%values, {});
  die "chained expansion mismatch\n"
    unless $values{MESSAGE} eq "hello RISC-V";
  my $error = eval { expand_string("\$MISSING", {}); 1 };
  die "missing variable did not fail\n" if $error;
'
