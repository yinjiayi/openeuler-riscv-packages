#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-AsObject
rpm -q --whatprovides 'perl(Hash::AsObject)'
perl -MHash::AsObject -e '
  die "unexpected version\n" unless $Hash::AsObject::VERSION eq "0.13";
  my $hash = Hash::AsObject->new({foo => 123});
  die "accessor failed\n" unless $hash->foo == 123;
  $hash->bar(456);
  die "mutator failed\n" unless $hash->bar == 456 && $hash->{bar} == 456;
'
