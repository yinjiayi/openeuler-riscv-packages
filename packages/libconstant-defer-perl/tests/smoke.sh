#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libconstant-defer-perl
perl -e '
    my $calls = 0;
    use constant::defer SMOKE_VALUE => sub { ++$calls; 42 };
    die "constant calculated before first lookup\n" if $calls;
    die "constant did not cache the first result\n"
        unless SMOKE_VALUE() == 42 && SMOKE_VALUE() == 42 && $calls == 1;
    print "installed deferred constant computes once\n";
'
