#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-String-Koremutake
rpm -q --whatprovides 'perl(String::Koremutake)'
perl -MString::Koremutake -e '
  die "unexpected version\n" unless $String::Koremutake::VERSION eq "0.30";
  my $k = String::Koremutake->new;
  for my $n (0, 39, 128, 65535, 10610353957) {
    my $encoded = $k->integer_to_koremutake($n);
    die "round-trip mismatch for $n\n"
      unless $k->koremutake_to_integer($encoded) == $n;
  }
  my $accepted = eval { $k->koremutake_to_integer("Hello world"); 1 };
  die "invalid Koremutake input was accepted\n" if $accepted;
  die "unexpected invalid-input failure: $@\n"
    unless $@ =~ /Phoneme .* not valid/;
'
