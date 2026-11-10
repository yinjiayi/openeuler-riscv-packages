#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdate-simple-perl
perl -MDate::Simple -e '
    die "Date::Simple loaded its fallback" if exists $INC{"Date/Simple/NoXS.pm"};
    my $date = Date::Simple->new("2024-02-29");
    die "unexpected leap-day parse" unless $date && "$date" eq "2024-02-29";
    die "unexpected Gregorian rollover" unless "".($date+1) eq "2024-03-01";
    print "installed native XS leap-day rollover passed\n";
'
