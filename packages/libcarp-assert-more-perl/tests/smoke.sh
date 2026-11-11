#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcarp-assert-more-perl
perl -MCarp::Assert::More -e '
    assert_integer(42);
    my $accepted = eval { assert_integer("not-an-integer"); 1 };
    die "invalid integer did not trigger the expected assertion\n"
        if $accepted || $@ !~ /Assertion.+failed/;
    print "installed integer assertion accepts and rejects correctly\n";
'
