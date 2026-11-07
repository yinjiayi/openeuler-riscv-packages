#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-lingua-en-syllable
perl <<'PERL'
use strict;
use warnings;
use Lingua::EN::Syllable qw(syllable);
die "version mismatch\n" unless $Lingua::EN::Syllable::VERSION eq '0.31';
my %cases = (organism => 4, microorganisms => 6, executed => 4, accused => 2, w => 2, cwm => 1);
for my $word (sort keys %cases) {
    die "syllable mismatch for $word\n" unless syllable($word) == $cases{$word};
}
print "Lingua::EN::Syllable heuristic smoke passed\n";
PERL
