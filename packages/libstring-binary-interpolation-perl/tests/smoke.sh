#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Binary-Interpolation
rpm -q --whatprovides 'perl(String::Binary::Interpolation)'
perl -MString::Binary::Interpolation -e '
  die "unexpected version\n"
    unless $String::Binary::Interpolation::VERSION eq "1.0.1";
  my $bytes = "${b00000000}${b01000100}${b11111111}";
  die "byte boundaries mismatch\n" unless unpack("H*", $bytes) eq "0044ff";
'
