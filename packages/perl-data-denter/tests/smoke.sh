#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Data-Denter
perl -MData::Denter -e '
  die "unexpected version\n" unless $Data::Denter::VERSION eq "0.15";
  my $encoded = Data::Denter::Indent({ name => "value" });
  my $decoded = Data::Denter::Undent($encoded);
  die "round-trip failed\n" unless ref($decoded) eq "HASH" && $decoded->{name} eq "value";
'
