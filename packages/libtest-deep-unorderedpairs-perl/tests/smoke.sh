#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-deep-unorderedpairs
perl -MTest::Deep=eq_deeply -MTest::Deep::UnorderedPairs -e '
    die "unordered repeated tuple match failed" unless
        eq_deeply([b=>3, a=>1, a=>2], tuples(a=>1, a=>2, b=>3));
    die "unexpected tuple match" if
        eq_deeply([b=>3, a=>1, a=>4], tuples(a=>1, a=>2, b=>3));
    print "installed Test::Deep::UnorderedPairs repeated tuple comparison passed\n";
'
