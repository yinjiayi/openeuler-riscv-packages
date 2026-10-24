#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-Ordered
rpm -q --whatprovides 'perl(Hash::Ordered)'
perl -MHash::Ordered -e '
  die "unexpected version\n" unless $Hash::Ordered::VERSION eq "0.014";
  my $ordered = Hash::Ordered->new(a => 1, b => 2);
  die "initial order failed\n" unless join(",", $ordered->keys) eq "a,b";
  $ordered->set(a => 3);
  die "update failed\n" unless $ordered->get("a") == 3;
  $ordered->set(c => 4);
  die "append order failed\n" unless join(",", $ordered->keys) eq "a,b,c";
'
