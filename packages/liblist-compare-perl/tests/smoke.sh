#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-List-Compare
rpm -q --whatprovides 'perl(List::Compare)'
perl -MList::Compare -MList::Compare::Functional=get_intersection -e '
  die "unexpected version\n" unless $List::Compare::VERSION eq "0.55";
  my $compare = List::Compare->new([qw(a b)], [qw(b c)]);
  my @intersection = $compare->get_intersection;
  my @union = $compare->get_union;
  my @functional = get_intersection([[qw(a b)], [qw(b c)]]);
  die "object intersection failed\n" unless join(",", @intersection) eq "b";
  die "union failed\n" unless join(",", @union) eq "a,b,c";
  die "functional intersection failed\n" unless join(",", @functional) eq "b";
'
