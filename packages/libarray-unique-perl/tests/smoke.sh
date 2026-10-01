#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Array-Unique
perl -MArray::Unique -e '
  die "unexpected version\n" unless $Array::Unique::VERSION eq "0.09";
  tie my @values, "Array::Unique";
  push @values, qw(alpha beta alpha gamma beta);
  die "unique array mismatch\n"
    unless join(",", @values) eq "alpha,beta,gamma";
  die "variant module missing\n"
    unless require Array::Unique::Std;
'
