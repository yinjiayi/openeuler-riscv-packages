#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

test "$(rpm -q --qf '%{VERSION}' perl-Algorithm-LCSS)" = '0.01'
perl -MAlgorithm::LCSS=LCSS,CSS,CSS_Sorted -e '
    die "unexpected module version\n" unless $Algorithm::LCSS::VERSION eq "0.01";
    die "string result mismatch\n" unless LCSS("abcdef", "zzcdeyy") eq "cde";
    my $array = LCSS([qw(a b c d)], [qw(x b c y)]);
    die "array result mismatch\n" unless join("", @$array) eq "bc";
    my $sorted = CSS_Sorted("abcdefghijklmnopqrstuvwxyz", "flubberabcdubberdofghijklm");
    die "sorted result mismatch\n" unless join(" ", @$sorted) eq "fghijklm abcd e";
    print "Algorithm::LCSS installed smoke passed\n";
'
