#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-test-abortable
perl -MTest::Abortable -e '
    my $out = Test::Abortable::testeval { 6 * 7 };
    die "wrong successful block result" unless $out == 42;
    eval { Test::Abortable::testeval { die "ordinary error\n" } };
    die "ordinary error swallowed" unless $@ eq "ordinary error\n";
    print "ok 1 - installed Test::Abortable preserves successful results and propagates ordinary errors\n";
'
