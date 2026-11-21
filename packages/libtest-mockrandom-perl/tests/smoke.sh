#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-mockrandom

perl -MTest::MockRandom -e '
    my $random = Test::MockRandom->new(0.25, 0.75);
    die "unexpected deterministic sequence\n"
        unless $random->rand(8) == 2 && $random->rand(4) == 3
            && $random->rand() == 0;
    print "ok 1 - installed MockRandom returns deterministic scaled sequence\n";
'
