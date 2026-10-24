#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-Case
rpm -q --whatprovides 'perl(Hash::Case)'
perl -MHash::Case::Lower -MHash::Case::Upper -MHash::Case::Preserve -e '
  die "unexpected version\n" unless $Hash::Case::VERSION eq "1.07";
  tie my %lower, "Hash::Case::Lower";
  $lower{MiXeD} = 3;
  die "lower-case lookup failed\n" unless $lower{mixed} == 3;
  tie my %upper, "Hash::Case::Upper";
  $upper{MiXeD} = 4;
  die "upper-case lookup failed\n" unless $upper{MIXED} == 4;
  tie my %preserve, "Hash::Case::Preserve";
  $preserve{MiXeD} = 5;
  die "preserved-case lookup failed\n" unless $preserve{mixed} == 5;
  die "original case lost\n" unless (keys %preserve)[0] eq "MiXeD";
'
