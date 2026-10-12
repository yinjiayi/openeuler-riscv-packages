#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Random-Free
rpm -q --whatprovides 'perl(Math::Random::Free)'
perl -MMath::Random::Free=random_set_seed_from_phrase,random_uniform_integer,random_permutation -e '
  die "unexpected version\n" unless $Math::Random::Free::VERSION eq "0.2.0";
  random_set_seed_from_phrase("rva23-smoke");
  my @first = random_uniform_integer(4, 1, 6);
  random_set_seed_from_phrase("rva23-smoke");
  my @again = random_uniform_integer(4, 1, 6);
  die "seeded sequence changed\n" unless join(",", @first) eq join(",", @again);
  die "out-of-range value\n" unless @first == 4 && !grep { $_ < 1 || $_ > 6 } @first;
  my @permutation = random_permutation(0..4);
  die "invalid permutation\n" unless join(",", sort @permutation) eq "0,1,2,3,4";
'
