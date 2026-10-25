#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-WithDefaults
rpm -q --whatprovides 'perl(Hash::WithDefaults)'
perl -MHash::WithDefaults -e '
  die "unexpected version\n" unless $Hash::WithDefaults::VERSION eq "0.05";
  tie my %case, "Hash::WithDefaults", "lower", [Name => "value"];
  die "case lookup failed\n" unless $case{nAmE} eq "value";
  tie my %values, "Hash::WithDefaults", "sensitive", [explicit => "own"];
  my %fallback = (inherited => "first");
  tied(%values)->AddDefault(\%fallback);
  die "default lookup failed\n" unless $values{inherited} eq "first";
  $fallback{inherited} = "updated";
  die "mutable default not visible\n" unless $values{inherited} eq "updated";
  delete $values{explicit};
  die "delete retained explicit key\n" if exists $values{explicit};
'
