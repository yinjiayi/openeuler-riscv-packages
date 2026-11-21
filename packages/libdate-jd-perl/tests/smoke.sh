#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdate-jd-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Date::JD qw(jd_to_mjd mjd_to_jd);
use Math::BigRat 0.13;

my $jd = Math::BigRat->new('2451545');
my $mjd = jd_to_mjd($jd);
die "wrong scalar conversion" unless jd_to_mjd(2451545) == 51544.5;
die "wrong exact rational conversion" unless
    ref($mjd) eq 'Math::BigRat' &&
    $mjd == Math::BigRat->new('103089/2') &&
    mjd_to_jd($mjd) == $jd;
print "installed scalar and rational Julian-date roundtrip passed\n";
PERL
