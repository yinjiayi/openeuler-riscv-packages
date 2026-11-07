#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-lingua-en-numbers-ordinate
perl <<'PERL'
use strict;
use warnings;
use Lingua::EN::Numbers::Ordinate qw(ordinate th ordsuf);
die "version" unless $Lingua::EN::Numbers::Ordinate::VERSION eq '1.05';
for my $case ([1,'1st'], [2,'2nd'], [3,'3rd'], [11,'11th'], [12,'12th'], [13,'13th'], [23,'23rd'], [-342,'-342nd'], [0,'0th']) {
    die "ordinal for $case->[0]" unless ordinate($case->[0]) eq $case->[1];
    die "alias for $case->[0]" unless th($case->[0]) eq $case->[1];
}
die "suffix" unless ordsuf(112) eq 'th' && ordsuf(123) eq 'rd';
die "undefined boundary" unless ordinate(undef) eq '0th' && ordinate('') eq '0th';
print "Lingua::EN::Numbers::Ordinate installed API checks passed\n";
PERL
