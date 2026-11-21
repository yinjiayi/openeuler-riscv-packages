#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdate-holidays-de-perl
unset PERL5LIB PERLLIB PERL5OPT
export TZ=UTC LC_ALL=C
/usr/bin/perl -MDate::Holidays::DE - <<'PERL'
use strict;
use warnings;

sub dates {
    my ($year, $state) = @_;
    return { map { $_ => 1 } @{Date::Holidays::DE::holidays(
        YEAR => $year, WHERE => [$state], FORMAT => '%Y-%m-%d'
    )} };
}

die "expected Berlin 2025 date absent" unless dates(2025, 'be')->{'2025-05-08'};
die "unexpected Berlin 2024 date" if dates(2024, 'be')->{'2024-05-08'};
die "unexpected Hessen 2025 date" if dates(2025, 'he')->{'2025-05-08'};
print "installed Berlin date/state guards passed\n";
PERL
