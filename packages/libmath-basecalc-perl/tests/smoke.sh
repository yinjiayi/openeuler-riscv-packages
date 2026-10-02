#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-BaseCalc
rpm -q --whatprovides 'perl(Math::BaseCalc)'
perl -MMath::BaseCalc -e '
  die "unexpected Math::BaseCalc version\n" unless $Math::BaseCalc::VERSION eq "1.019";
  my $calc = Math::BaseCalc->new(digits => "hex");
  die "hex encoding mismatch\n" unless $calc->to_base(255) eq "ff";
  die "hex decoding mismatch\n" unless $calc->from_base("ff") == 255;
  $calc->digits("bin");
  die "binary encoding mismatch\n" unless $calc->to_base(5) eq "101";
  die "binary decoding mismatch\n" unless $calc->from_base("101") == 5;
'
