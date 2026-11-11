#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-number-misc
perl -MNumber::Misc=:all -e '
    die "version\n" unless $Number::Misc::VERSION eq "1.2";
    die "numeric\n" unless is_numeric("3.14") && !is_numeric("bad");
    die "conversion\n" unless to_number(" 3,000 ") == 3000;
    die "commas\n" unless commafie(2000) eq "2,000";
    die "padding\n" unless zero_pad(2, 3) eq "002";
    die "parity\n" unless is_even(2) && is_odd(3) && !is_even(3);
    my $value = rand_in_range(-1, 10);
    die "random range\n" unless $value >= -1 && $value <= 10;
    print "Number::Misc installed smoke passed\n";
'
