#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtest-deep-fuzzy-perl
perl -MTest::Deep -MTest::Deep::Fuzzy -e '
    my $want = { number => is_fuzzy_num(0.008, 0.001) };
    die "equal rounding bucket was rejected\n"
        unless Test::Deep::eq_deeply({ number => 0.0078125 }, $want);
    die "different rounding bucket was accepted\n"
        if Test::Deep::eq_deeply({ number => 0.015 }, $want);
    print "installed Test::Deep::Fuzzy compares same and different rounding buckets\n";
'
