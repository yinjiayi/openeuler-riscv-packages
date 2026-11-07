#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-number-range
perl <<'PERL'
use strict;
use warnings;
use Number::Range;
die 'version' unless $Number::Range::VERSION eq '0.12';
my $r = Number::Range->new('-10..10,20..30');
die 'inside' unless $r->inrange(-10) && $r->inrange(30);
die 'outside' if $r->inrange(15);
die 'scalar all-of' if scalar $r->inrange(0, 1000);
die 'scalar reversed' if scalar $r->inrange(1000, 0);
die 'scalar success' unless scalar $r->inrange(0, 25);
my @flags = $r->inrange(0, 15, 25);
die 'list mapping' unless join(',', @flags) eq '1,0,1';
$r->addrange('40..45');
$r->delrange('42..44');
die 'mutation' unless $r->inrange(40) && !$r->inrange(43);
my $large = Number::Range->new('0..99999999');
die 'large scalar' if scalar $large->inrange(1, 100000000);
die 'large size' unless $large->size == 100000000;
print "Number::Range smoke passed\n";
PERL
