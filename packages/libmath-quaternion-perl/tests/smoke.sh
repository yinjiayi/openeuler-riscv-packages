#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Math-Quaternion
rpm -q --whatprovides 'perl(Math::Quaternion)'
perl -MMath::Quaternion -e '
  die "unexpected version\n" unless $Math::Quaternion::VERSION eq "0.07";
  my $q = Math::Quaternion->new(1, 2, 3, 4);
  my $identity = Math::Quaternion->new(1, 0, 0, 0);
  my $product = $q * $identity;
  die "identity multiplication failed\n" unless join(",", @$product) eq "1,2,3,4";
'
