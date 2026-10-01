#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-C3
perl -MAlgorithm::C3 -e '
  die "unexpected Algorithm::C3 version\n"
    unless $Algorithm::C3::VERSION eq "0.11";
  my %parents = (
    A => [qw(B C)],
    B => ["D"],
    C => ["D"],
    D => [],
  );
  my @order = Algorithm::C3::merge("A", sub {
    return @{$parents{$_[0]}};
  });
  die "C3 merge order mismatch\n"
    unless join(",", @order) eq "A,B,C,D";
'
