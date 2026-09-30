#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Parity
rpm -q --whatprovides 'perl(String::Parity)'
perl -MString::Parity -e '
  die "unexpected String::Parity version\n"
    unless $String::Parity::VERSION eq "1.34";
  my $even = setEvenParity("\x31");
  my $odd = setOddParity("\x31");
  die "even parity mismatch\n"
    unless unpack("H*", $even) eq "b1" && isEvenParity($even);
  die "odd parity mismatch\n"
    unless unpack("H*", $odd) eq "31" && isOddParity($odd);
'
