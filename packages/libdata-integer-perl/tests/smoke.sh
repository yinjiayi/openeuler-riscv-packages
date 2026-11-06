#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Integer
rpm -q --whatprovides 'perl(Data::Integer)'
perl -e '
  use Data::Integer qw(natint_bits nint_add);
  die "unexpected Data::Integer version\n"
    unless $Data::Integer::VERSION eq "0.007";
  die "native integer width too small\n" unless natint_bits() >= 32;
  die "integer arithmetic mismatch\n" unless nint_add(2, 3) == 5;
'
