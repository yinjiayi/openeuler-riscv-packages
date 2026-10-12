#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
perl -MAlgorithm::Permute -e '
  die "version mismatch\n" unless $Algorithm::Permute::VERSION eq "0.17";
  my $p = Algorithm::Permute->new([1, 2, 3]);
  my %seen;
  while (my @v = $p->next) { $seen{join(",", @v)}++; }
  die "permutations mismatch\n" unless keys(%seen) == 6 && !grep { $_ != 1 } values %seen;
  $p->reset;
  my $count = 0;
  while (my @v = $p->next) { $count++; }
  die "reset mismatch\n" unless $count == 6;
  my $q = Algorithm::Permute->new([1, 2, 3, 4], 2);
  $count = 0;
  while (my @v = $q->next) { die "subset length\n" unless @v == 2; $count++; }
  die "subset mismatch\n" unless $count == 12;
  print "Algorithm::Permute XS permutations and reset passed\n";
'
