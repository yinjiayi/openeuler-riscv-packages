#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Set-Infinite
rpm -q --whatprovides 'perl(Set::Infinite)'
module_file="$(perl -MSet::Infinite -e 'print $INC{"Set/Infinite.pm"}')"
test -n "$module_file"
rpm -qf -- "$module_file"

perl -MSet::Infinite -e '
  die "unexpected version\n" unless $Set::Infinite::VERSION eq "0.65";
  my $left = Set::Infinite->new(1, 3);
  my $right = Set::Infinite->new(3, 5);
  die "intersection boundary failed\n"
    unless "$left" eq "[1..3]"
      && "" . $left->intersection($right) eq "3";
  die "union failed\n"
    unless "" . $left->union($right) eq "[1..5]";
  my $open = Set::Infinite->new({a => 1, open_begin => 0, b => 3, open_end => 1});
  die "open interval failed\n"
    unless "$open" eq "[1..3)"
      && $open->intersection($right)->is_empty;
'
