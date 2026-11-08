#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtime-fake-perl
unset PERL5LIB PERLLIB PERL5OPT
/usr/bin/perl - <<'PERL'
use strict;
use warnings;
use Time::Fake;

my $before = CORE::time();
my $previous = Time::Fake->offset('+5m');
my $faked = time;
my $after = CORE::time();
die "unexpected clock offset" unless $previous == 0
    && $faked >= $before + 300 && $faked <= $after + 300;
die "unexpected reset" unless Time::Fake->reset == 300
    && Time::Fake->offset == 0;
print "installed clock offset and reset passed\n";
PERL
