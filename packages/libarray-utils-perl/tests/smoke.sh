#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Array-Utils
rpm -q --whatprovides 'perl(Array::Utils)'
perl -MArray::Utils=unique,intersect,array_minus -e '
  die "unexpected version\n" unless $Array::Utils::VERSION eq "0.5";
  my @union = sort(unique(qw(a b a c)));
  die "unique mismatch\n" unless join(",", @union) eq "a,b,c";
  my @a = qw(a b c);
  my @b = qw(b c d);
  die "intersection mismatch\n" unless join(",", intersect(@a, @b)) eq "b,c";
  die "minus mismatch\n" unless join(",", array_minus(@a, @b)) eq "a";
'
