#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-tie-sub
perl -MTie::Sub -e '
    tie my %out, "Tie::Sub", sub { return join(":", @_) };
    die "scalar fetch" unless $out{word} eq "word";
    die "argument-vector fetch" unless $out{[qw(a b)]} eq "a:b";
    print "installed tied subroutine scalar and argument-vector lookup passed\n";
'
