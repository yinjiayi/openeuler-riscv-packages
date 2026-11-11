#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-hexdifferences
perl -MTest::HexDifferences -MTest::HexDifferences::HexDump -e '
    die "missing comparison API\n" unless Test::HexDifferences->can("eq_or_dump_diff");
    die "unexpected binary formatter result\n"
        unless hex_dump("ABCD") eq "0000 : 41 42 43 44 : ABCD\n";
    print "installed Test::HexDifferences binary formatting passed\n";
'
