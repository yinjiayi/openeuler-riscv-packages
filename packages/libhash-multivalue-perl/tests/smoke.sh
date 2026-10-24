#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Hash-MultiValue
rpm -q --whatprovides 'perl(Hash::MultiValue)'
perl -MHash::MultiValue -e '
  die "unexpected version\n" unless $Hash::MultiValue::VERSION eq "0.16";
  my $values = Hash::MultiValue->new(foo => "first", foo => "second");
  my @all = $values->get_all("foo");
  die "multi-value lookup failed\n" unless join(",", @all) eq "first,second";
  die "hash-style lookup failed\n" unless $values->{foo} eq "second";
  $values->add(foo => "third");
  die "add failed\n" unless $values->{foo} eq "third";
'
