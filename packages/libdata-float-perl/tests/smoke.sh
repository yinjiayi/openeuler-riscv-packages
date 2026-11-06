#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Data-Float
rpm -q --whatprovides 'perl(Data::Float)'
perl -MData::Float=float_class,float_is_finite,signbit -e '
  die "unexpected Data::Float version\n" unless $Data::Float::VERSION eq "0.015";
  die "normal float classification mismatch\n" unless float_class(1.5) eq "NORMAL";
  die "finite float predicate mismatch\n" unless float_is_finite(1.5);
  die "positive sign mismatch\n" if signbit(1.5);
'
