#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Array-IntSpan
rpm -q --whatprovides 'perl(Array::IntSpan)'
perl -MArray::IntSpan -e '
  die "unexpected version\n" unless $Array::IntSpan::VERSION eq "2.004";
  my $span = Array::IntSpan->new([0, 9, "low"], [10, 19, "high"]);
  die "initial lookup failed\n" unless $span->lookup(12) eq "high";
  $span->set_range(10, 19, "new");
  die "updated lookup failed\n" unless $span->lookup(12) eq "new";
  die "Fields module missing\n" unless require Array::IntSpan::Fields;
  die "IP module missing\n" unless require Array::IntSpan::IP;
'
