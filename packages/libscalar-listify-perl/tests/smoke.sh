#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libscalar-listify-perl
perl -MScalar::Listify -e '
  use strict;
  use warnings;
  my @plain = listify(0);
  die "zero scalar lost" unless @plain == 1 && defined $plain[0] && $plain[0] == 0;
  my @empty = listify([]);
  die "empty list became a value" if @empty;
  my $items = ["a b", 0, undef];
  my $copy = listify_aref($items);
  die "order/value not preserved"
      unless @$copy == 3 && $copy->[0] eq "a b" && $copy->[1] == 0 && !defined $copy->[2];
  $copy->[0] = "changed";
  die "input mutated" unless $items->[0] eq "a b";
  print "installed Scalar::Listify preserves zero, empty lists and array order\n";
'
