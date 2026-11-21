#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtie-cycle-sinewave-perl
perl -MTie::Cycle::Sinewave <<'PERL'
use strict;
use warnings;
my ($maxima, $minima) = (0, 0);
tie my $cycle, 'Tie::Cycle::Sinewave',
    min => 0, max => 8, period => 4,
    at_max => sub { ++$maxima }, at_min => sub { ++$minima };
my @expected = (4, 8, 4, 0, 4);
my @samples = map { my $v = $cycle; $v } @expected;
for my $i (0 .. $#expected) {
    die "unexpected cycle sample $i" if abs($samples[$i] - $expected[$i]) > 1e-9;
}
die "wrong extrema callbacks" unless $maxima == 1 && $minima == 1;
print "ok 1 - installed tied scalar cycles and fires both extrema callbacks\n";
PERL
