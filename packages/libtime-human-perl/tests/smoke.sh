#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-time-human
perl <<'PERL'
use strict;
use warnings;
use Time::Human;
die "wrong release" unless $Time::Human::VERSION eq '1.03';
for my $case ([0,0,'exactly midnight'], [0,12,'exactly midday'], [30,18,'exactly half past six in the evening']) {
    my ($minutes, $hour, $expected) = @$case;
    my $got = humanize(0, $minutes, $hour);
    $got =~ s/\s+\z//;
    die "unexpected fixed-time rendering" unless $got eq $expected;
}
print "staged Time::Human fixed-time rendering passed\n";
PERL
